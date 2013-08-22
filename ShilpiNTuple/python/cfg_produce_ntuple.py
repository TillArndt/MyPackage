

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
process.load("MyPackage.TtGamma8TeV.cfi_photonUserData")
process.load("MyPackage.TtGamma8TeV.cfi_evtWeightPU")
process.load("MyPackage.TtGamma8TeV.cff_dataMCComp")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
process.load("MyPackage.TtGamma8TeV.cff_jets")
process.load("MyPackage.TtGamma8TeV.cff_preSel")

process.widenedCocPatPhotons.src = "photonUserDataLargestPdgId"
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
    )


# Implementation of cutstrings
hoe             = "hadTowOverEm"
sieie           = "sigmaIetaIeta"
pfchargedIso    = "max(chargedHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_charged')), 0.)"
pfneutralIso    = "max(neutralHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_neutral')), 0.)"
pfphoIso        = "max(photonIso - (userFloat('kt6pf_rho')*userFloat('EA_photons')), 0.)"

cuthoe          = "0.05"
cutsieie        = "0.012"
cutchargedIso   = "4.0"
cutneutralIso   = "(4.5 + 0.04*pt)"
cutphoIso       = "(4.5 + 0.005*pt)"

maxchargedIso   = "min(0.2*et, 5*" + cutchargedIso  + ")"
maxneutralIso   = "min(0.2*et, 5*" + cutneutralIso  + ")"
maxphoIso       = "min(0.2*et, 5*" + cutphoIso      + ")"
maxhoe          = cuthoe

lower_cut = (
    "( "       + pfchargedIso + ">" + cutchargedIso
    + ") || (" + pfneutralIso + ">" + cutneutralIso
    + ") || (" + pfphoIso     + ">" + cutphoIso
    + ") || (" + sieie        + ">" + cutsieie
    + ")"
    )
upper_cut = (
    "( "       + pfchargedIso + "<" + maxchargedIso
    + ") && (" + pfneutralIso + "<" + maxneutralIso
    + ") && (" + pfphoIso     + "<" + maxphoIso
    + ") && (" + hoe          + "<" + maxhoe
    + ")"
    )

from MyPackage.TtGamma8TeV.cff_photonIDCuts import cuts
tight_cut_key_list = [
    "drmuon",
    "drjet",
    "hadTowOverEm",
    "chargedHadronIsoEB",
    "neutralHadronIsoEB",
    "photonIsoEB",
]
tight_cuts_list = list(cuts[cutkey][0] for cutkey in tight_cut_key_list)
tight_cuts_str = "( " + ") && (".join(tight_cuts_list) + " )"

tight_sideband_list = list(
    cuts[cutkey][0]
    for cutkey in tight_cut_key_list
    if cutkey != "chargedHadronIsoEB"
)
tight_sideband_list.append(
    pfchargedIso + " > 2. && 6. > " + pfchargedIso
)
tight_sideband_str = "( " + ") && (".join(tight_sideband_list) + " )"

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
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
        ),
        cms.PSet(
            tag = cms.untracked.string("maxAncestorPDG"),
            quantity = cms.untracked.string('userFloat("largestAncestorPdgId")')
        ),
        cms.PSet(
            tag = cms.untracked.string("motherPDG"),
            quantity = cms.untracked.string(
'?genParticlesSize>0 && genParticle.numberOfMothers>0?genParticle.mother.pdgId:0'
            )
        ),
        cms.PSet(
            tag = cms.untracked.string("LooseDenoID"),
            quantity = cms.untracked.string("?("+upper_cut+")&&("+lower_cut+")?1.:0.")
        ),
        cms.PSet(
            tag = cms.untracked.string("TightID"),
            quantity = cms.untracked.string("?("+tight_cuts_str+")?1.:0.")
        ),
        cms.PSet(
            tag = cms.untracked.string("TightSideband"),
            quantity = cms.untracked.string("?("+tight_sideband_str+")?1.:0.")
        ),
        cms.PSet(
            tag = cms.untracked.string("passEleVeto"),
            quantity = cms.untracked.string("userFloat('passEleVeto')")
        ),
        cms.PSet(
            tag = cms.untracked.string("sigmaIetaIeta"),
            quantity = cms.untracked.string("sigmaIetaIeta")
        ),
    )
)

process.p = cms.Path(
    process.preSel *
    process.puWeight *
    process.photonUserDataLargestPdgId *
    process.widenedCocPatPhotons *
    process.photonInputDummy *
    process.photonTuple
)

#################################################################### output ###
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(
        "/afs/cern.ch/work/h/htholen/public/photon_tuples/"
        + sample
        + '_edmTuple.root'
    ),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *', 'keep *_photonTuple_*_*')
)

process.outpath = cms.EndPath(process.out)
