import FWCore.ParameterSet.Config as cms

import MyPackage.TtGammaAnalysis.myBTagRequirement_cfi as btag
import MyPackage.TtGammaAnalysis.sequenceHardPhoton_cfi as hardPhot
import MyPackage.TtGammaAnalysis.sequenceCocPatPhoton_cfi as cocPhot
import MyPackage.TtGammaAnalysis.mcTruthSequence_cfi as mcTruth

widenedCocPatPhotons = cocPhot.cocPatPhotons.clone()
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 1.0
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 1.0
widenedCocPatPhotons.checkOverlaps.jets.requireNoOverlaps = False
widenedCocPatPhotons.checkOverlaps.muons.requireNoOverlaps = False


analyzer_dRPhotonFromME = cms.EDAnalyzer("MyPhotonAnalyzer",
                     src = cms.InputTag("photonsFromME")
)

analyzer_dRPhotonFromElsewhere = analyzer_dRPhotonFromME.clone(
                     src = cms.InputTag("photonsFromElsewhere")
)

overlapsPath = cms.Path(
      btag.myBTagRequirement
    * hardPhot.hardPhotonSequence
    * mcTruth.mcTruthSequence
    * widenedCocPatPhotons
    * analyzer_dRPhotonFromME
    * analyzer_dRPhotonFromElsewhere
)
