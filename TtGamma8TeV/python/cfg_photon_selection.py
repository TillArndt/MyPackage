
# fetch variables from CmsRunController
runOnMC     = True
legend      = NameError
useMerging  = ""
preSelOpt   = None
puWeight    = None
sample      = ""
skipChecks  = False

try:
    print "cms_var options: "
    print cms_var
    runOnMC     = not cms_var["is_data"]
    legend      = cms_var["legend"]
    preSelOpt   = cms_var.get("preSelOpt",preSelOpt)
    puWeight    = cms_var.get("puWeight", puWeight)
    sample      = cms_var.get("sample", sample)
    skipChecks  = cms_var.get("skipChecks", skipChecks)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"
print "<"+__name__+">: Running On MC:", runOnMC
print "<"+__name__+">: Samplename is:", sample


############################################## Regular Config starting here ###
###############################################################################

import FWCore.ParameterSet.Config as cms

puWeightInstance = puWeight
if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)

process = cms.Process('PhotonSelection')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( '' ),
    noEventSort = cms.untracked.bool( True ),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop *_conditionsInEdm_*_*',
        'drop *_logErrorTooManyClusters_*_*',
    )
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TFILESERVICE_cfg_photon_selection.root')
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
#logger.MessageLogger.categories +=  (["TTGammaMerger"])
#logger.MessageLogger.categories +=  (["checkCorrs"])
#logger.MessageLogger.categories +=  (["EvtWeightPU"])
logger.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

# input and presel
process.load("MyPackage.TtGamma8TeV.cfi_cocPatPhotons")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
process.load("MyPackage.TtGamma8TeV.cfi_photonUserData")
process.load("MyPackage.TtGamma8TeV.cfi_evtWeightPU")
process.load("MyPackage.TtGamma8TeV.cff_dataMCComp")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
process.load("MyPackage.TtGamma8TeV.cfi_topPtSequence")
process.load("MyPackage.TtGamma8TeV.cff_jets")
process.load("MyPackage.TtGamma8TeV.cff_preSel")

#process.widenedCocPatPhotons.src = "photonUserDataLargestPdgId"
process.widenedCocPatPhotons.src = "photonUserDataSCFootRm"
process.photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("widenedCocPatPhotons"),
    cut = cms.string(""),
    filter = cms.bool(False)
)



# options for ttbar and ttgam
if preSelOpt == "doOverlapRemoval":
    process.preSel.replace(
        process.bTagCounter,
        process.bTagCounter
        * process.ttgammaMerging
        * process.topPtSequenceTTBar   ## also do the top pt production
    )
elif preSelOpt == "go4Whiz":
    process.topPtTTbar.two2fiveMode = cms.untracked.bool(True)

process.InputProducerSequence = cms.Sequence()
if preSelOpt in ("doOverlapRemoval", "go4Whiz"):
    process.puWeight.weights = cms.untracked.InputTag("topPtWeight")
    process.InputProducerSequence *= process.topPtSequenceTTBar
    
    # make btag weight only (non convoluted with previous ones)
    process.bTagWeightVanilla = process.bTagWeight.clone(weights="")
    process.InputProducerSequence *= process.bTagWeightVanilla
    process.bTagWeightHisto.src = "bTagWeightVanilla"

# btag weight
process.bTagWeight.weights = process.puWeight.weights
process.puWeight.weights = cms.untracked.InputTag("bTagWeight")

# final weight histogram
process.eventWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src     = cms.InputTag("puWeight", puWeightInstance),
    name    = cms.untracked.string("histo"),
    title   = cms.untracked.string(";final event weight;events"),
    nbins   = cms.untracked.int32(50),
    min     = cms.untracked.double(0.),
    max     = cms.untracked.double(2.),
)

# Path declarations
process.producerPath = cms.Path(
    process.preSel *
    process.InputProducerSequence *
    process.bTagWeight *
    process.bTagWeightHisto *
    process.puWeight *
    process.eventWeightHisto *
#    process.photonUserDataLargestPdgId *
#    process.jetSequence *
    process.widenedCocPatPhotons *
    process.photonInputDummy
)

process.selectionPath = cms.Path(
    process.preSel *
    process.photonInputDummy
)

process.dataMC = cms.Path(
    process.preSel *
    process.dataMCSequence
)

process.load("MyPackage.TtGamma8TeV.cff_vtxMultiplicity")


################################################################### ID CUTS ###
from MyPackage.TtGamma8TeV.cff_photonIDCuts import add_photon_cuts
pre_paths, post_paths = add_photon_cuts(process)

