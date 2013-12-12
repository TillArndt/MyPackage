#ifndef TOPTRIGGERWEIGHTPROVIDER_H
#define TOPTRIGGERWEIGHTPROVIDER_H

#include <vector>
/**
 * \class TopTriggerWeightProvider
 *
 * \brief Abstract: Class to read the trigger efficiency weights and
 * apply them on MC. Note that this class does not check whether you
 * are running on Data or MC, this is the responsibility of the
 * analyst.  In the class the various datataking periods have been
 * taken into account. One should note however that also the cut
 * selection changes during datataking, and this class assumes the
 * analyst is running the correct cutset for each run period. The
 * provided weights also assume that the analyst is comparing with
 * data with the correct trigger bit, depending on the run period
 *
 * \author Kelly Beernaert, Ghent University, v1 08/11/2012
 */


class TopTriggerEfficiencyProvider {
 public:

  TopTriggerEfficiencyProvider(bool verbose = true, double *lumis = 0);
  ~TopTriggerEfficiencyProvider() {};

  enum Runs { RunBEGIN=0, RunA=0, RunB, RunC, RunD, RunEND};
  enum JES { NOMINAL=0, DOWN=-1, UP=1};

  void setLumi(Runs r, double lumi) {luminosity[r]=lumi;}

  std::vector<double> get_weight(double lep_pt, double lep_eta,
		    double jet_pt, double jet_eta,
		    int npvertices, int njets,
		    bool LepIsMuon, JES jes=NOMINAL) const;

 protected:
  double GetLeptonWeight(bool isMuon, double pt, double eta, int npvertices) const;
  double GetJetWeight(double pt, double eta, int njets, JES jes) const;
  double TurnOn(double x, double par[4]) const;
  double VFunction(int x, const double par[2]) const;
  void warn(const char*) const;

  double luminosity[RunEND];
  const bool verbose;

  const static unsigned
    nMuEtabins, nMuPtbins,
    nElEtabins, nElPtbins,
    nJetEtabins,nJetPtbins,
    nJetMin,nJetNbins;

  const static double
    lumiDefaults[RunEND],
    jetPtMin, muPtMin, elPtMin,
    jetPtMax, muPtMax, elPtMax,
    jetEtaMax,muEtaMax,elEtaMax,
    JetEtaEdges[],JetPtEdges[],
    ElEtaEdges[],  ElPtEdges[],
    MuEtaEdges[],  MuPtEdges[],
    Mu[RunEND][6][8][2],
    El[RunEND][11][7][2],
    Jet[RunEND][3][5][5],
    JetDown[RunEND][3][5][5],
    JetUp[RunEND][3][5][5];
};

#endif








//#include "MyPackage/TopTriggerWeight/interface/TopTriggerEfficiencyProvider.h"
#include <algorithm>
#include <iostream>
#include "TMath.h"

TopTriggerEfficiencyProvider::TopTriggerEfficiencyProvider(bool verbose, double *lumis)
  : verbose(verbose) {
  for(int r = RunBEGIN; r<RunEND; r++) setLumi(Runs(r), lumis ? lumis[r] : lumiDefaults[r]);
}


std::vector<double> TopTriggerEfficiencyProvider::     //l+jets crosstrigger efficiency
get_weight(double lep_pt, double lep_eta,
	   double jet_pt, double jet_eta, // fourth leading jet
	   int npvertices, int njets,     // number primary vertices, number of jets
	   bool LepIsMuon, JES jes        // JES NOMINAL(0), UP(1), DOWN(-1)
	   ) const {
  std::vector<double> result;
  double weight =   0.0001 //factor to convert %^2 to efficiency on [0,1]
	    * GetLeptonWeight( LepIsMuon, lep_pt, lep_eta, npvertices) // weight of the leptonic leg of the cross trigger
	    * GetJetWeight( jet_pt, jet_eta, njets, jes);            // weight of the hadronic leg of the cross trigger
  result.push_back(weight);
  result.push_back(weight*sqrt(pow(0.9/GetLeptonWeight( LepIsMuon, lep_pt, lep_eta, npvertices),2)+pow(0.6/GetJetWeight( jet_pt, jet_eta, njets, jes),2)));
  return result;
}

double TopTriggerEfficiencyProvider::     //l+jets crosstrigger leptonic leg efficiency *100
GetLeptonWeight(bool isMu, double pt, double eta, int npvertices) const {
  int bin_x = isMu
    ? int( std::lower_bound( MuEtaEdges, MuEtaEdges + nMuEtabins, eta ) - MuEtaEdges )
    : int( std::lower_bound( ElEtaEdges, ElEtaEdges + nElEtabins, eta ) - ElEtaEdges );
  int bin_y = isMu
    ? int( std::lower_bound( MuPtEdges, MuPtEdges + nMuPtbins, std::min( muPtMax, pt ) ) - MuPtEdges)
    : int( std::lower_bound( ElPtEdges, ElPtEdges + nElPtbins, std::min( elPtMax, pt ) ) - ElPtEdges);

  if( fabs(eta) > (isMu?muEtaMax:elEtaMax) || pt < (isMu?muPtMin:elPtMin) || (!isMu && (bin_x ==2 || bin_x == 8))) {
    if(verbose) warn(isMu?"muon":"electron");
    return 100;
  }

  double sumL(0), sumWL(0);
  for (int r=RunBEGIN; r<RunEND; r++) {
    sumL += luminosity[r];
    sumWL += luminosity[r] * VFunction( npvertices, isMu ? Mu[r][bin_x][bin_y] : El[r][bin_x][bin_y]);
    }
  return std::min(100., std::max(0., sumWL / sumL ));
}


double TopTriggerEfficiencyProvider::   //evaluate linear parameterization of efficiency(x)
VFunction(int x, const double par[2]) const {
  return std::min( 100., std::max( 0., par[0]*x + par[1] ));
}


