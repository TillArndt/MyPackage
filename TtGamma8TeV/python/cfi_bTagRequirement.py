
jetsource  = "selectedPatJetsForAnalysis"
try:
    jetsource = cms_var.get("jetsource", jetsource)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

bTagRequirement = cms.EDFilter(
    "PATJetRefSelector",
    src = cms.InputTag(jetsource),
    cut = cms.string('bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679'),
    filter = cms.bool(True)
)
