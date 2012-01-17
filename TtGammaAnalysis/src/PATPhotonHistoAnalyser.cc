/* \class PATPhotonHistoAnalyzer
 * 
 * Configurable pat::Photon Histogram creator
 *
 * \author: Heiner Tholen, RWTH Aachen
 *
 */
#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/HistoAnalyzer.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
//#include "DataFormats/Common/interface/View.h"
#include <vector>

typedef HistoAnalyzer<std::vector<pat::Photon> > PATPhotonHistoAnalyzer;

DEFINE_FWK_MODULE( PATPhotonHistoAnalyzer );










