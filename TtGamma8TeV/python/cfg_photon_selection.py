
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
    useMerging  = cms_var.get("useMerging", useMerging)
    preSelOpt   = cms_var.get("preSelOpt",preSelOpt)
    puReweight  = cms_var.get("puWeight", puWeight)
    sample      = cms_var.get("sample", sample)
    skipChecks  = cms_var.get("skipChecks", skipChecks)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"
print "<"+__name__+">: Running On MC:", runOnMC
print "<"+__name__+">: Samplename is:", legend


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
    fileName = cms.string('TFILESERVICEmyPhotonSelection.root')
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
process.load("MyPackage.TtGamma8TeV.cfi_mcTruth")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
process.load("MyPackage.TtGamma8TeV.cfi_photonUserData")
process.load("MyPackage.TtGamma8TeV.cfi_evtWeightPU")
#process.load("MyPackage.TtGamma8TeV.cff_dataMCComp")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
process.load("MyPackage.TtGamma8TeV.cff_jets")
process.load("MyPackage.TtGamma8TeV.cff_preSel")

process.photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("widenedCocPatPhotons"),
    cut = cms.string(""),
    filter = cms.bool(False)
)

if preSelOpt == "go4Signal":
    process.preSel.replace(
        process.bTagRequirement,
        process.bTagRequirement
        * process.ttgammaMerging
        * process.patPhotonsSignal
        * process.patPhotonsSignalCounter
    )
#    process.widenedCocPatPhotons.src = "photonsSignalTwo2Seven"

if preSelOpt == "go4Noise":
    process.preSel.replace(
        process.bTagRequirement,
        process.bTagRequirement
        * process.ttgammaMerging
        * process.patPhotonsSignal
        * ~process.patPhotonsSignalCounter
    )
#    process.widenedCocPatPhotons.src = "photonsSignalTwo2Seven"

if preSelOpt == "go4Whiz":
    process.patPhotonsSignal.genSignal = "photonsSignalME"
    process.preSel.replace(
        process.bTagRequirement,
        process.bTagRequirement
        * process.photonsSignalMEsequence
        * process.patPhotonsSignal
    )

# Path declarations
#process.dataMC = cms.Path(
#    process.preSel *
#     process.dataMCSequence
#)

process.producerPath = cms.Path(
    process.preSel *
    process.puWeight *
#    process.photonUserDataSequence *
    process.jetSequence *
    process.widenedCocPatPhotons *
    process.photonInputDummy
)

process.selectionPath = cms.Path(
    process.preSel *
    process.photonInputDummy
)

if preSelOpt == "go4Signal" or preSelOpt == "go4Noise":
    process.selectionPath.replace(
        process.ttbarPhotonMerger,
        process.ttbarPhotonMergerSingleCall
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
#    process.dataMC,
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
else:
    process.dataTemplatePathSihih.insert(0, process.preSel * process.Nm1FiltsihihEB)
    process.dataTemplatePathChHadIso.insert(0, process.preSel * process.Nm1FiltchargedHadronIsoEB)
    process.schedule.append(process.dataTemplatePathSihih)
    process.schedule.append(process.dataTemplatePathChHadIso)


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
    for p in process.schedule:
        p.remove(process.bTagRequirement)

    # event count will produce invalid result, if lumis sections are skipped
    process.selectionPath.remove(process.InputCntPrnt)
    process.selectionPath.remove(process.OutputCntPrnt)
    process.options.fileMode = cms.untracked.string('NOMERGE')
    if runOnMC:
        process.options.emptyRunLumiMode = cms.untracked.string(
            'doNotHandleEmptyRunsAndLumis'
        )


############################################# output module for debugging ###
#process.out = cms.OutputModule( "PoolOutputModule",
#    outputCommands  = cms.untracked.vstring( 'keep *' ),
#    SelectEvents    = cms.untracked.PSet( SelectEvents = cms.vstring('producerPath') ),
#    fileName        = cms.untracked.string("test_out_" + sample + ".root"),
#)
#process.outPath = cms.EndPath(process.out)
#process.schedule.append(process.outPath)


