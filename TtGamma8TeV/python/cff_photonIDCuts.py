
puWeight  = None
try:
    puWeight  = cms_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)

################## cuts / histo defs
# example : (cut, low, high, n-bins, x-axis-label, plotquantity)

histo_pre = {
    "et" : (
        "", 0, 700, 140,
        "E_{T} / GeV",
        "et"
    ),
    "drmuon" : (
        "", 0.,5.,100,
        "#DeltaR(photon, muon)",
        'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'
    ),
    "drjet" : (
        "",0.,5.,100,
        "#DeltaR(photon, jet)",
        'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'
    ),
    "ptrelDrjet" : (
        "",0.,1.1,100,
        "E_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.15",
        '?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15)? pt / overlaps("jets")[0].pt: -0.01'
    ),
}

histo_post = {
    "et" : (
        "", 0, 700, 35,
        "E_{T} / GeV",
        "et"
    ),
    "eta" : (
        "", -4., 4., 40,
        "#eta",
        "eta"
    ),
    "drmuon" : (
        "",0.,5.,100,
        "#DeltaR(photon, muon)",
        'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'
    ),
    "drjet" : (
        "",0.,5.,100,
        "#DeltaR(photon, jet)",
        'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'
    ),
    "ptrelDrjet" : (
        "",0.,1.1,100,
        "E_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.15",
        '?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15)? pt / overlaps("jets")[0].pt: -0.01'
    ),
}

cuts = {
    #"drmuon" : ('deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi) > 0.3',0.,5.,100, "#DeltaR(photon, muon)",'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'),
    #"drjet" : ('deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) > 0.5 || deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15',0.,5.,100,"#DeltaR(photon, jet)", 'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'),
    #"ptrelDrjet" : ('deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15 && pt / overlaps("jets")[0].pt > 0.75',0.,1.1,100, "E_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.15", '?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.15)? pt / overlaps("jets")[0].pt: -0.01'),

# FIDUCIALIZATION / CONVENIENCE CUTS
    #"eta" : ("abs(eta)<1.4442 || 1.556<abs(eta)<2.5", -4, 4, 80, "#eta", "eta"),
    #"etaEE" : ("1.556<abs(eta)<2.5",-4, 4, 80, "#eta", "eta"),
    "etaEB" : (
        "abs(eta)<1.4442",
        -4, 4, 80,
        "#eta",
        "eta"
    ),
    "etcut" : (
        "et>15",
        0, 700, 140,
        "E_{T} / GeV",
        "et"
    ),

# ZE OFFICIAL PHOTON ID
    "passEleVeto" : (
        "userFloat('passEleVeto') > 0.5",
        -.5, 1.5, 2,
        "passes conv. ele. veto",
        "userFloat('passEleVeto')"
    ),
    "hadTowOverEm" : (
        "hadTowOverEm<0.05",
        0., 4., 80,
        "H/E",
        "hadTowOverEm"
    ),
    "sihihEB" : (
        "sigmaIetaIeta<0.011", # EE: 0.031
        0., 10., 80,
        "#sigma_{i #eta i #eta}",
        "sigmaIetaIeta"
    ),
    "chargedHadronIsoEB" : (
        "chargedHadronIso<0.7", # EE: 0.5
        0., 10., 80,
        "PF charged hadron isolation",
        "chargedHadronIso"
    ),
    "neutralHadronIsoEB" : (
        "neutralHadronIso<(0.4 + 0.04*pt)", # EE: 1.5 + 0.04*pt
        0., 10., 80,
        "PF neutral hadron isolation",
        "neutralHadronIso"
    ),
    "photonIsoEB" : (
        "photonIso<(0.5 + 0.005*pt)", # EE: 1.0 + 0.005*pt
        0., 10., 80,
        "PF photon isolation",
        "photonIso"
    ),

# TODO:
# ARE THE ISOLATIONS RHO CORRECTED BY PF2PAT??? NO!!
# PU !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# OVERLAP REMOVAL
# PLOTTING: *LEGEND *LOGSCALE
}

cut_key_order = [
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
]
num_cut_keys = len(cut_key_order)

all_cuts = ""
for key in cuts:
    all_cuts += cuts[key][0] + " && "
print "\nALL CUTS:\n" + str(all_cuts) + "\n\n"

def make_cutflow_token(cut):
    return (
        "", -.5, num_cut_keys + .5, num_cut_keys,
        cut,
        str(cut_key_order.index(cut) + 1) + "."
    )

