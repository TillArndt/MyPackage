

puWeight = None
try:
    puWeight  = crc_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: crc_var not in __builtin__!"


templateBase = "PhotonProducerhadronicoverem"
import FWCore.ParameterSet.Config as cms

matched = 'genParticlesSize>0'

real = '\
(\
    genParticlesSize>0 \
    && (\
        (abs(energy - genParticle.energy) / genParticle.energy)^2 \
        < 4 * (\
        (3.63 / sqrt(genParticle.energy))^2 \
        + (.124 / genParticle.energy)^2 \
        + (0.3)^2 \
        )\
    )\
)'

piZero = '\
( \
 abs(genParticle.mother.pdgId) == 111 \
 || \
 abs(genParticle.mother.mother.pdgId) == 111 \
)'

prompt = real + '&& !' + piZero



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
    cut = cms.string(prompt)
)
fakePhotons = matchedPhotons.clone(
    cut = cms.string('!(' + prompt + ')')
)
piZeroPhotons = matchedPhotons.clone(
    cut = cms.string(real + "&&" + piZero)
)

# Analyzers
matchedTemplate = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("matchedPhotons"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(0.08),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('sihih'),
            description  = cms.untracked.string(';#sigma_{i #eta i #eta};number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('sigmaIetaIeta')
        ),
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(0.08),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('sihihEE'),
            description  = cms.untracked.string(';#sigma_{i #eta i #eta};number of photons (endcap)'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('?abs(eta) > 1.5? sigmaIetaIeta: -0.1')
        ),
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(0.08),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('sihihEB'),
            description  = cms.untracked.string(';#sigma_{i #eta i #eta};number of photons (barrel)'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('?abs(eta) < 1.5? sigmaIetaIeta: -0.1')
        ),
    )
)
matchQuality = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("realPhotons"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(0.02),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('deltaR'),
            description  = cms.untracked.string(';#DeltaR(#gamma_{reco},#gamma_{gen});number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('deltaR(eta, phi, genParticle.eta, genParticle.phi)')
        ),
        cms.PSet(
            min          = cms.untracked.double(-0.2),
            max          = cms.untracked.double(0.2),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('deltaErel'),
            description  = cms.untracked.string(';(E_{#gamma,reco} - E_{#gamma,gen}) / E_{#gamma,gen};number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('(energy - genParticle.energy) / genParticle.energy')
        ),
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
piZeroTemplate = matchedTemplate.clone(
    src = cms.InputTag("piZeroPhotons"),
)
templatePath = cms.Path(
    matchedPhotons
    * unmatchedPhotons
    * realPhotons
    * fakePhotons
    * piZeroPhotons
    * matchedTemplate
    * unmatchedTemplate
    * realTemplate
    * fakeTemplate
    * piZeroTemplate
    * matchQuality
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