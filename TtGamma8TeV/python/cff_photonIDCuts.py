
runOnMC     = True
puWeight    = None
etCutValue  = 25.
try:
    runOnMC     = not cms_var["is_data"]
    puWeight    = cms_var.get("puWeight", puWeight)
    etCutValue  = cms_var.get("etCutValue", etCutValue)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)

################## cuts / histo defs
# example : (cut, low, high, n-bins, x-axis-label, plotquantity)

histo_pre = {
    "et" : (
        "", 0., 700., 140,
        "E_{T} / GeV",
        "et"
    ),
    "drmuon" : (
        "", 0.,5.,50,
        "#DeltaR(photon, muon)",
        'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'
    ),
    "drjet" : (
        "",0.,5.,50,
        "#DeltaR(photon, jet)",
        'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'
    ),
}

histo_post = {
    "et" : (
        "", 0., 700., 70,
        "E_{T} / GeV",
        "et"
    ),
    "eta" : (
        "", -2., 2., 40,
        "#eta",
        "eta"
    ),
    "drmuon" : (
        "",0.,5.,50,
        "#DeltaR(photon, muon)",
        'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'
    ),
    "drjet" : (
        "",0.,5.,50,
        "#DeltaR(photon, jet)",
        'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'
    ),
    "scaleFactor" : (
        "", -700., 700., 140,
        "E_{T} / GeV",
        "?(abs(eta) < 0.8) ? -et : et"
    ),
}

cuts = {
    "drmuon" : (
        'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi) > 0.7'
        ,0.,5.,50,
        "#DeltaR(photon, muon)",
        'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'
    ),
    "drjet" : (
        'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) > 0.7 || deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.3',
        0.,5.,50,
        "#DeltaR(photon, jet)",
        'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'
    ),

# FIDUCIALIZATION / CONVENIENCE CUTS
    #"eta" : ("abs(eta)<1.4442 || 1.556<abs(eta)<2.5", -4, 4, 80, "#eta", "eta"),
    #"etaEE" : ("1.556<abs(eta)<2.5",-4, 4, 80, "#eta", "eta"),
    "etaEB" : (
        "abs(eta)<1.4442",
        -4., 4., 80,
        "#eta",
        "eta"
    ),
    "etcut" : (
        "et>"+str(etCutValue),
        0., 700., 70,
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
        0., 1., 20,
        "H/E",
        "hadTowOverEm"
    ),
    "sihihEB" : (
        "sigmaIetaIeta<0.011", # EE: 0.031
        0., 0.03, 30,
        "#sigma_{i #eta i #eta}",
        "sigmaIetaIeta"
    ),
    "chargedHadronIsoEB" : (
        "max(chargedHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_charged')), 0.) < 0.7", # EE: 0.5
        0., 10., 40,
        "PF charged hadron isolation (#rho corrected) / GeV",
        "max(chargedHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_charged')), 0.)"
    ),
    "neutralHadronIsoEB" : (
        "max(neutralHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_neutral')), 0.) < (0.4 + 0.04*pt)", # EE: 1.5 + 0.04*pt
        0., 10., 40,
        "PF neutral hadron isolation (#rho corrected) / GeV",
        "max(neutralHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_neutral')), 0.)"
    ),
    "photonIsoEB" : (
        "max(photonIso - (userFloat('kt6pf_rho')*userFloat('EA_photons')), 0.) < (0.5 + 0.005*pt)", # EE: 1.0 + 0.005*pt
        0., 10., 40,
        "PF photon isolation (#rho corrected) / GeV",
        "max(photonIso - (userFloat('kt6pf_rho')*userFloat('EA_photons')), 0.)"
    ),
}

def loose_deno_cuts(lower_cut_with_sieie = True):
    """Implementation of cutstrings for loose deno id"""
    hoe             = "hadTowOverEm"
    sieie           = "sigmaIetaIeta"
    pfchargedIso    = "max(chargedHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_charged')), 0.)"
    pfneutralIso    = "max(neutralHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_neutral')), 0.)"
    pfphoIso        = "max(photonIso - (userFloat('kt6pf_rho')*userFloat('EA_photons')), 0.)"

    cuthoe          = "0.05"
    cutsieie        = "0.012"
    cutchargedIso   = "4.0"
    cutneutralIso   = "(4.5 + 0.04*pt)"
    cutphoIso       = "(4.5 + 0.005*pt)"

    maxchargedIso   = "min(0.2*et, 5*" + cutchargedIso  + ")"
    maxneutralIso   = "min(0.2*et, 5*" + cutneutralIso  + ")"
    maxphoIso       = "min(0.2*et, 5*" + cutphoIso      + ")"
    maxhoe          = cuthoe

    lower_cut = (
        "( "       + pfchargedIso + ">" + cutchargedIso
        + ") || (" + pfneutralIso + ">" + cutneutralIso
        + ") || (" + pfphoIso     + ">" + cutphoIso
        + ")"
        )
    if lower_cut_with_sieie:
        lower_cut += " || (" + sieie + ">" + cutsieie + ")"
    upper_cut = (
        "( "       + pfchargedIso + "<" + maxchargedIso
        + ") && (" + pfneutralIso + "<" + maxneutralIso
        + ") && (" + pfphoIso     + "<" + maxphoIso
        + ") && (" + hoe          + "<" + maxhoe
        + ")"
        )
    return lower_cut, upper_cut

