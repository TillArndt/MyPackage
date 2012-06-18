import FWCore.ParameterSet.Config as cms


puReweight  = ""
try:
    puReweight  = crc_var.get("puReweight", puReweight)
except NameError:
    print "<"+__name__+">: crc_var not in __builtin__!"


# PRODUCERS
# large pt ...
largeEtPhotons = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonInputDummy"),
            cut = cms.string('\
    et > 20 \
    && abs(eta) < 2.1 \
    '),
            filter = cms.bool(False)
)

# require tight Photon ID
photonsWithTightID = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("largeEtPhotons"),
            cut = cms.string('photonID("PhotonCutBasedIDTight")'),
            filter = cms.bool(False)
)



# FILTERS
largeEtFilter = cms.EDFilter(
    "PATCandViewCountFilter",
    src = cms.InputTag("largeEtPhotons"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(9999)
)

tightIDFilter = largeEtFilter.clone(
    src = cms.InputTag("photonsWithTightID")
)

hardPhotonFilters = cms.Sequence(
      largeEtFilter
    * tightIDFilter
)