double TopTriggerEfficiencyProvider::     //l+jets crosstrigger hadronic leg efficiency *100
GetJetWeight(double pt, double eta, int njets, JES jes) const {
  if( pt < jetPtMin || njets < int(nJetMin) || fabs(eta) > jetEtaMax ) {
    if(verbose) warn("jet");
    return 100;
  }

  int bin_x = std::min( int(nJetNbins-1), std::max(0, int(njets-nJetMin)));
  int bin_y = int( std::lower_bound( JetEtaEdges, JetEtaEdges + nJetEtabins, eta ) - JetEtaEdges );
  int bin_z = int( std::lower_bound( JetPtEdges,  JetPtEdges  + nJetPtbins,  std::min(pt, jetPtMax) ) - JetPtEdges );

  double sumL(0), sumWL(0);
  for (int r=RunBEGIN; r<RunEND; r++) {
    sumL += luminosity[r];
    sumWL += luminosity[r] * (jes==DOWN ? JetDown :
			      jes==UP   ? JetUp   : Jet)[r][bin_x][bin_y][bin_z];
  }
  return std::min(100., std::max(0., sumWL / sumL ));
}


void TopTriggerEfficiencyProvider::
warn(const char* obj) const {
  std::cout << "Your " << obj
	    << " cut is not in sync with the Top Reference Selection! "
	    << "Please check your cutset again. Weight artificially 1." << std::endl;
}


double TopTriggerEfficiencyProvider::   //unused, but maybe necessary in future
TurnOn(double x, double par[4]) const
{
  double arg  = fabs(TMath::Sqrt(x)*par[1]) > 0
    ? (x - par[0])/ (TMath::Sqrt(x)*par[1])
    : 100000000000.;
  double arg2 = (x - par[3])/ (TMath::Sqrt(2.)*par[4]);

  return 0.5*par[2]*(1+TMath::Erf(arg)+TMath::Erf(arg2));
}

const double TopTriggerEfficiencyProvider::lumiDefaults[TopTriggerEfficiencyProvider::RunEND] = {0.744,4.518,6.340,6.751};

const double TopTriggerEfficiencyProvider::muPtMin = 20;
const double TopTriggerEfficiencyProvider::muPtMax = 250;
const unsigned TopTriggerEfficiencyProvider::nMuPtbins = 8;
const double TopTriggerEfficiencyProvider::MuPtEdges[TopTriggerEfficiencyProvider::nMuPtbins] = {26, 30, 35, 40, 50, 60, 80, 250}; //Upper bin edges

const double TopTriggerEfficiencyProvider::muEtaMax = 2.1;
const unsigned TopTriggerEfficiencyProvider::nMuEtabins = 6;
const double TopTriggerEfficiencyProvider::MuEtaEdges[TopTriggerEfficiencyProvider::nMuEtabins] = { -1.2, -0.9, 0, 0.9, 1.2, 2.1}; //Upper bin edges

