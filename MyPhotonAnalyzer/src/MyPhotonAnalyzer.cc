// -*- C++ -*-
//
// Package:    MyPhotonAnalyzer
// Class:      MyPhotonAnalyzer
// 
/**\class MyPhotonAnalyzer MyPhotonAnalyzer.cc MyPackage/MyPhotonAnalyzer/src/MyPhotonAnalyzer.cc

 Description: My Photon Analyzer, eh?! Shows me, what I wanna know from photons...

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen
//         Created:  Fri Jan 13 23:02:34 CET 2012
// $Id: MyPhotonAnalyzer.cc,v 1.1 2012/01/19 09:30:17 htholen Exp $
//
//


// system include files
#include <memory>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"

#include <DataFormats/PatCandidates/interface/Photon.h>
#include <DataFormats/PatCandidates/interface/Jet.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
//
// class declaration
//

class MyPhotonAnalyzer : public edm::EDAnalyzer {
   public:
      explicit MyPhotonAnalyzer(const edm::ParameterSet&);
      ~MyPhotonAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------
      TH1D * deltaRMuons_;
      TH1D * deltaRJets_; 
      TH1D * overlapJetsNConst_; 
      edm::InputTag photons_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
MyPhotonAnalyzer::MyPhotonAnalyzer(const edm::ParameterSet& iConfig):
  photons_(iConfig.getParameter<edm::InputTag>("src"))
{
   //now do what ever initialization is needed
  edm::Service<TFileService> fs;
  deltaRJets_        = fs->make<TH1D>("DeltaR_jet", 
				      "dR(photon, jet)",
				      44 , 0. , 1.1);
  deltaRMuons_       = fs->make<TH1D>("DeltaR_muon",   
                                      "dR(photon, muon)",
                                      44 , 0. , 1.1);
  overlapJetsNConst_ = fs->make<TH1D>("overlapJetsNumConstituents", 
				      "overlapJetsNumConstituents",
				      30 , 0.5 , 30.5);
}

MyPhotonAnalyzer::~MyPhotonAnalyzer() {}


//
// member functions
//

// ------------ method called for each event  ------------
void
MyPhotonAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;

    edm::Handle<std::vector<pat::Photon> > photons;
    iEvent.getByLabel(photons_, photons); 

    std::vector<pat::Photon>::const_iterator photon = photons->begin();
    for( ; photon != photons->end(); ++photon) {
      
        reco::CandidatePtrVector::const_iterator overlap_it = photon->overlaps("jets").begin();
	for(; overlap_it != photon->overlaps("jets").end(); ++overlap_it) { 
	    const pat::Jet * overlap = dynamic_cast<const pat::Jet*>(overlap_it->get());
	    // number of constituents
	    overlapJetsNConst_->Fill(overlap->getPFConstituents().size());
	    // deltaR to overlapCand
	    float deltaR = reco::deltaR( overlap->eta(), overlap->phi(), photon->eta(), photon->phi() );
	    deltaRJets_->Fill( deltaR );
	}
        overlap_it = photon->overlaps("muons").begin();
        for(; overlap_it != photon->overlaps("muons").end(); ++overlap_it) {
            
            const pat::Muon * overlap = dynamic_cast<const pat::Muon*>(overlap_it->get());
            // deltaR to overlapCand
            float deltaR = reco::deltaR( overlap->eta(), overlap->phi(), photon->eta(), photon->phi() );
            deltaRMuons_->Fill( deltaR );
        }
    }
}

// ------------ method called once each job just before starting event loop  ------------
void 
MyPhotonAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MyPhotonAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
MyPhotonAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MyPhotonAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MyPhotonAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MyPhotonAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MyPhotonAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MyPhotonAnalyzer);
