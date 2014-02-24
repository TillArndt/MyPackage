

runOnMC     = True
try:
    runOnMC     = not cms_var["is_data"]
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms
import MyPackage.TtGamma8TeV.cff_photonIDCuts as pho_cuts

#################################################### definition of mc truth ###

stat1phot = "genParticlesSize > 0 && abs(genParticle.pdgId) == 22 && genParticle.status == 1"
largestId = 'userFloat("largestAncestorPdgId")'
prompt      = stat1phot+" && "+largestId+' > 0.5 && 24.5 > '+largestId
real        = prompt
fake        = '!('+prompt+')'
fakeGamma   = stat1phot+" && "+fake
fakeOther   = "!("+stat1phot+")"


########################################################### sihih histogram ###
_template_input_collection = "Nm1FiltsihihEB"

# Take only one photon per event (photons are pt-ordered)
firstPhotonForSihih = cms.EDProducer("FirstPhotonPicker",
    src = cms.InputTag(_template_input_collection)
)
_template_input_collection = "firstPhotonForSihih"

PhotonsSihih = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(_template_input_collection),
    cut = cms.string(""),
    filter = cms.bool(False)
)

TemplateSihih = pho_cuts.make_histo_analyzer(
    "PhotonsSihih",
    pho_cuts.cuts["sihihEB"]
)

TemplatePathSihih = cms.Path(
    firstPhotonForSihih
    * PhotonsSihih
    * TemplateSihih
)


################################################# sihih templates (only mc) ###

# Filters
PhotonsSihihreal = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(_template_input_collection),
    cut = cms.string(real),
    filter = cms.bool(False)
)
PhotonsSihihfake = PhotonsSihihreal.clone(
    cut = cms.string(fake)
)
PhotonsSihihfakeGamma = PhotonsSihihreal.clone(
    cut = cms.string(fakeGamma)
)
PhotonsSihihfakeOther = PhotonsSihihreal.clone(
    cut = cms.string(fakeOther)
)

# Analyzers
matchQualitySihih = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("PhotonsSihihreal"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(0.02),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('deltaR'),
            description  = cms.untracked.string(';#DeltaR(#gamma_{reco},#gamma_{gen});Number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('deltaR(eta, phi, genParticle.eta, genParticle.phi)')
        ),
        cms.PSet(
            min          = cms.untracked.double(-0.2),
            max          = cms.untracked.double(0.2),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('deltaErel'),
            description  = cms.untracked.string(';(E_{#gamma,reco} - E_{#gamma,gen}) / E_{#gamma,gen};Number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('(energy - genParticle.energy) / genParticle.energy')
        ),
    )
)

TemplateSihihreal = TemplateSihih.clone(
    src = cms.InputTag("PhotonsSihihreal"),
)
TemplateSihihfake = TemplateSihih.clone(
    src = cms.InputTag("PhotonsSihihfake"),
)
TemplateSihihfakeGamma = TemplateSihih.clone(
    src = cms.InputTag("PhotonsSihihfakeGamma"),
)
TemplateSihihfakeOther = TemplateSihih.clone(
    src = cms.InputTag("PhotonsSihihfakeOther"),
)
TemplateSequenceSihihTruth = cms.Sequence(
    firstPhotonForSihih
    * PhotonsSihihreal
    * PhotonsSihihfake
    * PhotonsSihihfakeGamma
    * PhotonsSihihfakeOther
    * matchQualitySihih
    * TemplateSihihreal
    * TemplateSihihfake
    * TemplateSihihfakeGamma
    * TemplateSihihfakeOther
)
if runOnMC:
    TemplatePathSihih *= TemplateSequenceSihihTruth


