
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

process.widenedCocPatPhotons.src = "photonUserDataLargestPdgId"
process.photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("widenedCocPatPhotons"),
    cut = cms.string(""),
    filter = cms.bool(False)
)

if preSelOpt == "doOverlapRemoval":
    process.preSel.replace(
        process.bTagCounter,
        process.bTagCounter
        * process.ttgammaMerging
        * process.topPtSequenceTTBar   ## also do the top pt production
    )

# Path declarations
process.dataMC = cms.Path(
    process.preSel *
    process.dataMCSequence
)

process.producerPath = cms.Path(
    process.preSel *
    process.puWeight *
    process.photonUserDataLargestPdgId *
#    process.jetSequence *
    process.widenedCocPatPhotons *
    process.photonInputDummy
)

process.selectionPath = cms.Path(
    process.preSel *
    process.photonInputDummy
)

#process.load("MyPackage.TtGamma8TeV.cff_vtxMultiplicity")
#if puWeight:
#    process.schedule.append(process.vtxMultPath)


################################################################### ID CUTS ###
from MyPackage.TtGamma8TeV.cff_photonIDCuts import add_photon_cuts
pre_paths, post_paths = add_photon_cuts(process)

# schedule
process.schedule = cms.Schedule(
    *pre_paths
)
process.schedule += [
    process.producerPath,
    process.dataMC,
    process.selectionPath,
#    process.overlapsPath,
]
process.schedule += post_paths


######################################################### template creation ###
process.load("MyPackage.TtGamma8TeV.cff_templateCreation")
if runOnMC:
    process.templatePathSihih.insert(0, process.preSel * process.Nm1FiltsihihEB)
    process.templatePathChHadIso.insert(0, process.preSel * process.Nm1FiltchargedHadronIsoEB)
    process.schedule.append(process.templatePathSihih)
    process.schedule.append(process.templatePathChHadIso)

process.dataTemplatePathSihih.insert(0, process.preSel * process.Nm1FiltsihihEB)
process.dataTemplatePathChHadIso.insert(0, process.preSel * process.Nm1FiltchargedHadronIsoEB)
process.schedule.append(process.dataTemplatePathSihih)
process.schedule.append(process.dataTemplatePathChHadIso)

########################################### data driven background template ###
# n-2 paths and sideband background templates
import MyPackage.TtGamma8TeV.cff_templateDatDrvBkg as ddrvTmpl
process.schedule += ddrvTmpl.add_bkg_template_path(process)
if runOnMC:
    process.schedule += ddrvTmpl.add_nm2_path(process)
else:
    process.schedule += ddrvTmpl.add_nm2_path_core(process)

# paths for sihih background template with loose id
import MyPackage.TtGamma8TeV.cff_templateDatDrvBkgLooseID as ddrvTmplLoose
if runOnMC:
    process.schedule += ddrvTmplLoose.add_path_truth(process)
else:
    process.schedule += ddrvTmplLoose.add_path_core(process)

#################################################### real tight id counters ###
if runOnMC:
    process.realFullTightID = process.realPhotonsSihih.clone(
        src = "FullTightIDBlocking",
        filter = True,
    )
    process.realFullTightIDCount = process.FullTightIDCount.clone()
    process.realFullTightIDCountPrnt = process.FullTightIDCountPrnt.clone(
        src = "realFullTightIDCount"
    )
    process.realFullTightIDSequence = cms.Sequence(
        process.realFullTightID
        * process.realFullTightIDCount
        * process.realFullTightIDCountPrnt
    )
    process.pathLooseID *= process.realFullTightIDSequence

##################################### sihih shifted histos for template fit ###
if runOnMC:
    from MyPackage.TtGamma8TeV.cff_templateCreation import add_sihih_shifted_histos
    add_sihih_shifted_histos(process)
    process.sihihShiftPath.insert(0, process.preSel)
    process.schedule += [process.sihihShiftPath]


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


################################################ output module for debugging ###
#process.out = cms.OutputModule( "PoolOutputModule",
#    outputCommands  = cms.untracked.vstring( 'keep *' ),
#    SelectEvents    = cms.untracked.PSet( SelectEvents = cms.vstring('pathLooseID') ),
#    fileName        = cms.untracked.string("outputEvents/" + sample + ".root"),
#)
#process.outPath = cms.EndPath(process.out)
#process.schedule.append(process.outPath)