# schedule
process.schedule = cms.Schedule(
    *pre_paths
)
process.schedule += [
    process.producerPath,
    process.selectionPath,
    process.dataMC,
]
process.schedule += post_paths

if puWeight:
    process.schedule.append(process.vtxMultPath)

######################################################### template creation ###
process.load("MyPackage.TtGamma8TeV.cff_templateCreation")
process.TemplatePathSihih.insert(0, process.preSel * process.Nm1FiltsihihEB)
process.TemplatePathChHadIso.insert(0, process.preSel * process.Nm1FiltchargedHadronIsoEB)
process.schedule.append(process.TemplatePathSihih)
process.schedule.append(process.TemplatePathChHadIso)

########################################### data driven background template ###
# n-2 paths and sideband background templates
import MyPackage.TtGamma8TeV.cff_templateDatDrvBkg as ddrvTmpl
process.schedule += ddrvTmpl.add_bkg_template_path(process)
if runOnMC:
    process.schedule += ddrvTmpl.add_nm2_path(process)
else:
    process.schedule += ddrvTmpl.add_nm2_path_core(process)

# paths for sihih background template with loose id
import MyPackage.TtGamma8TeV.cff_templateDatDrvBkgSihihSB as ddrvTmplSihihSB
if runOnMC:
    process.schedule += ddrvTmplSihihSB.add_path_truth(process)
else:
    process.schedule += ddrvTmplSihihSB.add_path_core(process)

# paths for sihih background template with loose id
import MyPackage.TtGamma8TeV.cff_templateDatDrvBkgSBID as ddrvTmplSBID
if runOnMC:
    process.schedule += ddrvTmplSBID.add_path_truth(process)
else:
    process.schedule += ddrvTmplSBID.add_path_core(process)


##################################### sihih shifted histos for template fit ###
#if runOnMC:
#    from MyPackage.TtGamma8TeV.cff_templateCreation import add_sihih_shifted_histos
#    add_sihih_shifted_histos(process)
#    process.sihihShiftPath.insert(0, process.preSel)
#    process.schedule += [process.sihihShiftPath]


#################################################### real tight id counters ###
if runOnMC:
    process.FullIDreal = process.PhotonsSihihreal.clone(
        src = "FullIDBlocking",
        filter = True,
    )
    process.FullIDCountreal = process.FullIDCount.clone()
    process.FullIDCountrealPrnt = process.FullIDCountPrnt.clone(
        src = "FullIDCountreal"
    )
    process.FullIDrealSequence = cms.Sequence(
        process.FullIDreal
        * process.FullIDCountreal
        * process.FullIDCountrealPrnt
    )
    process.pathLooseID *= process.FullIDrealSequence


############################################################### event count ###
process.InputEventCount = cms.EDProducer("EventCountProducer")
process.OutputEventCount = cms.EDProducer("EventCountProducer")
#process.out.outputCommands += ["keep *_*EventCount*_*_*"]

process.selectionPath.insert(0, process.InputEventCount)
process.selectionPath += process.OutputEventCount

process.InputCntPrnt = cms.EDAnalyzer("EventCountPrinter",
    src = cms.InputTag("InputEventCount", "", "PAT")
)
process.OutputCntPrnt = cms.EDAnalyzer("EventCountPrinter",
    src = cms.InputTag("OutputEventCount", "", "MERGE")
)
process.selectionPath.insert(0, process.OutputCntPrnt)
process.selectionPath.insert(0, process.InputCntPrnt)


################################################################ skip checks ###
if skipChecks:
    process.source.duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
    process.producerPath.remove(process.CheckOneObj)

    # event count will produce invalid result, if lumis sections are skipped
    process.selectionPath.remove(process.InputCntPrnt)
    process.selectionPath.remove(process.OutputCntPrnt)
    process.options.fileMode = cms.untracked.string('NOMERGE')
    if runOnMC:
        process.options.emptyRunLumiMode = cms.untracked.string(
            'doNotHandleEmptyRunsAndLumis'
        )

# btag currently not needed
#process.preSel.remove(process.bTagRequirement)
#process.preSel.remove(process.bTagCounter)

################################################ output module for debugging ###
#process.out = cms.OutputModule( "PoolOutputModule",
#    outputCommands  = cms.untracked.vstring( 'keep *' ),
#    SelectEvents    = cms.untracked.PSet( SelectEvents = cms.vstring('pathLooseID') ),
#    fileName        = cms.untracked.string("outputEvents/" + sample + ".root"),
#)
#process.outPath = cms.EndPath(process.out)
#process.schedule.append(process.outPath)