########################################### path for sihih shift histograms ###
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
        real_tmplt      = pho_cuts.make_histo_analyzer("PhotonsSihihreal", shift_cut)
        fake_tmplt      = pho_cuts.make_histo_analyzer("PhotonsSihihfake", shift_cut)
        fakeGamma_tmplt = pho_cuts.make_histo_analyzer("PhotonsSihihfakeGamma", shift_cut)

        # add to process and to path
        setattr(process, shift_id+"real",       real_tmplt)
        setattr(process, shift_id+"fake",       fake_tmplt)
        setattr(process, shift_id+"fakeGamma",  fakeGamma_tmplt)
        process.sihihShiftPath *= real_tmplt
        process.sihihShiftPath *= fake_tmplt
        process.sihihShiftPath *= fakeGamma_tmplt


######################################################## chhadiso histogram ###
_template_input_collection = "Nm1FiltchargedHadronIsoEB"

# Take only one photon per event (photons are pt-ordered)
firstPhotonForChHadIso = cms.EDProducer("FirstPhotonPicker",
    src = cms.InputTag(_template_input_collection)
)
_template_input_collection = "firstPhotonForChHadIso"

PhotonsChHadIso = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(_template_input_collection),
    cut = cms.string(""),
    filter = cms.bool(False)
)

TemplateChHadIso = pho_cuts.make_histo_analyzer(
    "PhotonsChHadIso",
    pho_cuts.cuts["chargedisoSCFootRmEB"]
)

TemplatePathChHadIso = cms.Path(
    firstPhotonForChHadIso
    * PhotonsChHadIso
    * TemplateChHadIso
)


############################################## chhadiso templates (only mc) ###

# Filters
PhotonsChHadIsoreal = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag(_template_input_collection),
    cut = cms.string(real),
    filter = cms.bool(False)
)
PhotonsChHadIsofake = PhotonsChHadIsoreal.clone(
    cut = cms.string(fake)
)
PhotonsChHadIsofakeGamma = PhotonsChHadIsoreal.clone(
    cut = cms.string(fakeGamma)
)
PhotonsChHadIsofakeOther = PhotonsChHadIsoreal.clone(
    cut = cms.string(fakeOther)
)

# Analyzers
matchQualityChHadIso = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("PhotonsChHadIsoreal"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(0.02),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('deltaR'),
            description  = cms.untracked.string(';#DeltaR(#gamma_{reco},#gamma_{gen});Number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('deltaR(eta, phi, genParticle.eta, genParticle.phi)')
        ),
        cms.PSet(
            min          = cms.untracked.double(-0.2),
            max          = cms.untracked.double(0.2),
            nbins        = cms.untracked.int32 (80),
            name         = cms.untracked.string('deltaErel'),
            description  = cms.untracked.string(';(E_{#gamma,reco} - E_{#gamma,gen}) / E_{#gamma,gen};Number of photons'),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string('(energy - genParticle.energy) / genParticle.energy')
        ),
    )
)

TemplateChHadIsoreal = TemplateChHadIso.clone(
    src = cms.InputTag("PhotonsChHadIsoreal"),
)
TemplateChHadIsofake = TemplateChHadIso.clone(
    src = cms.InputTag("PhotonsChHadIsofake"),
)
TemplateChHadIsofakeGamma = TemplateChHadIso.clone(
    src = cms.InputTag("PhotonsChHadIsofakeGamma"),
)
TemplateChHadIsofakeOther = TemplateChHadIso.clone(
    src = cms.InputTag("PhotonsChHadIsofakeOther"),
)
TemplateSequenceChHadIsoTruth = cms.Sequence(
    firstPhotonForChHadIso
    * PhotonsChHadIsoreal
    * PhotonsChHadIsofake
    * PhotonsChHadIsofakeGamma
    * PhotonsChHadIsofakeOther
    * matchQualityChHadIso
    * TemplateChHadIsoreal
    * TemplateChHadIsofake
    * TemplateChHadIsofakeGamma
    * TemplateChHadIsofakeOther
)
if runOnMC:
    TemplatePathChHadIso *= TemplateSequenceChHadIsoTruth