def make_histo_analyzer(src, tokens):
    """tokens: (cut, low, high, n-bins, x-axis-label, plotquantity)"""
    histoAnalyzer = cms.EDAnalyzer(
        "CandViewHistoAnalyzer",
        src = cms.InputTag(src),
        histograms = cms.VPSet(
            cms.PSet(
                lazyParsing  = cms.untracked.bool(True),
                min          = cms.untracked.double(tokens[1]),
                max          = cms.untracked.double(tokens[2]),
                nbins        = cms.untracked.int32 (tokens[3]),
                name         = cms.untracked.string("histo"),
                description  = cms.untracked.string(
                    ";" + tokens[4] + ";Number of photons"
                ),
                plotquantity = cms.untracked.string(tokens[5]),
            )
        )
    )
    if puWeight:
        histoAnalyzer.weights = puWeight
    return histoAnalyzer

def add_photon_cuts(process):
    """Produces cutflow modules (incl. histograms). Returns new paths."""
    last_producer = "photonInputDummy"
    last_filter   = "photonInputDummy"
    new_paths = []

    # TODO: break this long sequence in smaller functions
    # cutflow bin zero: preselection
    cutflow_hist = make_histo_analyzer(
        last_filter, # put collection with exactly one item here
        ("",  -.5, num_cut_keys + .5, num_cut_keys, "preselected", "0.")
    )
    setattr(process, "CutFlowpreselected", cutflow_hist)
    last_filt_obj = getattr(process, last_filter)
    process.selectionPath.replace(last_filt_obj, last_filt_obj * cutflow_hist)

    #loop over cuts
    for cut_key in cut_key_order:

        # prepare the not_cut and cuts_minus_one string
        not_cut = cuts[cut_key][0]
        cuts_minus_one = all_cuts.replace(not_cut + " && ", "")
        cuts_minus_one = cuts_minus_one[:-4] # remove trailing &&
        print "NOT_CUT", not_cut
        #print "YES_CUT", cuts_minus_one

        # Filter for producerPath
        new_producer = "PhotonProducer" + cut_key
        PhotonProdTmp = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag(last_producer),
            cut = cms.string(not_cut),
            filter = cms.bool(False)
        )
        setattr(process, new_producer, PhotonProdTmp)
        last_prod_obj = getattr(process, last_producer)

        # Before Cut: Control Plot for cut on actual distribution
        CrtlPlotTmp = make_histo_analyzer(last_producer, cuts[cut_key])
        setattr(process, "CrtlFilt" + cut_key, CrtlPlotTmp)
        process.producerPath.replace(last_prod_obj, last_prod_obj * CrtlPlotTmp * PhotonProdTmp)

        # Filter for selectionPath
        new_filter   = "PhotonFilt" + cut_key
        PhotonFiltTmp = cms.EDFilter(
            "PATCandViewCountFilter",
            src = cms.InputTag(new_producer),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(9999)
        )
        setattr(process, new_filter, PhotonFiltTmp)
        last_filt_obj = getattr(process, last_filter)

        process.selectionPath.replace(last_filt_obj, last_filt_obj * PhotonFiltTmp)

        # After Cut: Histogram for cutflow
        cutflow_hist = make_histo_analyzer(
            new_filter,
            make_cutflow_token(cut_key)
        )
        setattr(process, "CutFlow" + cut_key, cutflow_hist)
        process.selectionPath.replace(PhotonFiltTmp, PhotonFiltTmp * cutflow_hist)

        # Filter for n - 1 plot
        PhotonFiltersMinusTmp = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonInputDummy"),
            cut = cms.string(cuts_minus_one),
            filter = cms.bool(False)
        )
        setattr(process, "PhotonFiltersMinus" + cut_key, PhotonFiltersMinusTmp)

        # n - 1 Plot
        PhotonAnaTmp = make_histo_analyzer("PhotonFiltersMinus" + cut_key, cuts[cut_key])
        setattr(process, "PhotonAna" + cut_key, PhotonAnaTmp)

        pathTmp = cms.Path(
            process.preSel
            * getattr(process, "PhotonFiltersMinus" + cut_key)
            * getattr(process, "PhotonAna" + cut_key)
        )
        setattr(process, "path"+cut_key, pathTmp)
        new_paths.append(pathTmp)

        #set for next round
        last_producer = new_producer
        last_filter   = new_filter

    return new_paths

