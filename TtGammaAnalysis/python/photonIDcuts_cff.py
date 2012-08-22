
import FWCore.ParameterSet.Config as cms

################## n-1 Cuts

# examplecut : ("cut",min,max,nbins,"name","description", lazyparsing,"plotquantity")

cuts = {
    "drjet" : ('deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) > 0.5',0.,5.,100,"deltaRjet", ";#DeltaR(photon, jet);Number of photons", 1,'deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)'),
    "ptrelDrjet02" : ('1.<2.',0.,1.1,100,"ptreldeltaRjet05", ";p_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.02;Number of photons", 1,'?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.02)? pt / overlaps("jets")[0].pt: -0.01'),
    "ptrelDrjet10" : ('1.<2.',0.,1.1,100,"ptreldeltaRjet05", ";p_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.1;Number of photons", 1,'?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.10)? pt / overlaps("jets")[0].pt: -0.01'),
    "ptrelDrjet30" : ('1.<2.',0.,1.1,100,"ptreldeltaRjet05", ";p_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 0.3;Number of photons", 1,'?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 0.30)? pt / overlaps("jets")[0].pt: -0.01'),
    "ptrelDrjet99" : ('1.<2.',0.,1.1,100,"ptreldeltaRjet05", ";p_{T,photon} / p_{T,jet} for #DeltaR(photon, jet) < 5.0;Number of photons", 1,'?(deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) < 5.)? pt / overlaps("jets")[0].pt: -0.01'),
    "drmuon" : ('deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi) > 0.3',0.,5.,100,"deltaRjet", ";#DeltaR(photon, muon);Number of photons", 1,'deltaR(eta, phi, overlaps("muons")[0].eta, overlaps("muons")[0].phi)'),
    "etcut" : ("et>20", 0, 500, 100, "TransversalEnergy", ";E_{T} / 5 GeV;Number of photons", 1, "et"),
    "eta" : ("(abs(eta)<1.4442 || 1.556<abs(eta)<2.5)", -4, 4, 80, "Eta", ";#eta;Number of photons", 1, "eta"),
    "etabarrel" : ("abs(eta)<1.4442", -4, 4, 80, "EtaBarrel", "Eta;#eta;Number of photons", 1, "eta"),
    "etaendcap" : ("1.556<abs(eta)<2.5",-4, 4, 80, "EtaEndcap", "Eta;#eta;Number of photons", 1, "eta"),
    "hadronicoverem" : ("hadronicOverEm<0.05", 0, 0.1, 40, "HadronicOverEm", ";H/E;Number of photons", 1, "hadronicOverEm"),
    #"etawidth" : ("(superCluster.etaWidth<0.011 || (abs(eta)>1.5 && superCluster.etaWidth<0.03))", 0, 0.06, 40, "EtaWidth", ";#eta width;Number of photons", 1, "superCluster.etaWidth"),
    #"etawidthendcap" : ("superCluster.etaWidth<0.03", 0, 0.06, 80, "EtaWidthEndcap", "EtaWidthEndcap;#eta width;Number of photons", 1, "superCluster.etaWidth"),
    #"etawidthbarrel" : ("superCluster.etaWidth<0.011", 0, 0.06, 30, "EtaWidthBarrel", "EtaWidthBarrel;#eta width;Number of photons", 1, "superCluster.etaWidth"),
    "haspixelseeds" : ("hasPixelSeed = 0", -0.5, 1.5, 2, "HasPixelSeeds", ";Number of pixel seeds;Number of photons", 1, "hasPixelSeed"),
    "sigmaietaieta" : ("(sigmaIetaIeta<0.011 || (abs(eta)>1.5 && sigmaIetaIeta<0.03))",0, 0.09,40,"SigmaIetaIeta", ";#sigma_{i #eta i #eta}; Number of photons", 1, "sigmaIetaIeta"),
    "hollowconetrackiso" : ("trkSumPtHollowConeDR04<2+0.001*et+0.0167", 0, 20, 40, "HollowConeTrackIso", ";Hollow cone track iso / 0.5 GeV;Number of photons", 1, "trkSumPtHollowConeDR04"),
    "jurassicecaliso" : ("ecalRecHitSumEtConeDR04<4.2+0.006*et", 0, 20, 40 , "JurassicECALIso", ";Jurassic ECAL iso / 0.5 GeV;Number of photons", 1, "ecalRecHitSumEtConeDR04"),
    "hcaliso" : ("hcalTowerSumEtConeDR04<2.2+0.0025*et", 0, 8, 40, "TowerbasedHcalIsolation", ";Towerbased HCAL iso / 0.2 GeV;Number of photons", 1, "hcalTowerSumEtConeDR04"),
    }
#,"etawidth"
cut_key_list = [
    "eta",
    "etcut",
    "drmuon",
#    "ptrelDrjet99",
#    "drjet",
    "haspixelseeds",
    "hadronicoverem",
    "sigmaietaieta",
    "ptrelDrjet02",
    "ptrelDrjet10",
    "ptrelDrjet30",
    "hollowconetrackiso",
    "jurassicecaliso",
    "hcaliso"
]
all_cuts = ""
for key in cuts:
    all_cuts += cuts[key][0] + " && "
print "\nALL CUTS:\n" + str(all_cuts) + "\n\n"

def make_plot(src, key):
    ControlPlot=cms.EDAnalyzer(
        "CandViewHistoAnalyzer",
        src = cms.InputTag(src),
        histograms = cms.VPSet(
            cms.PSet(
                min          = cms.untracked.double(cuts[key][1]),
                max          = cms.untracked.double(cuts[key][2]),
                nbins        = cms.untracked.int32 (cuts[key][3]),
                name         = cms.untracked.string("histo"),
                description  = cms.untracked.string(cuts[key][5]),
                lazyParsing  = cms.untracked.bool(True),
                plotquantity = cms.untracked.string(cuts[key][7])
            )
        )
    )
    return ControlPlot

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