const double TopTriggerEfficiencyProvider::Mu[TopTriggerEfficiencyProvider::RunEND][TopTriggerEfficiencyProvider::nMuEtabins][TopTriggerEfficiencyProvider::nMuPtbins][2] = {
  //RunA
  {{{ -0.786239, 88.0548 },{ -0.647274, 88.2607 },{ -0.557871, 88.5382 },{ -0.698177, 89.7107 },{ -0.591695, 89.8018 },{ -0.408135, 88.6635 },{ -0.586906, 92.0239 },{ -0.155323, 87.9477 } },
   {{ -0.698116, 88.6538 },{ -0.69978, 90.0567 },{ -0.940882, 95.2113 },{ -0.789592, 94.2578 },{ -0.679069, 93.3022 },{ -0.309612, 89.4445 },{ -0.381995, 91.8964 },{ -0.427049, 93.4482 } },
   {{ -0.59619, 93.2825 },{ -0.597186, 96.5267 },{ -0.493166, 96.4465 },{ -0.333111, 95.5162 },{ -0.261601, 95.8136 },{ -0.246547, 97.1673 },{ -0.148039, 96.0134 },{ -0.125502, 97.3149 } },
   {{ -0.854371, 97.2737 },{ -0.78862, 98.9136 },{ -0.5496, 97.618 },{ -0.419147, 97.0159 },{ -0.277043, 96.4474 },{ -0.228958, 96.8989 },{ -0.1367, 96.47 },{ -0.128746, 98.6746 } },
   {{ -1.01608, 93.1439 },{ -0.729595, 91.0788 },{ -0.724583, 91.5986 },{ -0.741503, 92.9753 },{ -0.748872, 94.1436 },{ -0.383513, 89.312 },{ -1.18062, 99.6014 },{ -1.11143, 101 } },
   {{ -0.805007, 89.4837 },{ -0.644028, 89.9611 },{ -0.450436, 88.1643 },{ -0.623627, 90.5344 },{ -0.66697, 91.4791 },{ -0.347725, 88.3197 },{ -0.350754, 88.3808 },{ -6.75269e-08, 88.7312 } }
  },

  //RunB
  {{{ -0.619034, 87.8381 },{ -0.53659, 88.848 },{ -0.510818, 87.7688 },{ -0.565823, 89.0159 },{ -0.545478, 89.3826 },{ -0.511984, 89.8459 },{ -0.429207, 88.9785 },{ -0.647861, 91.474 } },
   {{ -0.567199, 91.3577 },{ -0.494599, 92.0531 },{ -0.604714, 92.8431 },{ -0.582239, 92.3209 },{ -0.536812, 92.2881 },{ -0.426188, 91.1242 },{ -0.3277, 89.4473 },{ -0.580493, 92.6217 } },
   {{ -0.329806, 95.7945 },{ -0.246494, 96.1973 },{ -0.229645, 96.4168 },{ -0.186123, 96.36 },{ -0.118318, 95.9153 },{ -0.111322, 96.3112 },{ -0.103323, 96.2071 },{ -0.0338217, 94.9667 } },
   {{ -0.322097, 95.7216 },{ -0.273866, 96.8511 },{ -0.230154, 96.8367 },{ -0.157111, 96.3442 },{ -0.125872, 96.3507 },{ -0.104811, 96.264 },{ -0.0998774, 96.284 },{ -0.0296805, 95.021 } },
   {{ -0.553777, 90.4576 },{ -0.593409, 93.2143 },{ -0.609846, 92.4631 },{ -0.566875, 92.0931 },{ -0.520986, 92.1664 },{ -0.509328, 92.1046 },{ -0.478162, 91.7639 },{ -0.475186, 90.1882 } },
   {{ -0.484202, 87.6505 },{ -0.540188, 90.4458 },{ -0.484046, 89.5044 },{ -0.548141, 89.8624 },{ -0.545668, 90.3359 },{ -0.482066, 89.6734 },{ -0.562812, 91.6837 },{ -0.366324, 88.1425 } }
  },

  //RunC
  {{{ -0.55704, 88.0277 },{ -0.507766, 89.5853 },{ -0.563012, 89.797 },{ -0.543924, 89.7468 },{ -0.562943, 90.9052 },{ -0.495891, 90.5357 },{ -0.564886, 91.9206 },{ -0.381618, 88.9241 } },
   {{ -0.730376, 93.4954 },{ -0.716422, 95.876 },{ -0.542967, 92.0332 },{ -0.581084, 93.1386 },{ -0.537562, 92.658 },{ -0.408543, 91.3671 },{ -0.435887, 92.4277 },{ -0.555714, 92.2796 } },
   {{ -0.427374, 97.0603 },{ -0.265758, 96.4887 },{ -0.221022, 96.6464 },{ -0.180648, 96.4976 },{ -0.138286, 96.2977 },{ -0.081107, 96.0489 },{ -0.110883, 96.4291 },{ -0.103891, 96.0399 } },
   {{ -0.338184, 96.1382 },{ -0.260786, 96.6323 },{ -0.216931, 96.7321 },{ -0.196436, 96.9933 },{ -0.145212, 96.6221 },{ -0.130701, 96.8074 },{ -0.0950852, 96.304 },{ -0.0982588, 96.3275 } },
   {{ -0.665485, 92.7635 },{ -0.415882, 90.9149 },{ -0.655836, 93.644 },{ -0.614353, 93.4979 },{ -0.544135, 92.6599 },{ -0.440197, 91.4815 },{ -0.422683, 91.2302 },{ -0.562614, 93.276 } },
   {{ -0.562824, 90.3032 },{ -0.532421, 91.9433 },{ -0.486816, 91.3027 },{ -0.579303, 92.1732 },{ -0.572183, 92.5289 },{ -0.489473, 92.2809 },{ -0.467045, 91.7748 },{ -0.565103, 92.7513 } }
  },

  //RunD
  {{{ -0.609066, 88.79 },{ -0.586106, 90.3098 },{ -0.59297, 90.2651 },{ -0.622024, 91.044 },{ -0.604919, 91.7018 },{ -0.566922, 91.2273 },{ -0.524986, 90.5492 },{ -0.421954, 89.4114 } },
   {{ -0.710292, 93.2105 },{ -0.617157, 92.9399 },{ -0.583646, 92.47 },{ -0.631703, 93.2791 },{ -0.585367, 93.1323 },{ -0.508508, 92.7607 },{ -0.484216, 92.1149 },{ -0.499768, 92.3318 } },
   {{ -0.474935, 97.2321 },{ -0.320233, 96.9922 },{ -0.263906, 96.9654 },{ -0.200558, 96.604 },{ -0.168419, 96.706 },{ -0.126124, 96.3686 },{ -0.114979, 96.3594 },{ -0.0662406, 95.2466 } },
   {{ -0.42883, 96.8156 },{ -0.314535, 97.2471 },{ -0.260723, 97.2056 },{ -0.214813, 97.1404 },{ -0.146342, 96.6862 },{ -0.137041, 96.861 },{ -0.0761856, 96.1912 },{ -1.53758e-08, 94.8369 } },
   {{ -0.610022, 91.5672 },{ -0.614159, 93.5643 },{ -0.590222, 92.1583 },{ -0.639852, 93.0818 },{ -0.563038, 92.7968 },{ -0.55239, 92.8128 },{ -0.440929, 91.5361 },{ -0.444304, 91.6417 } },
   {{ -0.648128, 91.0422 },{ -0.580822, 91.906 },{ -0.62413, 92.3268 },{ -0.619006, 92.1502 },{ -0.585898, 92.3159 },{ -0.575194, 92.3792 },{ -0.558846, 92.2402 },{ -0.541224, 92.0354 } }
  }

};


const double TopTriggerEfficiencyProvider::elPtMin = 30;
const double TopTriggerEfficiencyProvider::elPtMax = 250;
const unsigned TopTriggerEfficiencyProvider::nElPtbins = 7;
const double TopTriggerEfficiencyProvider::ElPtEdges[TopTriggerEfficiencyProvider::nElPtbins] = {35, 40, 45, 50, 55, 60, 250}; //Upper bin edges

const double TopTriggerEfficiencyProvider::elEtaMax = 2.5;
const unsigned TopTriggerEfficiencyProvider::nElEtabins = 11;
const double TopTriggerEfficiencyProvider::ElEtaEdges[TopTriggerEfficiencyProvider::nElEtabins] = {-2.0, -1.566, -1.4442, -0.9, -0.3, 0.3, 0.9, 1.4442, 1.566, 2.0, 2.5}; //Upper bin edges

