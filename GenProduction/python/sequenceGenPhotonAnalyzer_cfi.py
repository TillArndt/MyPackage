import FWCore.ParameterSet.Config as cms

anaPT_phoME = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("photonsME"),
    #weights = cms.untracked.InputTag("puWeight", "Reweight1BX"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(         0.),
            max          = cms.untracked.double(        700),
            nbins        = cms.untracked.int32 (        350),
            name         = cms.untracked.string( 'photonPT'),
            description  = cms.untracked.string(';photon p_{T} / GeV;number of photons'),
            plotquantity = cms.untracked.string('pt'),
        )
    )
)

anaPT_phoTopShow = anaPT_phoME.clone(
    src = "photonsTopShower"
)

anaPT_phoBotShow = anaPT_phoME.clone(
    src = "photonsBottomShower"
)

anaPT_phoWBoShow = anaPT_phoME.clone(
    src = "photonsWBosonShower"
)

anaPT_phoOther  = anaPT_phoME.clone(
    src = "photonsOther"
)

genPhotonAnalyzerSequence = cms.Sequence(
      anaPT_phoME
    * anaPT_phoTopShow
    * anaPT_phoBotShow
    * anaPT_phoWBoShow
    * anaPT_phoOther
)
