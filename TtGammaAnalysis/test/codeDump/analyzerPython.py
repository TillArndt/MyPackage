
# Analyzer, not used because cut parser cannot iterate 
analyzerDR_PhotonsFromME = cms.EDAnalyzer(
    "PATPhotonHistoAnalyzer",
    src = cms.InputTag("patPhotonsFromME"),
    histograms = cms.VPSet(
            cms.PSet(min          = cms.untracked.double(         0.),
                     max          = cms.untracked.double(        1.1),
                     nbins        = cms.untracked.int32 (         44),
                     name         = cms.untracked.string( 'deltaRJets'),
                     description  = cms.untracked.string('deltaR(photon, jet);dR;count'),
                     plotquantity = cms.untracked.string('\
 ? overlaps("jets").size > 0 ?\
 deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) : 1.09 \
                                                          '),
                     lazyParsing  = cms.untracked.bool(True)
            ),
            cms.PSet(min          = cms.untracked.double(         0.),
                     max          = cms.untracked.double(        1.1),
                     nbins        = cms.untracked.int32 (         44),
                     name         = cms.untracked.string( 'deltaRMuons'),
                     description  = cms.untracked.string('deltaR(photon, muon);dR;count'),
                     plotquantity = cms.untracked.string('\
 ? overlaps("muons").size > 0 ?\
 deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi) : 1.09 \
                                                          '),
                     lazyParsing  = cms.untracked.bool(True)
            ),
    )
)