const double  TopTriggerEfficiencyProvider::El[TopTriggerEfficiencyProvider::RunEND][TopTriggerEfficiencyProvider::nElEtabins][TopTriggerEfficiencyProvider::nElPtbins][2] = {
  //RunA
  {{{ -1, 97.2132 },{ -0.563853, 98.8803 },{ -0.572235, 99.65 },{ -0.217779, 98.69 },{ -0.413419, 100.091 },{ 0.0, 97.2504 },{ 0.0, 95.7938 }},
   {{ -0.707184, 90.7544 },{ -0.680842, 96.6096 },{ -0.487965, 98.3306 },{ -0.301638, 97.6247 },{ -0.186875, 96.16 },{ -0.32949, 101 },{ -0.276702, 101 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.342037, 94.4601 },{ -0.105942, 94.1746 },{ -0.0907823, 95.5102 },{ -0.141756, 96.6221 },{ -0.228131, 98.4097 },{ 0, 96.533 },{ 0, 96.882} },
   {{ -0.172909, 92.5472 },{ -0.2616, 95.9411 },{ -0.130754, 96.036 },{ -0.257306, 98.471 },{ -0.143689, 96.5894 },{ 0, 94.3187 },{ 0, 95.9834 } },
   {{ -0.574124, 96.3134 },{ -0.212348, 93.6791 },{ -0.287115, 95.8293 },{ -0.117726, 94.9048 },{ -0.201588, 95.0753 },{ -0.0249331, 93.7034 },{ -0.22474, 96.9022} },
   {{ -0.318877, 92.1333 },{ -0.0929064, 92.8829 },{ -0.123572, 94.5809 },{ -0.0246895, 93.991 },{ -0.00590131, 94.4255 },{ -0.0952009, 96.3412 },{ 0, 93.9257 } },
   {{ -0.328397, 93.0142 },{ -0.0637046, 93.4674 },{ -0.154763, 96.6573 },{ -0.0265248, 95.2955 },{ 0, 95.4335 },{ 0, 96.1759 },{ 0, 97.4194 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.484194, 89.5653 },{ -0.534574, 95.2254 },{ -0.287775, 96.4871 },{ 0.0, 93.5507 },{ 0.0, 95.6312 },{ 0.0, 92.0602 },{ 0.0, 96.1455 } },
   {{ -0.79215, 93.9242 },{ -0.684836, 99.0099 },{ -0.187567, 96.6416 },{ -0.213511, 96.3112 },{ -0.150084, 97.6014 },{ -0.102185, 97.8765 },{ -0.278678, 100.475 } }
  },

  //RunB
  {{{ -0.739697, 94.1035 },{ -0.56571, 97.6511 },{ -0.394384, 98.7111 },{ -0.253083, 97.9691 },{ -0.319215, 100.027 },{ -0.100264, 97.4922 },{ -0.0102552, 97.0193 } },
   {{ -0.460334, 88.6797 },{ -0.399236, 93.9139 },{ -0.32928, 96.4057 },{ -0.272064, 96.7994 },{ -0.108545, 96.5186 },{ -0.106825, 96.2021 },{ -0.0387592, 96.8721 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.364395, 93.0969 },{ -0.183553, 94.5773 },{ -0.153076, 96.0444 },{ -0.105736, 96.4698 },{ -0.109568, 96.9283 },{ -0.0122119, 95.9629 },{ -0.110969, 97.9636 } },
   {{ -0.370621, 94.7748 },{ -0.209063, 95.0539 },{ -0.170314, 96.5568 },{ -0.12287, 96.7606 },{ -0.083158, 96.4913 },{ -0.0830593, 96.8121 },{ 0.0, 96.0513 } },
   {{ -0.390612, 94.6528 },{ -0.23036, 95.0458 },{ -0.177004, 96.0709 },{ -0.129269, 96.2262 },{ -0.121796, 96.5344 },{ -0.0424696, 95.9968 },{ -0.0480462, 96.315 } },
   {{ -0.35506, 94.0233 },{ -0.249421, 95.2578 },{ -0.147393, 95.9007 },{ -0.110904, 96.0461 },{ -0.121223, 96.9072 },{ -0.0752708, 96.2985 },{ -0.018918, 96.0494 } },
   {{ -0.319954, 92.9104 },{ -0.227249, 95.3743 },{ -0.145299, 96.3758 },{ -0.12227, 96.6828 },{ -0.155303, 97.7402 },{ -0.106365, 97.4288 },{ 0.0, 96.5272 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.641998, 90.2577 },{ -0.417292, 93.7635 },{ -0.295611, 95.658 },{ -0.205841, 95.9305 },{ -0.0755797, 94.7779 },{ -0.184313, 96.8579 },{ -0.0799222, 96.3935 } },
   {{ -0.671962, 93.0569 },{ -0.41043, 95.7282 },{ -0.346678, 98.114 },{ -0.201583, 97.8414 },{ -0.189693, 97.74 },{ -0.00836585, 96.5515 },{ -0.0192024, 97.3 } }
  },

  //RunC
  {{{ -0.288676, 92.945 },{ -0.195894, 96.0052 },{ -0.146664, 97.3446 },{ -0.0811838, 97.3357 },{ -0.0613536, 97.7694 },{ -0.143759, 98.482 },{ 0.0, 97.4304 } },
   {{ -0.288096, 89.5554 },{ -0.234294, 94.3938 },{ -0.192007, 96.55 },{ -0.133382, 96.803 },{ -0.0714007, 96.5601 },{ -0.0990196, 97.0496 },{ -0.0628163, 97.3839 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.23734, 92.3849 },{ -0.165286, 94.7303 },{ -0.127319, 96.1637 },{ -0.127397, 97.0132 },{ -0.0300499, 95.9075 },{ -0.0346437, 96.5689 },{ -0.0362946, 96.9163 } },
   {{ -0.176414, 93.0712 },{ -0.143654, 94.9714 },{ -0.0988406, 95.9987 },{ -0.0614571, 96.1212 },{ -0.0588242, 96.4552 },{ -0.0313257, 96.6759 },{ -0.0483794, 97.0096 } },
   {{ -0.194918, 93.3208 },{ -0.13746, 94.4179 },{ -0.127911, 95.948 },{ -0.10993, 96.3335 },{ -0.0940826, 96.3219 },{ -0.0373471, 96.1665 },{ -0.032645, 96.3675 } },
   {{ -0.189317, 92.8449 },{ -0.144255, 94.6473 },{ -0.077174, 95.2017 },{ -0.0826738, 95.9374 },{ -0.0655797, 96.1344 },{ -0.0576705, 96.3494 },{ -0.0499148, 96.79 } },
   {{ -0.218998, 92.6319 },{ -0.149911, 94.9111 },{ -0.128941, 96.3567 },{ -0.0747269, 96.5359 },{ -0.0982935, 97.1081 },{ -0.0889128, 97.182 },{ -0.0124396, 96.8497 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.303766, 90.0336 },{ -0.224919, 94.2062 },{ -0.171682, 96.6069 },{ -0.148586, 97.4016 },{ -0.100687, 97.037 },{ -0.113776, 97.5499 },{ -0.0468661, 97.6356 } },
   {{ -0.284465, 92.3929 },{ -0.168501, 95.378 },{ -0.137427, 97.2548 },{ -0.0530461, 97.0519 },{ -0.119471, 98.5861 },{ -0.00392371, 97.303 },{ -0.0685242, 97.9174 } }
  },

  //RunD
  {{{ -0.161498, 91.1772 },{ -0.194675, 96.8259 },{ -0.106393, 97.221 },{ -0.102315, 98.3105 },{ -0.0954168, 98.2349 },{ 0.0, 97.2509 },{ 0.0, 97.6573 } },
   {{ -0.218698, 89.3184 },{ -0.235385, 94.9808 },{ -0.162286, 96.3942 },{ -0.122847, 96.9607 },{ -0.113094, 97.3265 },{ -0.0522723, 96.9902 },{ -0.0145501, 97.1115 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.266259, 92.4174 },{ -0.177815, 95.099 },{ -0.121346, 95.9522 },{ -0.112036, 96.672 },{ -0.101876, 96.7594 },{ -0.0875329, 97.1885 },{ -0.0866564, 97.7484 } },
   {{ -0.17402, 93.0241 },{ -0.112391, 94.3752 },{ -0.106294, 95.9204 },{ -0.0835331, 96.2847 },{ -0.0766488, 96.4895 },{ -0.0181821, 96.2884 },{ -0.0562084, 97.097 } },
   {{ -0.193194, 93.6095 },{ -0.134024, 94.5119 },{ -0.100369, 95.5685 },{ -0.10885, 96.242 },{ -0.0894055, 96.3316 },{ -0.048559, 95.8359 },{ -0.0669883, 96.7656 } },
   {{ -0.133874, 92.1953 },{ -0.118137, 94.2409 },{ -0.0916051, 95.2205 },{ -0.0781521, 95.8512 },{ -0.0741892, 96.1174 },{ -0.0663577, 96.4366 },{ -0.035773, 96.2752 } },
   {{ -0.246327, 92.669 },{ -0.18648, 95.4505 },{ -0.12597, 96.3526 },{ -0.107638, 96.8441 },{ -0.0782217, 97.0346 },{ -0.0888068, 97.3431 },{ -0.0529251, 97.2029 } },
   {{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0 },{ 0, 0} },
   {{ -0.260094, 90.1695 },{ -0.220372, 95.066 },{ -0.156704, 96.8369 },{ -0.102716, 97.1635 },{ -0.101287, 97.5797 },{ -0.115564, 98.0715 },{ -0.0825701, 98.0981 } },
   {{ -0.173382, 90.4522 },{ -0.178755, 95.7686 },{ -0.101956, 96.9176 },{ -0.126752, 98.2457 },{ -0.0303544, 97.3971 },{ 0.0, 97.1887 },{ 0.0, 97.2893 } }
  }

};


