import FWCore.ParameterSet.Config as cms

import MyPackage.TtGammaAnalysis.myBTagRequirement_cfi as btag
#import MyPackage.TtGammaAnalysis.sequenceHardPhoton_cfi as hardPhot
import MyPackage.TtGammaAnalysis.sequenceCocPatPhoton_cfi as cocPhot


widenedCocPatPhotons = cocPhot.cocPatPhotons.clone(
    src = "photonInputDummy"
)
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 1.0
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 1.0
widenedCocPatPhotons.checkOverlaps.jets.requireNoOverlaps = False
widenedCocPatPhotons.checkOverlaps.muons.requireNoOverlaps = False

analyzer_Photon = cms.EDAnalyzer(
    "MyPhotonAnalyzer",
    src = cms.InputTag("widenedCocPatPhotons")
)

overlapsPath = cms.Path(
      btag.myBTagRequirement
    * widenedCocPatPhotons
    * analyzer_Photon
)
