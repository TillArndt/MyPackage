import FWCore.ParameterSet.Config as cms

from MyPackage.TtGamma8TeV.cfi_bTagRequirement import bTagRequirement

preSel = cms.Sequence(
    bTagRequirement
)

