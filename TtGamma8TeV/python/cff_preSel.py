import FWCore.ParameterSet.Config as cms

from MyPackage.TtGamma8TeV.cfi_bTagRequirement import bTagRequirement

OnlyBarrelPhotons = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("patPhotons"),
    cut = cms.string("abs(eta)<1.4442"),
    filter = cms.bool(True)
)

preSel = cms.Sequence(
    bTagRequirement
#    * OnlyBarrelPhotons
)

