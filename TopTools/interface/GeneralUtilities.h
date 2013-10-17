#ifndef GeneralUtilities_h
#define GeneralUtilities_h

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h" 
#include "FWCore/ServiceRegistry/interface/Service.h"

#include <map>
#include <string>

#include "TTree.h"
#include <TString.h>
#include "TMath.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include <DataFormats/BTauReco/interface/SoftLeptonTagInfo.h>
#include <DataFormats/TrackReco/interface/Track.h>
#include <DataFormats/PatCandidates/interface/Jet.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/BTauReco/interface/SoftLeptonTagInfo.h>
#include "Math/Vector4D.h"
#include <sstream>
//#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "TVector3.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/ServiceRegistry/interface/Service.h"

#include <map>
#include <string>
#include "TVector3.h"
// #include "Math/VectorUtil.h" 

#include "TH1F.h"
#include "TGraph.h"
#include "TH2.h"
#include <TString.h>
#include <DataFormats/TrackReco/interface/Track.h>
#include <DataFormats/PatCandidates/interface/Jet.h>
#include <DataFormats/PatCandidates/interface/Muon.h>


using namespace std;
using namespace edm;
using namespace reco;

class GeneralUtilities{

  public:

    GeneralUtilities(){}; 
	~GeneralUtilities(){};
	
    template <typename T> int matchCollections(const T* object, edm::Handle<edm::View<T> > collection);
    template <typename T> int matchCollections(const T* object, edm::Handle<std::vector<T> > collection);
    double Round(double Zahl, int Stellen);
    std::string Table(std::map<std::string, std::vector<double> > entries, std::vector<std::string> head);
    std::string LatexTable(std::string label, std::string caption, std::vector<std::string> lines, std::vector<std::string> columns, std::vector<std::vector<double> > entries, std::vector<std::vector<double> > errorsPlus,std::vector<std::vector<double> > errorsMinus , int nachkommma);

    double ptVsJetaxis( reco::Track muon ,  const pat::JetRef  jetchosen  );
    double ptVsJetaxis( reco::Track muon ,  const pat::Jet &  jetchosen  );
    double ptVsJetaxis( const reco::GenParticleRef muon ,  const reco::GenParticleRef  bQuark);
    double ptVsJetaxis(const reco::Candidate& muon, reco::GenParticleRef bQuark);
    double ptVsJetaxis( reco::Track muon , edm::Ref<edm::View<pat::Jet> > jetchosen  );
    double ptVsJetaxis(const reco::Candidate& muon, const reco::Candidate*& bQuark);
    double plVsJetaxis( reco::Track muon ,  const pat::JetRef  jetchosen  );
    double plVsJetaxis( reco::Track muon ,  const pat::Jet &  jetchosen  );
    double plVsJetaxis( const reco::GenParticleRef muon ,  const reco::GenParticleRef  bQuark);
    double plVsJetaxis(const reco::Candidate& muon, reco::GenParticleRef bQuark);
    double plVsJetaxis( reco::Track muon , edm::Ref<edm::View<pat::Jet> > jetchosen  );
    double plVsJetaxis(const reco::Candidate& muon, const reco::Candidate*& bQuark);
};
template <typename T> // match to one collection
int
GeneralUtilities::matchCollections(const T* object, edm::Handle<edm::View<T> > collection)
{
  int index=-1;
  int indextmp=0;
  for(typename edm::View<T>::const_iterator it = collection->begin(); it != collection->end(); it++){ // import selection from filter
    if( fabs(it->pt() - object->pt())<0.0001 && fabs(it->eta() - object->eta())<0.0001 ){
      index=indextmp;
      break;
    }
    indextmp++;
  }
  return index;
}
template <typename T> // match to one collection
int
GeneralUtilities::matchCollections(const T* object, edm::Handle<std::vector<T> > collection)
{
  int index=-1;
  int indextmp=0;
  for(uint i=0 ; i < collection->size(); ++i){ // import selection from filter
    if( fabs( (*collection)[i].pt() - object->pt())<0.0001 && fabs( (*collection)[i].eta() - object->eta())<0.0001 ){
      index=indextmp;
      break;
    }
    indextmp++;
  }
  return index;
}
#endif
