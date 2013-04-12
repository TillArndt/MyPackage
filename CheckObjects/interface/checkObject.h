#ifndef checkObject_h
#define checkObject_h
//SYSTEM
#include <memory>
//USER
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/EDProduct.h"

//CMSSW
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h" 
#include "FWCore/ServiceRegistry/interface/Service.h"
//C++
#include <iostream>
#include <vector>
//ROOT
#include "TMath.h"
#include "TH1.h"
#include "TGraph.h"
#include "TFile.h"
#include "TTree.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include <DataFormats/PatCandidates/interface/Electron.h>
#include <DataFormats/PatCandidates/interface/Photon.h>
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/TriggerPath.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "AnalysisDataFormats/TopObjects/interface/TtSemiLeptonicEvent.h"
#include "AnalysisDataFormats/TopObjects/interface/TtSemiLepEvtPartons.h"
#include "TRandom.h"
#include "TDatime.h"
#include "TF1.h"
#include <fstream>

//CLASS DECLARATION---------------------------------------------------

class checkObject : public edm::EDAnalyzer {
   public:
      explicit checkObject(const edm::ParameterSet&);
      ~checkObject();
      template <typename T> int analyzeCollection(edm::Handle<edm::View<T> > collection, double weight);

   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob();

      /// check if histogram was booked
      bool booked(const std::string histName) const { return hists_.find(histName.c_str())!=hists_.end(); };
      /// fill histogram if it had been booked before
      void fill(const std::string histName, double value, double weight) const { if(booked(histName.c_str())) hists_.find(histName.c_str())->second->Fill(value, weight); };
      
      // simple map to contain all histograms; 
      // histograms are booked in the beginJob() 
      // method
      std::map<std::string, TH1F*> hists_; 

      std::string bTagAlgorithm_;
      const edm::InputTag srcObjects_;
      std::string objectType_;

};

template <typename T>
int
checkObject::analyzeCollection(edm::Handle<edm::View<T> > collection, double weight)
{
  fill("Mult", collection->size(), weight);
  if( collection->size()>0 ){
    fill("1Pt", (*collection)[0].pt(), weight);
    fill("1Eta", (*collection)[0].eta(), weight);
    fill("1Phi", (*collection)[0].phi(), weight);
    if(objectType_=="patJet"){
      const reco::Candidate* cand(&((*collection)[0]));
      const pat::Jet *jet=dynamic_cast<const pat::Jet*> (cand);
      fill("1Btag", jet->bDiscriminator(bTagAlgorithm_), weight);
    }
  }
  if( collection->size()>1 ){
    fill("2Pt", (*collection)[1].pt(), weight);
    fill("2Eta", (*collection)[1].eta(), weight);
    fill("2Phi", (*collection)[1].phi(), weight);
    if(objectType_=="patJet"){
      const reco::Candidate* cand(&((*collection)[1]));
      const pat::Jet *jet=dynamic_cast<const pat::Jet*> (cand);
      fill("2Btag", jet->bDiscriminator(bTagAlgorithm_), weight);
    }
  }
  if( collection->size()>2 ){
    fill("3Pt", (*collection)[2].pt(), weight);
    fill("3Eta", (*collection)[2].eta(), weight);
    fill("3Phi", (*collection)[2].phi(), weight);
    if(objectType_=="patJet"){
      const reco::Candidate* cand(&((*collection)[2]));
      const pat::Jet *jet=dynamic_cast<const pat::Jet*> (cand);
      fill("3Btag", jet->bDiscriminator(bTagAlgorithm_), weight);
    }
  }
  if( collection->size()>3 ){
    fill("4Pt", (*collection)[3].pt(), weight);
    fill("4Eta", (*collection)[3].eta(), weight);
    fill("4Phi", (*collection)[3].phi(), weight);
    if(objectType_=="patJet"){
      const reco::Candidate* cand(&((*collection)[3]));
      const pat::Jet *jet=dynamic_cast<const pat::Jet*> (cand);
      fill("4Btag", jet->bDiscriminator(bTagAlgorithm_), weight);
    }
  }
  if( collection->size()>4 ){
    fill("5Pt", (*collection)[4].pt(), weight);
    fill("5Eta", (*collection)[4].eta(), weight);
    fill("5Phi", (*collection)[4].phi(), weight);
    if(objectType_=="patJet"){
      const reco::Candidate* cand(&((*collection)[4]));
      const pat::Jet *jet=dynamic_cast<const pat::Jet*> (cand);
      fill("5Btag", jet->bDiscriminator(bTagAlgorithm_), weight);
    }
  }
  for(typename edm::View<T>::const_iterator it = collection->begin(); it != collection->end(); it++){ // import selection from filter
    fill("Pt", it->pt(), weight);
    fill("Eta", it->eta(), weight);
    fill("Phi", it->phi(), weight);
    if(objectType_=="patJet"){
      const reco::Candidate* cand(&(*it));
      const pat::Jet *jet=dynamic_cast<const pat::Jet*> (cand);
      fill("Charge", jet->jetCharge(), weight);
      fill("Btag", jet->bDiscriminator(bTagAlgorithm_), weight);
    }
    if(objectType_=="patMuon"){
     const reco::Candidate* cand(&(*it));
      const pat::Muon *muon=dynamic_cast<const pat::Muon*> (cand);
      fill("Charge", muon->charge(), weight);
    }
  }
  return 1;
}



#endif
