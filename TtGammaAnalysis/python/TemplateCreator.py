

puWeight = None
try:
    puWeight  = crc_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: crc_var not in __builtin__!"


templateBase = "PhotonProducerhcaliso"
import FWCore.ParameterSet.Config as cms

matched = 'genParticlesSize>0'
real = '\
genParticlesSize>0\
&& (abs(energy - genParticle.energy) / genParticle.energy / 2.)^2 \
< (\
(3.63 / sqrt(energy))^2 \
+ (.124 / energy)^2 \
+ (0.3)^2 \
)'

# Filters
matchedPhotons = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(templateBase),
    cut = cms.string(matched),
    filter = cms.bool(False)
)
unmatchedPhotons = matchedPhotons.clone(
    cut = cms.string('!(' + matched + ')')
)
realPhotons = matchedPhotons.clone(
    cut = cms.string(real)
)
fakePhotons = matchedPhotons.clone(
    cut = cms.string('!(' + real + ')')
)

# Analyzers
matchedTemplate = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("matchedPhotons"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(0.09),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('sihih'),
            description  = cms.untracked.string(';#sigma_{i #eta i #eta};number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('sigmaIetaIeta')
        ),
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(40.),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('HoCoTrkIso'),
            description  = cms.untracked.string(';hollow cone track isolation / GeV;number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('trkSumPtHollowConeDR04')
        )
    )
)
if puWeight:
    matchedTemplate.weights = puWeight
unmatchedTemplate = matchedTemplate.clone(
    src = cms.InputTag("unmatchedPhotons"),
)
realTemplate = matchedTemplate.clone(
    src = cms.InputTag("realPhotons"),
)
fakeTemplate = matchedTemplate.clone(
    src = cms.InputTag("fakePhotons"),
)

templatePath = cms.Path(
    matchedPhotons
    * unmatchedPhotons
    * realPhotons
    * fakePhotons
    * matchedTemplate
    * unmatchedTemplate
    * realTemplate
    * fakeTemplate
)

dataTemplateFitPhotons = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(templateBase),
    cut = cms.string("1<2"),
    filter = cms.bool(False)
)
dataTemplateFitHisto = matchedTemplate.clone(
    src = cms.InputTag("dataTemplateFitPhotons")
)

templatePathData = cms.Path(
    dataTemplateFitPhotons
    * dataTemplateFitHisto
)