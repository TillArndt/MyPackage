

puWeight    = None
try:
    puWeight  = cms_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)


matched = 'genParticlesSize>0'

real_with_ECAL_cut = '\
(\
    genParticlesSize > 0 \
    && (\
        (abs(energy - genParticle.energy) / genParticle.energy)^2 < 4 * ( \
            (3.63 / sqrt(genParticle.energy))^2 \
            + (.124 / genParticle.energy)^2 \
            + (0.3)^2 \
        )\
    )\
)'

real = '\
(\
    genParticlesSize > 0 \
    && (\
        (abs(energy - genParticle.energy) / genParticle.energy) < 2. \
    ) && (\
        deltaR(eta, phi, genParticle.eta, genParticle.phi) < 0.2 \
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

#prompt = real + '&& !' + piZero
largestId = 'userFloat("largestAncestorPdgId")'
prompt = largestId + ' > 0.5 && 24.5 > ' + largestId + ' && ' + real


##################################################################### Sihih ###
template_input_collection_sihih = "Nm1FiltsihihEB"

# Take only one photon per event (photons are pt-ordered)
firstPhotonForSihih = cms.EDProducer("FirstPhotonPicker",
    src = cms.InputTag(template_input_collection_sihih)
)
template_input_collection_sihih = "firstPhotonForSihih"

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
            max          = cms.untracked.double(0.03),
            nbins        = cms.untracked.int32 (30),
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
    firstPhotonForSihih
    * matchedPhotonsSihih
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
    cut = cms.string(""),
    filter = cms.bool(False)
)
dataTemplateFitHistoSihih = matchedTemplateSihih.clone(
    src = cms.InputTag("dataTemplateFitPhotonsSihih")
)

dataTemplatePathSihih = cms.Path(
    firstPhotonForSihih
    * dataTemplateFitPhotonsSihih
    * dataTemplateFitHistoSihih
)

############################### path for sihih shift histograms ###

import MyPackage.TtGamma8TeV.cff_photonIDCuts as pho_cuts
def add_sihih_shifted_histos(process):
    process.sihihShiftPath = cms.Path()
    cut_token = pho_cuts.cuts["sihihEB"]
    for shift_int in xrange(900, 1050, 2):

        # prepare tokens 
        shift           = (shift_int - 1000) * 0.00001
        shift_id        = "TemplateSihihShift%04d" % shift_int
        shift_cut       = list(cut_token)
        shift_cut[4]    = ("%.5f + " % shift) + shift_cut[4]
        shift_cut[5]    = ("%.5f + " % shift) + shift_cut[5]

        # n - 1 Plot takes input from existing n-1 filter
        real_tmplt = pho_cuts.make_histo_analyzer("realPhotonsSihih", shift_cut)
        fake_tmplt = pho_cuts.make_histo_analyzer("fakePhotonsSihih", shift_cut)

        # add to process and to path
        setattr(process, "real" + shift_id, real_tmplt)
        setattr(process, "fake" + shift_id, fake_tmplt)
        process.sihihShiftPath *= real_tmplt
        process.sihihShiftPath *= fake_tmplt


################################################################## ChHadIso ###
template_input_collection_chhadiso = "Nm1FiltchargedHadronIsoEB"

# Take only one photon per event (photons are pt-ordered)
firstPhotonForChHadIso = cms.EDProducer("FirstPhotonPicker",
    src = cms.InputTag(template_input_collection_chhadiso)
)
template_input_collection_chhadiso = "firstPhotonForChHadIso"

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
            nbins        = cms.untracked.int32 (40),
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
    firstPhotonForChHadIso
    * matchedPhotonsChHadIso
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

dataTemplateFitPhotonsChHadIso = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(template_input_collection_chhadiso),
    cut = cms.string(""),
    filter = cms.bool(False)
)
dataTemplateFitHistoChHadIso = matchedTemplateChHadIso.clone(
    src = cms.InputTag("dataTemplateFitPhotonsChHadIso")
)

dataTemplatePathChHadIso = cms.Path(
    firstPhotonForChHadIso
    * dataTemplateFitPhotonsChHadIso
    * dataTemplateFitHistoChHadIso
)
