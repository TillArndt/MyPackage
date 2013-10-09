

sample      = ""
preSelOpt   = None
try:
    print "cms_var options: "
    print cms_var
    sample      = cms_var.get("sample", sample)
    preSelOpt   = cms_var.get("preSelOpt",preSelOpt)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"
print "<"+__name__+">: Samplename is:", sample


###############################################################################
import FWCore.ParameterSet.Config as cms

puWeight = cms.untracked.InputTag("puWeight", "PUWeightTrue")

process = cms.Process("NTuple")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(""),
    noEventSort = cms.untracked.bool( True ),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop *_conditionsInEdm_*_*',
        'drop *_logErrorTooManyClusters_*_*',
    )
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TFILESERVICE_cfg_produce_ntuple.root')
)

########################################################## input and presel ###
process.load("MyPackage.TtGamma8TeV.cfi_cocPatPhotons")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
process.load("MyPackage.TtGamma8TeV.cfi_evtWeightPU")
process.load("MyPackage.TtGamma8TeV.cff_dataMCComp")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
process.load("MyPackage.TtGamma8TeV.cfi_topPtSequence")
process.load("MyPackage.TtGamma8TeV.cff_jets")
process.load("MyPackage.TtGamma8TeV.cff_preSel")

process.widenedCocPatPhotons.src = "photonUserDataSCFootRm"
process.photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("widenedCocPatPhotons"),
    cut = cms.string("et > 25. && abs(eta) < 1.4442"),
    filter = cms.bool(True)
)

if preSelOpt == "doOverlapRemoval":
    process.preSel.replace(
        process.bTagCounter,
        process.bTagCounter
        * process.ttgammaMerging
        * process.topPtSequenceTTBar
    )

process.InputProducerSequence = cms.Sequence()
if preSelOpt in ("doOverlapRemoval", "go4Whiz"):
    process.puWeight.weights = cms.untracked.InputTag("topPtWeight")
    process.InputProducerSequence *= process.topPtSequenceTTBar

# btag weight
process.bTagWeight.weights = process.puWeight.weights
process.puWeight.weights = cms.untracked.InputTag("bTagWeight")

################################################################ cutstrings ###
from MyPackage.TtGamma8TeV.cff_templateCreation import real
from MyPackage.TtGamma8TeV.cff_photonIDCuts import cuts_for_plot
from MyPackage.TtGamma8TeV.cff_templateDatDrvBkgSBID import lower_cut, sieie, pfneutralIso, pfphoIso

id_cut_key_list = [
    "drmuon",
    "drjet",
    "passEleVeto",
    "hadTowOverEm",
    "sihihEB",
    "neutralHadronIsoEB",
    "photonIsoEB",
]
id_cuts_list = list(cuts_for_plot[cutkey][0] for cutkey in id_cut_key_list)
id_cut = "( " + ") && (".join(id_cuts_list) + " )"

def bool_cut(cut):
    return "?("+cut+")? 1. : 0. "

process.photonTuple = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("photonInputDummy"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
        ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
        ),
        cms.PSet(
            tag = cms.untracked.string("idCut"),
            quantity = cms.untracked.string(bool_cut(id_cut))
        ),
        cms.PSet(
            tag = cms.untracked.string("lowerCut"),
            quantity = cms.untracked.string(bool_cut(lower_cut))
        ),
        cms.PSet(
            tag = cms.untracked.string("real"),
            quantity = cms.untracked.string(bool_cut(real))
        ),
        cms.PSet(
            tag = cms.untracked.string("chargedisoSCFootRmEB"),
            quantity = cms.untracked.string(cuts_for_plot["chargedisoSCFootRmEB"][5])
        ),
        cms.PSet(
            tag = cms.untracked.string("sieie"),
            quantity = cms.untracked.string(sieie)
        ),
        cms.PSet(
            tag = cms.untracked.string("pfneutralIso"),
            quantity = cms.untracked.string(pfneutralIso)
        ),
        cms.PSet(
            tag = cms.untracked.string("pfphoIso"),
            quantity = cms.untracked.string(pfphoIso)
        ),
    )
)

process.p = cms.Path(
    process.preSel *
    process.InputProducerSequence *
    process.bTagWeight *
    process.puWeight *
    process.widenedCocPatPhotons *
    process.photonInputDummy *
    process.photonTuple
)

#################################################################### output ###
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(
        "outputNTuple/"
        + sample
        + '_edmTuple.root'
    ),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_puWeight_*_*',
        'keep *_photonTuple_*_*'
    )
)

process.outpath = cms.EndPath(process.out)
