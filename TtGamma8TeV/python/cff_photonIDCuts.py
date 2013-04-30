
puWeight  = None
try:
    puWeight  = cms_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)
################## n-1 Cuts

# examplecut : ("cut",min,max,nbins,"name","description", lazyparsing,"plotquantity")

cuts = {

# PRE AND POST HISTOS
    "PREet" : ("1<2", 0, 700, 140, "E_{T} / GeV", "et"),
    "PREdrmuon" : ('1<2',0.,5.,100, "#DeltaR(photon, muon)",'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'),
    "PREdrjet" : ('1<2',0.,5.,100, "#DeltaR(photon, jet)", 'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'),
    "PREptrelDrjet" : ('1<2',0.,1.1,100, "E_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.15", '?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15)? pt / overlaps("jets")[0].pt: -0.01'),
    "POSTet" : ("1<2", 0, 700, 35, "E_{T} / GeV", "et"),
    "POSTeta" : ("1<2", -4., 4., 40, "#eta", "eta"),
    "POSTdrmuon" : ('1<2',0.,5.,100, "#DeltaR(photon, muon)",'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'),
    "POSTdrjet" : ('1<2',0.,5.,100, "#DeltaR(photon, jet)", 'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'),
    "POSTptrelDrjet" : ('1<2',0.,1.1,100, "E_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.15", '?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15)? pt / overlaps("jets")[0].pt: -0.01'),
    #"drmuon" : ('deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi) > 0.3',0.,5.,100, "#DeltaR(photon, muon)",'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'),
    #"drjet" : ('deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) > 0.5 || deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15',0.,5.,100,"#DeltaR(photon, jet)", 'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'),
    #"ptrelDrjet" : ('deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15 && pt / overlaps("jets")[0].pt > 0.75',0.,1.1,100, "E_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.15", '?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15)? pt / overlaps("jets")[0].pt: -0.01'),

# FIDUCIALIZATION / CONVENIENCE CUTS
    "eta" : ("abs(eta)<1.4442 || 1.556<abs(eta)<2.5", -4, 4, 80, "#eta", "eta"),
    "etaEB" : ("abs(eta)<1.4442", -4, 4, 80, "#eta", "eta"),
    "etaEE" : ("1.556<abs(eta)<2.5",-4, 4, 80, "#eta", "eta"),
    "etcut" : ("et>15", 0, 700, 140, "E_{T} / GeV", "et"),

# ZE OFFICIAL PHOTON ID
    "passEleVeto" : ("userFloat('passEleVeto') > 0.5", -.5, 1.5, 2, "passes conv. ele. veto", "userFloat('passEleVeto')"),
    "hadTowOverEm" : ("hadTowOverEm<0.05", 0., 4., 80, "H/E", "hadTowOverEm"),
    "sihihEB" : ("sigmaIetaIeta<0.011", 0., 10., 80, "#sigma_{i #eta i #eta}", "sigmaIetaIeta"), # EE: 0.031
    "chargedHadronIsoEB" : ("chargedHadronIso<0.7", 0., 10., 80, "PF charged hadron isolation", "chargedHadronIso"), # EE: 0.5
    "neutralHadronIsoEB" : ("neutralHadronIso<(0.4 + 0.04*pt)", 0., 10., 80, "PF neutral hadron isolation", "neutralHadronIso"), # EE: 1.5 + 0.04*pt
    "photonIsoEB" : ("photonIso<(0.5 + 0.005*pt)", 0., 10., 80, "PF photon isolation", "photonIso"), # EE: 1.0 + 0.005*pt

# ARE THE ISOLATIONS RHO CORRECTED BY PF2PAT??? NO!!
# PU !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# OVERLAP REMOVAL
# PLOTTING: *LEGEND *LOGSCALE
    }

cut_key_list = [
    "PREet",
    "PREdrmuon",
    "PREdrjet",
    "PREptrelDrjet",
    "etaEB",
    "etcut",
    #"drmuon",
    #"drjet",
    #"ptrelDrjet",
    #"passEleVeto",
    "hadTowOverEm",
    "sihihEB",
    "chargedHadronIsoEB",
    "neutralHadronIsoEB",
    "photonIsoEB",
    "POSTet",
    "POSTeta",
    "POSTdrmuon",
    "POSTdrjet",
    "POSTptrelDrjet",
    ]
all_cuts = ""
for key in cuts:
    all_cuts += cuts[key][0] + " && "
print "\nALL CUTS:\n" + str(all_cuts) + "\n\n"

def make_plot(src, key):
    histoAnalyzer=cms.EDAnalyzer(
        "CandViewHistoAnalyzer",
        src = cms.InputTag(src),
        histograms = cms.VPSet(
            cms.PSet(
                min          = cms.untracked.double(cuts[key][1]),
                max          = cms.untracked.double(cuts[key][2]),
                nbins        = cms.untracked.int32 (cuts[key][3]),
                name         = cms.untracked.string("histo"),
                description  = cms.untracked.string(";" + cuts[key][4] + ";Number of photons"),
                lazyParsing  = cms.untracked.bool(True),
                plotquantity = cms.untracked.string(cuts[key][5])
            )
        )
    )
    if puWeight:
        histoAnalyzer.weights = puWeight
    return histoAnalyzer

def add_photon_cuts(process):

    last_producer = "photonInputDummy"
    last_filter   = "photonInputDummy"
    new_paths = []
    for key in cut_key_list:

        # prepare the not_cut and cuts_minus_one string
        not_cut = cuts[key][0]
        cuts_minus_one = all_cuts.replace(not_cut + " && ", "")
        cuts_minus_one = cuts_minus_one[:-4] # remove trailing &&
        print "NOT_CUT", not_cut
        #print "YES_CUT", cuts_minus_one

        # Filter for producerPath
        new_producer = "PhotonProducer" + key
        PhotonProdTmp = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag(last_producer),
            cut = cms.string(not_cut),
            filter = cms.bool(False)
        )
        setattr(process, new_producer, PhotonProdTmp)
        last_prod_obj = getattr(process, last_producer)

        # Control Plot for cut on actual distribution
        CrtlPlotTmp = make_plot(last_producer, key)
        setattr(process, "CrtlFilt" + key, CrtlPlotTmp)
        process.producerPath.replace(last_prod_obj, last_prod_obj * CrtlPlotTmp * PhotonProdTmp)

        # Filter for selectionPath
        new_filter   = "PhotonFilt" + key
        PhotonFiltTmp = cms.EDFilter(
            "PATCandViewCountFilter",
            src = cms.InputTag(new_producer),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(9999)
        )
        setattr(process, new_filter, PhotonFiltTmp)
        last_filt_obj = getattr(process, last_filter)

        process.selectionPath.replace(last_filt_obj, last_filt_obj * PhotonFiltTmp)

        # Filter for n - 1 plot
        PhotonFiltersMinusTmp = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonInputDummy"),
            cut = cms.string(cuts_minus_one),
            filter = cms.bool(False)
        )
        setattr(process, "PhotonFiltersMinus" + key, PhotonFiltersMinusTmp)

        # n - 1 Plot
        PhotonAnaTmp = make_plot("PhotonFiltersMinus" + key, key)
        setattr(process, "PhotonAna" + key, PhotonAnaTmp)

        pathTmp = cms.Path(
            process.preSel
            * getattr(process, "PhotonFiltersMinus" + key)
            * getattr(process, "PhotonAna" + key)
        )
        setattr(process, "path"+key, pathTmp)
        new_paths.append(pathTmp)

        #set for next round
        last_producer = new_producer
        last_filter   = new_filter


    return new_paths

