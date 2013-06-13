
jetsource  = "AnalysisJets" #"selectedPatJetsForAnalysis"
muonsource = "tightmuons"
try:
    jetsource = cms_var.get("jetsource", jetsource)
    muonsource = cms_var.get("jetsource", muonsource)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

#PRODUCERS
# cross object clean
cocPatPhotons = cms.EDProducer("PATPhotonCleaner",
    src = cms.InputTag(""),
    preselection = cms.string(''),

    # overlap checking configurables
    checkOverlaps = cms.PSet(
        jets = cms.PSet(
            src                 = cms.InputTag(jetsource),
            algorithm           = cms.string("byDeltaR"),
            preselection        = cms.string(""),  # don't preselect the jets
            deltaR              = cms.double(0.5), # if > 0.5: make many jets overlapping
            checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
            pairCut             = cms.string(""),
            requireNoOverlaps   = cms.bool(True),
        ),
        muons = cms.PSet(
            src                 = cms.InputTag(muonsource),
            algorithm           = cms.string("byDeltaR"),
            preselection        = cms.string(""),
            deltaR              = cms.double(0.5),
            checkRecoComponents = cms.bool(False),
            pairCut             = cms.string(""),
            requireNoOverlaps   = cms.bool(True),
        ),
    ),
    finalCut = cms.string(''),
)

widenedCocPatPhotons = cocPatPhotons.clone(
    src = "photonUserData"
)
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 50000.0
widenedCocPatPhotons.checkOverlaps.muons.deltaR = 50000.0
widenedCocPatPhotons.checkOverlaps.jets.requireNoOverlaps = False
widenedCocPatPhotons.checkOverlaps.muons.requireNoOverlaps = False


#process.overlapsPath = cms.Path(
#    process.preSel
#    * process.analyzer_Photon
#    * process.analyzer_ET
#)