cut_key_order = [
    "etcut",
    "etaEB",
    "passEleVeto",
    "hadTowOverEm",
    "sihihEB",
    "chargedHadronIsoEB",
    "neutralHadronIsoEB",
    "photonIsoEB",
    "drmuon",
    "drjet",
    ]
num_cut_keys = len(cut_key_order)

all_cuts = ""
for key in cuts:
    all_cuts += cuts[key][0] + " && "
print "\nApplied Photon Cuts (in order): \n"+"\n".join(cut_key_order)+"\n\n"
#TODO: print cuts to, in a table, not only keys

def make_cutflow_token(cut):
    if cut in cut_key_order:
        bin = str(cut_key_order.index(cut) + 1) + "."
    else:
        bin = "0."
    return "", -.5, num_cut_keys + .5, num_cut_keys + 1, cut, bin

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
                    ";" + tokens[4] + ";number of photons"
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
    pre_paths = []
    post_paths = []

    # TODO: break this long sequence in smaller functions

    # CUTFLOW: use a one-object-collection as input for cutflow histo.
    one_obj_collection = "tightmuons"  ## HACK-AROUND: the tightmuons collection has always exactly one muon for ttbar-selected events.
    CheckOneObj = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(one_obj_collection),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(1),
    )
    setattr(process, "CheckOneObj", CheckOneObj)
    process.producerPath.insert(0,CheckOneObj)

    # cutflow bin zero: preselection
    cutflow_hist = make_histo_analyzer(
        one_obj_collection, # put collection with exactly one item here
        make_cutflow_token("preselected")
    )
    setattr(process, "CutFlowpreselected", cutflow_hist)
    last_filt_obj = getattr(process, last_filter)
    process.selectionPath.replace(last_filt_obj, cutflow_hist * last_filt_obj)

    # pre_histos
    for cut_key, tokens in histo_pre.iteritems():
        new_filter   = "CrtlPlotPre" + cut_key
        new_filter_obj = make_histo_analyzer(last_producer, tokens)
        setattr(process, new_filter, new_filter_obj)
        last_filt_obj = getattr(process, last_filter)
        process.selectionPath.replace(
            last_filt_obj,
            last_filt_obj * new_filter_obj
        )
        last_filter   = new_filter

    # photon cuts
    for cut_key in cut_key_order:

        ###################################################### producerPath ###
        new_producer = "PhotonProducer" + cut_key
        PhotonProdTmp = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag(last_producer),
            cut = cms.string(cuts[cut_key][0]),
            filter = cms.bool(False)
        )
        setattr(process, new_producer, PhotonProdTmp)
        last_prod_obj = getattr(process, last_producer)

        # add to path
        process.producerPath.replace(
            last_prod_obj,
            last_prod_obj * PhotonProdTmp
        )

        ##################################################### selectionPath ###
        # Before Cut: Control Plot for cut on actual distribution
        CrtlPlotTmp = make_histo_analyzer(last_producer, cuts[cut_key])
        setattr(process, "CrtlPlotInter" + cut_key, CrtlPlotTmp)

        # Filter for selectionPath
        new_filter   = "PhotonFilt" + cut_key
        new_cutflow_histo = "CutFlow" + cut_key
        PhotonFiltTmp = cms.EDFilter(
            "PATCandViewCountFilter",
            src = cms.InputTag(new_producer),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(9999)
        )
        setattr(process, new_filter, PhotonFiltTmp)
        last_filt_obj = getattr(process, last_filter)

        # After Cut: Histogram for cutflow
        cutflow_hist = make_histo_analyzer(
            one_obj_collection,
            make_cutflow_token(cut_key)
        )
        setattr(process, new_cutflow_histo, cutflow_hist)

        # add to path
        process.selectionPath.replace(
            last_filt_obj,
            last_filt_obj * CrtlPlotTmp * PhotonFiltTmp * cutflow_hist
        )

        #set for next round
        last_producer = new_producer
        last_filter   = new_cutflow_histo

    # post_histos
    for cut_key, tokens in histo_post.iteritems():
        new_filter   = "CrtlPlotPost" + cut_key
        new_filter_obj = make_histo_analyzer(last_producer, tokens)
        setattr(process, new_filter, new_filter_obj)
        last_filt_obj = getattr(process, last_filter)
        process.selectionPath.replace(
            last_filt_obj,
            last_filt_obj * new_filter_obj
        )
        last_filter   = new_filter

    ################################################### paths for n-1 plots ###
    for cut_key in cut_key_order:

        # make one cut string for the N-1 plots
        cutkeys_Nm1 = cut_key_order[:]
        cutkeys_Nm1.remove(cut_key)
        cuts_Nm1_list = list(cuts[cutkey][0] for cutkey in cutkeys_Nm1)
        cuts_Nm1_str = "( " + ") && (".join(cuts_Nm1_list) + " )"

        # Filter for n - 1 plot
        Nm1Filt = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonInputDummy"),
            cut = cms.string(cuts_Nm1_str),
            filter = cms.bool(False)
        )

        # n - 1 Plot
        Nm1Plot = make_histo_analyzer("Nm1Filt" + cut_key, cuts[cut_key])

        # Filter for n - 1 plot
        Nm1FiltBlocking = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonInputDummy"),
            cut = cms.string(cuts_Nm1_str),
            filter = cms.bool(True)
        )

        # post filter counter
        Nm1CountPost = cms.EDProducer("WeightedEventCountProducer")
        Nm1CountPostPrnt = cms.EDAnalyzer("WeightedEventCountPrinter",
            src = cms.InputTag("Nm1CountPost" + cut_key)
        )

        if puWeight:
            Nm1CountPost.weights    = puWeight

        # add to process
        setattr(process, "Nm1Filt" + cut_key, Nm1Filt)
        setattr(process, "Nm1Plot" + cut_key, Nm1Plot)
        setattr(process, "Nm1FiltBlocking" + cut_key, Nm1FiltBlocking)
        setattr(process, "Nm1CountPost" + cut_key, Nm1CountPost)
        setattr(process, "Nm1CountPostPrint" + cut_key, Nm1CountPostPrnt)

        # make path
        pathTmp = cms.Path(
            process.preSel
            * getattr(process, "Nm1Filt" + cut_key)
            * getattr(process, "Nm1Plot" + cut_key)
            * getattr(process, "Nm1FiltBlocking" + cut_key)
            * getattr(process, "Nm1CountPost" + cut_key)
            * getattr(process, "Nm1CountPostPrint" + cut_key)
        )
        setattr(process, "path"+cut_key, pathTmp)
        post_paths.append(pathTmp)

    ############################## input counter and counter after fid cuts ###
    # fiducialization cuts filter
    cuts_fid_list = list(cuts[cutkey][0] for cutkey in ["etcut", "etaEB",])
    cuts_fid_str = "( " + ") && (".join(cuts_fid_list) + " )"
    process.FidFiltBlocking = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut = cms.string(cuts_fid_str),
        filter = cms.bool(True)
    )

    # pre and post counters
    process.FidCountPre = cms.EDProducer("WeightedEventCountProducer")
    process.FidCountPost = cms.EDProducer("WeightedEventCountProducer")
    if puWeight:
        process.FidCountPre.weights     = puWeight
        process.FidCountPost.weights    = puWeight

    # ... and printers
    process.FidCountPrePrnt = cms.EDAnalyzer("WeightedEventCountPrinter",
        src = cms.InputTag("FidCountPre")
    )
    process.FidCountPostPrnt = cms.EDAnalyzer("WeightedEventCountPrinter",
        src = cms.InputTag("FidCountPost")
    )

    # path
    process.pathFidCount = cms.Path(
        process.preSel
        * process.FidCountPre
        * process.FidFiltBlocking
        * process.FidCountPost
        * process.FidCountPrePrnt
        * process.FidCountPostPrnt
    )
    post_paths.append(process.pathFidCount)

    ############################################## shilpi's loose id events ###

    # Blocking Filter for only complete tight ID events
    process.FullTightIDBlocking = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("Nm1FiltsihihEB"),
        cut = cms.string(cuts["sihihEB"][0]),
        filter = cms.bool(True)
    )

    # Filters for lower and upper cut
    lower_cut, upper_cut = loose_deno_cuts()
    process.LooseIDlower = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut = cms.string(lower_cut),
        filter = cms.bool(False)
    )
    process.LooseIDupper = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("LooseIDlower"),
        cut = cms.string(upper_cut),
        filter = cms.bool(False)
    )

    # Shilpi's Weight function
    process.ShilpiWeight = cms.EDProducer("ShilpiWeight",
        src = cms.InputTag("LooseIDupper"),
        weights = puWeight,
    )

    # tight id counter and printer
    process.FullTightIDCount = cms.EDProducer("WeightedEventCountProducer")
    if puWeight:
        process.FullTightIDCount.weights = puWeight
    process.FullTightIDCountPrnt = cms.EDAnalyzer("WeightedEventCountPrinter",
        src = cms.InputTag("FullTightIDCount")
    )

    process.pathLooseID = cms.Path(
        process.preSel
        * process.FullTightIDBlocking
        * process.FullTightIDCount
        * process.LooseIDlower
        * process.LooseIDupper
        * process.ShilpiWeight
        * process.FullTightIDCountPrnt
    )
    post_paths.append(process.pathLooseID)

    return pre_paths, post_paths