const unsigned TopTriggerEfficiencyProvider::nJetMin = 4;
const unsigned TopTriggerEfficiencyProvider::nJetNbins = 3;

const double TopTriggerEfficiencyProvider::jetEtaMax = 2.5;
const unsigned TopTriggerEfficiencyProvider::nJetEtabins = 5;
const double TopTriggerEfficiencyProvider::JetEtaEdges[TopTriggerEfficiencyProvider::nJetEtabins] = {-1.5,-0.50,0.50,1.50,2.5};

const double TopTriggerEfficiencyProvider::jetPtMin = 20;
const double TopTriggerEfficiencyProvider::jetPtMax = 120;
const unsigned TopTriggerEfficiencyProvider::nJetPtbins = 5;
const double TopTriggerEfficiencyProvider::JetPtEdges[TopTriggerEfficiencyProvider::nJetPtbins] = {25,30,35,40,120};

const double TopTriggerEfficiencyProvider::Jet[TopTriggerEfficiencyProvider::RunEND][TopTriggerEfficiencyProvider::nJetNbins][TopTriggerEfficiencyProvider::nJetEtabins][TopTriggerEfficiencyProvider::nJetPtbins] = {
  //RunA
  {{{96.124, 96.6667, 98.0952, 99.2064, 100},{97.2268, 97.8836, 97.9104, 99.5708, 100},{97.0149, 95.8716, 98.8372, 100, 100},{97.7891, 96.9697, 98.7342, 99.5781, 100},{95.7399, 94.3333, 98.1043, 100, 100}},
   {{97.0588, 98.2456, 98.4962, 100, 100},{98.913, 98.7421, 99.5238, 100, 100},{94.8529, 99.0291, 100, 100, 100},{95.2381, 96.8153, 99.0826, 100, 100},{95.7747, 99.1736, 97.6744, 100, 100}},
   {{100, 100, 95.7447, 100, 100},{100, 100, 98.9474, 100, 100},{93.75, 98.6842, 100, 100, 100},{90.9091, 90, 100, 100, 100},{100, 93.5484, 100, 100, 100}}
  },

  //RunB
  {{{98.6562, 99.5683, 99.0645, 99.8507, 100},{99.2269, 99.1772, 99.5668, 99.8344, 99.9017},{98.731, 99.1634, 99.8346, 99.9257, 99.9581},{98.9084, 99.2122, 99.516, 99.9178, 100},{98.7354, 99.2775, 99.5164, 100, 100}},
      {{98.8889, 99.361, 99.4012, 100, 100},{98.5267, 99.5015, 99.6367, 100, 100},{98.8176, 99.3301, 99.689, 99.9102, 99.9649},{99.0157, 99.7073, 99.6296, 99.8981, 99.9162},{98.916, 99.5192, 98.9751, 99.8311, 99.9208}},
        {{100, 100, 99.3921, 100, 100},{96.5517, 99.3902, 99.802, 99.8252, 99.9149},{98.6842, 99.7215, 99.8285, 99.8514, 99.9666},{100, 99.6689, 99.1837, 99.8305, 100},{100, 99.0099, 99.711, 100, 100}}
  },

  //RunC
  {{{98.45, 98.677, 99.4344, 99.5356, 100},{98.045, 98.7901, 99.5063, 100, 100},{98.1145, 99.5199, 99.6997, 99.7563, 99.9535},{98.0719, 98.5691, 99.6545, 99.9117, 100},{97.8091, 98.4727, 98.9373, 99.8536, 99.8968}},
      {{97.2477, 99.4898, 99.5106, 99.8138, 100},{98.2318, 98.9407, 99.6226, 99.8866, 100},{97.8175, 99.3852, 99.8145, 100, 99.9621},{99.2, 99.8837, 99.3782, 99.8855, 99.9527},{97.5831, 99.3548, 99.6587, 99.8055, 100}},
        {{98.2759, 98.0296, 100, 100, 100},{98.7654, 100, 100, 99.4854, 100},{100, 99.6564, 99.8039, 99.844, 100},{100, 98.9286, 100, 100, 100},{100, 98.8571, 99.3443, 100, 100}}
  },

  //RunD
  {{{96.6478, 98.4509, 99.3485, 99.6853, 99.7432},{97.7402, 98.4212, 99.3477, 99.8155, 99.9725},{97.9869, 98.8894, 99.8158, 99.877, 99.9534},{97.5676, 98.7209, 99.1911, 99.5787, 99.9725},{97.0625, 98.2711, 98.739, 99.5157, 99.8458}},
      {{98.1793, 98.3793, 98.9985, 99.5357, 99.9566},{98.5663, 99.2509, 99.4663, 99.72, 100},{98.0155, 98.8366, 99.6513, 100, 99.963},{97.4977, 98.4649, 99.5616, 99.6259, 99.9304},{96.1648, 98.8737, 99.3243, 99.6409, 100}},
        {{98.1982, 99.5, 99.8471, 99.7271, 100},{98.6755, 99.3651, 99.4429, 99.8259, 99.9564},{98.7342, 99.5399, 99.4521, 99.9249, 99.9824},{98.1366, 99.5327, 99.6176, 100, 99.9782},{97.5806, 99.4898, 99.8344, 99.8536, 100}}
  }

};

