
puWeight  = None
try:
    puWeight  = cms_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)

template_input_collection_sihih = "Nm1FiltsihihEB"
template_input_collection_chhadiso = "Nm1FiltchargedHadronIsoEB"

matched = 'genParticlesSize>0'

real = '\
(\
    genParticlesSize>0 \
    && (\
        (abs(energy - genParticle.energy) / genParticle.energy)^2 < 4 * ( \
            (3.63 / sqrt(genParticle.energy))^2 \
            + (.124 / genParticle.energy)^2 \
            + (0.3)^2 \
        )\
    )\
)'

piZero = '\
( \
    abs(genParticle.mother.pdgId) == 111 \
    || (\
        genParticle.mother.numberOfMothers > 0 \
        && \
        abs(genParticle.mother.mother.pdgId) == 111 \
    )\
)'

prompt = real + '&& !' + piZero


##################################################################### Sihih ###
# Filters
matchedPhotonsSihih = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(template_input_collection_sihih),
    cut = cms.string(matched),
    filter = cms.bool(False)
)
unmatchedPhotonsSihih = matchedPhotonsSihih.clone(
    cut = cms.string('!(' + matched + ')')
)
realPhotonsSihih = matchedPhotonsSihih.clone(
    cut = cms.string(prompt)
)
fakePhotonsSihih = matchedPhotonsSihih.clone(
    cut = cms.string('!(' + prompt + ')')
)
piZeroPhotonsSihih = matchedPhotonsSihih.clone(
    cut = cms.string(real + "&&" + piZero)
)

# Analyzers
matchQualitySihih = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("realPhotonsSihih"),
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

matchedTemplateSihih = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("matchedPhotonsSihih"),
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
if puWeight:
    matchedTemplateSihih.weights = puWeight
unmatchedTemplateSihih = matchedTemplateSihih.clone(
    src = cms.InputTag("unmatchedPhotonsSihih"),
)
realTemplateSihih = matchedTemplateSihih.clone(
    src = cms.InputTag("realPhotonsSihih"),
)
fakeTemplateSihih = matchedTemplateSihih.clone(
    src = cms.InputTag("fakePhotonsSihih"),
)
piZeroTemplateSihih = matchedTemplateSihih.clone(
    src = cms.InputTag("piZeroPhotonsSihih"),
)
templatePathSihih = cms.Path(
    matchedPhotonsSihih
    * unmatchedPhotonsSihih
    * realPhotonsSihih
    * fakePhotonsSihih
    * piZeroPhotonsSihih
    * matchQualitySihih
    * matchedTemplateSihih
    * unmatchedTemplateSihih
    * realTemplateSihih
    * fakeTemplateSihih
    * piZeroTemplateSihih
)

dataTemplateFitPhotonsSihih = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(template_input_collection_sihih),
    cut = cms.string("1<2"),
    filter = cms.bool(False)
)
dataTemplateFitHistoSihih = matchedTemplateSihih.clone(
    src = cms.InputTag("dataTemplateFitPhotonsSihih")
)

dataTemplatePathSihih = cms.Path(
    dataTemplateFitPhotonsSihih
    * dataTemplateFitHistoSihih
)

################################################################## ChHadIso ###
# Filters
matchedPhotonsChHadIso = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(template_input_collection_chhadiso),
    cut = cms.string(matched),
    filter = cms.bool(False)
)
unmatchedPhotonsChHadIso = matchedPhotonsChHadIso.clone(
    cut = cms.string('!(' + matched + ')')
)
realPhotonsChHadIso = matchedPhotonsChHadIso.clone(
    cut = cms.string(prompt)
)
fakePhotonsChHadIso = matchedPhotonsChHadIso.clone(
    cut = cms.string('!(' + prompt + ')')
)
piZeroPhotonsChHadIso = matchedPhotonsChHadIso.clone(
    cut = cms.string(real + "&&" + piZero)
)

# Analyzers
matchQualityChHadIso = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("realPhotonsChHadIso"),
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

matchedTemplateChHadIso = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("matchedPhotonsChHadIso"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(10.),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('ChHadIso'),
            description  = cms.untracked.string(';PF charged hadron isolation (#rho corrected);number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string("max(chargedHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_charged')), 0.)")
        ),
    )
)
if puWeight:
    matchedTemplateChHadIso.weights = puWeight
unmatchedTemplateChHadIso = matchedTemplateChHadIso.clone(
    src = cms.InputTag("unmatchedPhotonsChHadIso"),
)
realTemplateChHadIso = matchedTemplateChHadIso.clone(
    src = cms.InputTag("realPhotonsChHadIso"),
)
fakeTemplateChHadIso = matchedTemplateChHadIso.clone(
    src = cms.InputTag("fakePhotonsChHadIso"),
)
piZeroTemplateChHadIso = matchedTemplateChHadIso.clone(
    src = cms.InputTag("piZeroPhotonsChHadIso"),
)
templatePathChHadIso = cms.Path(
    matchedPhotonsChHadIso
    * unmatchedPhotonsChHadIso
    * realPhotonsChHadIso
    * fakePhotonsChHadIso
    * piZeroPhotonsChHadIso
    * matchQualityChHadIso
    * matchedTemplateChHadIso
    * unmatchedTemplateChHadIso
    * realTemplateChHadIso
    * fakeTemplateChHadIso
    * piZeroTemplateChHadIso
)

dataTemplateFitHistoChHadIso = matchedTemplateChHadIso.clone(
    src = cms.InputTag("dataTemplateFitPhotonsChHadIso")
)

dataTemplateFitPhotonsChHadIso = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(template_input_collection_chhadiso),
    cut = cms.string("1<2"),
    filter = cms.bool(False)
)

dataTemplatePathChHadIso = cms.Path(
    dataTemplateFitPhotonsChHadIso
    * dataTemplateFitHistoChHadIso
)