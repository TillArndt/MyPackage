sample = ""
try:
    sample = cms_var.get("sample", sample)
except NameError:
    pass

hltPath = ['HLT_*']
if "RunA" in sample:
    hltPath = ["HLT_IsoMu17_eta2p1_TriCentralPFJet30_v*"]
elif "RunB" in sample:
    hltPath = [
        "HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_v*",
        "HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_30_20_v*",
    ]
elif ("RunC" in sample) or ("RunD" in sample):
    hltPath = [
        "HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_30_20_v*",
        "HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet45_35_25_v*",
    ]

import FWCore.ParameterSet.Config as cms

l1Tag  = cms.InputTag('') # skip L1 results, since conflicts with the GlobalTag can occur
hltTag = cms.InputTag('TriggerResults::HLT')

from HLTrigger.special.hltPhysicsDeclared_cfi import *
hltPhysicsDeclared.L1GtReadoutRecordTag = l1Tag

from HLTrigger.HLTfilters.triggerResultsFilter_cfi import *
triggerResults = triggerResultsFilter.clone(
    hltResults = hltTag,
    l1tResults = l1Tag,
    throw      = False,
    triggerConditions = cms.vstring(*hltPath),
)

triggerSelection = cms.Sequence(
#  hltPhysicsDeclared *
  triggerResults
)