const double TopTriggerEfficiencyProvider::JetDown[TopTriggerEfficiencyProvider::RunEND][TopTriggerEfficiencyProvider::nJetNbins][TopTriggerEfficiencyProvider::nJetEtabins][TopTriggerEfficiencyProvider::nJetPtbins] = {
  //RunA
  {{{97.0588, 98.7179, 98.0296, 99.1936, 100},{97.2875, 98.8764, 98.7692, 99.5708, 100},{96.8858, 96.3504, 99.0991, 100, 100},{98.5213, 97.2067, 99.0712, 99.5833, 100},{98.3957, 95.5285, 99.0291, 100, 100}},
   {{98.3871, 99.1071, 100, 100, 100},{100, 99.2647, 99.4819, 100, 100},{96.9697, 100, 100, 100, 100},{98.7013, 97.2414, 99.4475, 100, 100},{98.6111, 100, 100, 100, 100}},
   {{100, 100, 97.8261, 100, 100},{100, 100, 98.6667, 100, 100},{100, 100, 100, 100, 100},{66.6667, 93.3333, 100, 100, 100},{100, 100, 100, 100, 100}}
  },

  //RunB
  {{{99.1412, 99.5185, 99.591, 99.8489, 100},{99.325, 99.5378, 99.7428, 99.8299, 99.9497},{99.0239, 99.4034, 99.9444, 99.85, 100},{99.1703, 99.2378, 99.8074, 99.9189, 100},{99.1081, 99.5272, 99.6875, 100, 99.9038}},
   {{98.0392, 99.4275, 99.6569, 100, 100},{99.0385, 99.3174, 99.6832, 100, 100},{99.3865, 99.6948, 99.8236, 99.9065, 100},{99.7748, 99.779, 99.8031, 99.7809, 99.9549},{99.3651, 99.4264, 99.3517, 100, 100}},
   {{100, 99.2958, 100, 100, 100},{100, 99.2337, 100, 99.7895, 99.9009},{100, 100, 99.7849, 99.8192, 99.9618},{100, 100, 98.995, 100, 100},{100, 100, 99.6241, 100, 100}}
  },

  //RunC
  {{{98.7429, 99.4619, 99.2814, 99.8311, 100},{98.249, 99.3754, 99.7171, 100, 100},{98.6842, 99.5475, 99.8101, 99.7602, 100},{98.4524, 99.1959, 99.7896, 100, 100},{98.6378, 99.0214, 99.0773, 99.8428, 100}},
   {{98.1061, 99.4141, 99.637, 100, 100},{98.7531, 99.3857, 99.6832, 100, 100},{99.2147, 99.8785, 99.799, 100, 99.9598},{99.5261, 99.7226, 99.4246, 100, 99.9485},{97.4074, 99.6317, 100, 100, 100}},
   {{97.8261, 100, 100, 100, 100},{98.1132, 100, 99.7429, 99.7976, 100},{100, 99.5708, 99.7664, 99.8117, 100},{100, 99.5169, 100, 100, 100},{100, 100, 99.5935, 100, 100}}
  },

  //RunD
  {{{97.6342, 98.7567, 99.3689, 99.6727, 99.788},{98.1348, 99.003, 99.7189, 99.8581, 100},{98.1776, 99.3374, 99.908, 99.9582, 99.9764},{98.2298, 99.124, 99.3861, 99.8578, 99.9435},{98.0293, 98.6225, 99.6401, 99.4048, 99.894}},
   {{98.1884, 98.7584, 99.6507, 99.5833, 100},{98.9035, 99.2528, 99.6294, 99.812, 100},{98.3723, 99.1458, 99.9031, 100, 99.9604},{97.7647, 98.8957, 99.723, 99.7689, 100},{98.2332, 99.3458, 99.5504, 99.895, 100}},
   {{100, 99.359, 100, 99.8205, 100},{100, 99.5842, 99.7658, 100, 99.9493},{100, 99.8016, 99.7758, 99.9079, 99.9795},{99.0991, 99.6154, 99.7561, 100, 99.9744},{100, 99.0196, 99.802, 99.8246, 100}},
  }

};

