
import FWCore.ParameterSet.Config as cms
import MyPackage.TtGammaAnalysis.sequenceCocPatPhoton_cfi as cocPhot

puWeight = None
try:
    puWeight  = crc_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: crc_var not in __builtin__!"

widenedCocPatPhotons = cocPhot.cocPatPhotons.clone(
    src = "patPhotonsPFlow"
)
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 50000.0
widenedCocPatPhotons.checkOverlaps.muons.deltaR = 50000.0
widenedCocPatPhotons.checkOverlaps.jets.requireNoOverlaps = False
widenedCocPatPhotons.checkOverlaps.muons.requireNoOverlaps = False

analyzer_Photon = cms.EDAnalyzer(
    "MyPhotonAnalyzer",
    src = cms.InputTag("widenedCocPatPhotons"),
)

# record pt before cutting
analyzer_ET = cms.EDAnalyzer(
    "PATPhotonHistoAnalyzer",
    src = cms.InputTag("photonInputDummy"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(         0.),
            max          = cms.untracked.double(       550.),
            nbins        = cms.untracked.int32 (         55),
            name         = cms.untracked.string( 'photonET'),
            description  = cms.untracked.string(';photon E_{T} / GeV;number of photons'),
            plotquantity = cms.untracked.string('et'),
        )
    )
)

if puWeight:
    analyzer_Photon.weights = puWeight
    analyzer_ET.weights = puWeight