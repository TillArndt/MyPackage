
import FWCore.ParameterSet.Config as cms
import MyPackage.TtGammaAnalysis.sequenceCocPatPhoton_cfi as cocPhot


widenedCocPatPhotons = cocPhot.cocPatPhotons.clone(
    src = "photonInputDummy"
)
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 5.0
widenedCocPatPhotons.checkOverlaps.muons.deltaR = 5.0
widenedCocPatPhotons.checkOverlaps.jets.requireNoOverlaps = False
widenedCocPatPhotons.checkOverlaps.muons.requireNoOverlaps = False

analyzer_Photon = cms.EDAnalyzer(
    "MyPhotonAnalyzer",
    src = cms.InputTag("widenedCocPatPhotons")
)

overlapsPath = cms.Path(
      widenedCocPatPhotons
    * analyzer_Photon
)