const double TopTriggerEfficiencyProvider::JetUp[TopTriggerEfficiencyProvider::RunEND][TopTriggerEfficiencyProvider::nJetNbins][TopTriggerEfficiencyProvider::nJetEtabins][TopTriggerEfficiencyProvider::nJetPtbins] = {
  //RunA
  {{{94.824, 93.6455, 98.6239, 98.5916, 100},{96.4885, 95.5497, 97.3761, 99.5816, 100},{95.3748, 96.0177, 96.6867, 99.6564, 100},{96.6049, 95.1923, 98.7692, 99.1803, 100},{95.183, 92.1875, 97.7477, 100, 100}},
   {{96.3415, 95.8621, 97.9592, 98.4962, 100},{94.9153, 96.2617, 97.7876, 99.1342, 100},{92.6174, 97.1074, 99.6124, 100, 100},{97.3684, 96.8254, 98.6726, 99.5516, 100},{93.8144, 96.7533, 96.8553, 99.1379, 100}},
   {{90.9091, 100, 96.7213, 98.0583, 100},{100, 100, 99.2593, 100, 100},{96.6667, 97.7273, 100, 99.3976, 100},{96.2963, 85.4167, 98.5714, 100, 100},{100, 92.4528, 98.4848, 100, 100}}
  },

  //RunB
  {{{97.7449, 99.1865, 98.7376, 99.723, 100},{98.5607, 98.6916, 99.3421, 99.9159, 99.9033},{98.4928, 99.0204, 99.6107, 99.9266, 99.9578},{98.3216, 98.9443, 99.5255, 99.7409, 100},{97.8683, 98.9508, 98.9761, 99.7271, 100}},
   {{98.5656, 98.564, 99.3481, 100, 100},{98.7441, 99.1993, 99.5173, 99.9023, 100},{98.2533, 99.0818, 99.4949, 100, 99.9349},{98.5075, 99.4814, 99.5905, 100, 99.9211},{98.6193, 98.9651, 98.961, 99.5427, 99.9283}},
   {{96, 99.6479, 99.5169, 100, 100},{96.1165, 99.7602, 99.5192, 99.8565, 99.9274},{99.0826, 99.093, 99.7218, 99.7619, 99.9709},{97.4138, 99.7409, 99.026, 99.8576, 100},{100, 98.6441, 100, 99.7863, 100}}
  },

  //RunC
  {{{97.3384, 98.1456, 99.1453, 99.5502, 100},{97.429, 98.5219, 99.2253, 99.9092, 100},{98.1607, 98.8894, 99.3448, 99.8318, 99.9088},{97.4594, 98.3511, 99.0747, 99.9097, 100},{97.295, 98.3441, 98.3756, 99.2837, 99.9017}},
   {{98.4513, 98.8827, 99.3234, 99.513, 100},{97.5884, 98.5795, 99.6537, 99.8947, 99.9557},{97.1564, 99.0758, 99.7494, 99.6337, 99.9644},{98.6509, 99.4861, 99.344, 99.5803, 99.9105},{96.9267, 98.9319, 99.4467, 99.6569, 100}},
   {{98.6667, 97.4545, 99.7382, 100, 100},{98.9691, 99.1501, 99.6716, 99.7072, 99.9612},{96.2963, 99.4652, 99.5448, 99.8696, 100},{100, 98.6413, 99.8081, 100, 100},{94.4444, 97.8903, 99.2556, 100, 100}}
  },

  //RunD
  {{{96.792, 97.2655, 98.7284, 99.4056, 99.7503},{96.7018, 97.5925, 98.912, 99.7631, 99.9445},{97.0667, 98.2585, 99.5078, 99.7967, 99.9062},{96.917, 98.1156, 98.9365, 99.4518, 99.9447},{96.2497, 97.598, 98.2741, 99.5356, 99.7435}},
   {{96.1225, 97.8523, 98.6568, 99.3506, 99.9191},{97.5794, 98.2921, 99.1525, 99.5914, 99.9562},{97.9275, 98.2899, 99.4404, 99.9117, 99.947},{97.4105, 97.6534, 99.0683, 99.4573, 99.9344},{95.9835, 97.3433, 98.9123, 99.4396, 99.9601}},
   {{95.9391, 99.0792, 99.0847, 99.7735, 100},{96.0526, 99.0419, 99.2464, 99.7177, 99.9626},{97.6526, 98.8493, 99.1085, 99.8155, 99.9848},{98.8764, 98.4108, 99.464, 99.9296, 99.9627},{97.5758, 98.2993, 99.5006, 99.5322, 100}},
  }

};







// -*- C++ -*-
//
// Package:    TopTriggerWeight
// Class:      TopTriggerWeight
// 
/**\class TopTriggerWeight TopTriggerWeight.cc MyPackage/TopTriggerWeight/src/TopTriggerWeight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Thu Nov 14 17:42:44 CET 2013
// $Id$
//
//


// system include files
#include <memory>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
//#include "MyPackage/TopTriggerWeight/interface/TopTriggerEfficiencyProvider.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"

//
// class declaration
//

class TopTriggerWeight : public edm::EDProducer {
   public:
      explicit TopTriggerWeight(const edm::ParameterSet&);
      ~TopTriggerWeight();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
      TopTriggerEfficiencyProvider *weight_provider_;
      int uncertMode_;
      TH1D * h_A_mu_pt_;
      TH1D * h_A_mu_eta_;
      TH1D * h_A_j_pt_;
      TH1D * h_A_j_eta_;
      TH1D * h_A_n_vtx_;
      TH1D * h_A_n_j_;
      TH1D * h_B_mu_pt_;
      TH1D * h_B_mu_eta_;
      TH1D * h_B_j_pt_;
      TH1D * h_B_j_eta_;
      TH1D * h_B_n_vtx_;
      TH1D * h_B_n_j_;

};

//
// constructors and destructor
//
TopTriggerWeight::TopTriggerWeight(const edm::ParameterSet& iConfig):
    uncertMode_(iConfig.getUntrackedParameter<int>("uncertMode", 0))
{
    weight_provider_ = new TopTriggerEfficiencyProvider();
    weight_provider_->setLumi(TopTriggerEfficiencyProvider::RunA,0.8893);
    weight_provider_->setLumi(TopTriggerEfficiencyProvider::RunB,4.4257);
    weight_provider_->setLumi(TopTriggerEfficiencyProvider::RunC,7.1477);
    weight_provider_->setLumi(TopTriggerEfficiencyProvider::RunD,7.318);
    produces<double>();

    edm::Service<TFileService> fs;
    h_A_mu_pt_    = fs->make<TH1D>("TTEP_A_mu_pt",  ";number of events;muon p_{T} / GeV", 100, 0., 500);
    h_A_mu_eta_   = fs->make<TH1D>("TTEP_A_mu_eta", ";number of events;muon #eta", 48, -2.4, 2.4);
    h_A_j_pt_     = fs->make<TH1D>("TTEP_A_jet_pt", ";number of events;4th leading jet p_{T} / GeV", 100, 0., 500);
    h_A_j_eta_    = fs->make<TH1D>("TTEP_A_jet_eta",";number of events;4th leading jet #eta", 48, -2.4, 2.4);
    h_A_n_vtx_    = fs->make<TH1D>("TTEP_A_n_vtx",  ";number of events;number of vertices", 50, 0.5, 50.5);
    h_A_n_j_      = fs->make<TH1D>("TTEP_A_n_jet",  ";number of events;number of jets", 20, 0.5, 20.5);
    h_B_mu_pt_    = fs->make<TH1D>("TTEP_B_mu_pt",  ";number of events;muon p_{T} / GeV", 100, 0., 500);
    h_B_mu_eta_   = fs->make<TH1D>("TTEP_B_mu_eta", ";number of events;muon #eta", 48, -2.4, 2.4);
    h_B_j_pt_     = fs->make<TH1D>("TTEP_B_jet_pt", ";number of events;4th leading jet p_{T} / GeV", 100, 0., 500);
    h_B_j_eta_    = fs->make<TH1D>("TTEP_B_jet_eta",";number of events;4th leading jet #eta", 48, -2.4, 2.4);
    h_B_n_vtx_    = fs->make<TH1D>("TTEP_B_n_vtx",  ";number of events;number of vertices", 50, 0.5, 50.5);
    h_B_n_j_      = fs->make<TH1D>("TTEP_B_n_jet",  ";number of events;number of jets", 20, 0.5, 20.5);
}


TopTriggerWeight::~TopTriggerWeight()
{
    delete weight_provider_;
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
TopTriggerWeight::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    std::auto_ptr<double> eventWeightOut(new double);
    *eventWeightOut = 1.;

    // only on MC!
    if (iEvent.isRealData()) {
        iEvent.put(eventWeightOut);
        return;
    }

    edm::Handle<edm::View<pat::Muon> > muon;
    iEvent.getByLabel("tightmuons", muon);

    edm::Handle< std::vector<pat::Jet> > jet;
    iEvent.getByLabel("selectedPatJetsForAnalysis", jet);

    edm::Handle<std::vector<reco::Vertex> > vertex;
    iEvent.getByLabel("offlinePrimaryVertices", vertex);

    if (jet->size() < 4 || muon->size() == 0) {
        iEvent.put(eventWeightOut);
        return;
    }

    std::vector<double> weight = weight_provider_->get_weight(
        (*muon)[0].pt(),
        (*muon)[0].eta(),
        (*jet)[3].pt(),
        (*jet)[3].eta(),
        vertex->size(),
        jet->size(),
        true,
        TopTriggerEfficiencyProvider::NOMINAL
    );

    if (weight[0] < 0.89) {
        h_A_mu_pt_->Fill((*muon)[0].pt());
        h_A_mu_eta_->Fill((*muon)[0].eta());
        h_A_j_pt_->Fill((*jet)[0].pt());
        h_A_j_eta_->Fill((*jet)[0].eta());
        h_A_n_vtx_->Fill(vertex->size());
        h_A_n_j_->Fill(jet->size());
    } else {
        h_B_mu_pt_->Fill((*muon)[0].pt());
        h_B_mu_eta_->Fill((*muon)[0].eta());
        h_B_j_pt_->Fill((*jet)[0].pt());
        h_B_j_eta_->Fill((*jet)[0].eta());
        h_B_n_vtx_->Fill(vertex->size());
        h_B_n_j_->Fill(jet->size());
    }

    // store in event
    if (uncertMode_ > 0)
        *eventWeightOut = weight[0] + weight[1];
    if (uncertMode_ == 0)
        *eventWeightOut = weight[0];
    if (uncertMode_ < 0)
        *eventWeightOut = weight[0] - weight[1];
    iEvent.put(eventWeightOut);
}

// ------------ method called once each job just before starting event loop  ------------
void 
TopTriggerWeight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TopTriggerWeight::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
TopTriggerWeight::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TopTriggerWeight::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TopTriggerWeight::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TopTriggerWeight::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TopTriggerWeight::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TopTriggerWeight);
