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
// $Id: MyPhotonAnalyzer.cc,v 1.2 2012/02/09 12:43:08 htholen Exp $
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
      TH1D * photonID_;
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
				                      200 , 0. , 5.);
  deltaRMuons_       = fs->make<TH1D>("DeltaR_muon",   
                                      "dR(photon, muon)",
                                      200 , 0. , 5.);
  overlapJetsNConst_ = fs->make<TH1D>("overlapJetsNumConstituents", 
                                      "overlapJetsNumConstituents",
                                      30 , 0.5 , 30.5);
  photonID_          = fs->make<TH1D>("photonID",
                                      ";photonID;number of photons",
                                      3 , 0.5 , 3.5);
  photonID_->SetStats(0);
  photonID_->SetBit(TH1::kCanRebin);
  photonID_->Fill("none", 1e-7);
  photonID_->Fill("loose", 1e-7);
  photonID_->Fill("tight", 1e-7);
}

MyPhotonAnalyzer::~MyPhotonAnalyzer()
{
    photonID_->GetXaxis()->SetNdivisions(3);
}


//
// member functions
//

// ------------ method called for each event  ------------
void
MyPhotonAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;

    // Photons Handle
    edm::Handle<std::vector<pat::Photon> > photons;
    iEvent.getByLabel(photons_, photons);

    // Reweight Handle
    edm::Handle<double> puWeight1BX;
    iEvent.getByLabel("puWeight","Reweight1BX", puWeight1BX);
    double pileUpWeight1BX = *puWeight1BX.product();
    if(iEvent.isRealData() || isnan(pileUpWeight1BX)){
        pileUpWeight1BX=1;
    }

    //turn pile up reweight off:
    pileUpWeight1BX=1;

    // loop over photons
    std::vector<pat::Photon>::const_iterator photon = photons->begin();
    for( ; photon != photons->end(); ++photon) {

        if (photon->photonID("PhotonCutBasedIDTight")) {
            photonID_->Fill("tight", pileUpWeight1BX);
        } else if (photon->photonID("PhotonCutBasedIDLoose")) {
            photonID_->Fill("loose", pileUpWeight1BX);
        } else {
            photonID_->Fill("none", pileUpWeight1BX);
        }

        reco::CandidatePtrVector::const_iterator overlap_it = photon->overlaps("jets").begin();
        for(; overlap_it != photon->overlaps("jets").end(); ++overlap_it) {
            const pat::Jet * overlap = dynamic_cast<const pat::Jet*>(overlap_it->get());
            // number of constituents
            overlapJetsNConst_->Fill(overlap->getPFConstituents().size(), pileUpWeight1BX);
            // deltaR to overlapCand
            float deltaR = reco::deltaR( overlap->eta(), overlap->phi(), photon->eta(), photon->phi() );
            deltaRJets_->Fill( deltaR, pileUpWeight1BX );
        }
        overlap_it = photon->overlaps("muons").begin();
        for(; overlap_it != photon->overlaps("muons").end(); ++overlap_it) {
            
            const pat::Muon * overlap = dynamic_cast<const pat::Muon*>(overlap_it->get());
            // deltaR to overlapCand
            float deltaR = reco::deltaR( overlap->eta(), overlap->phi(), photon->eta(), photon->phi() );
            deltaRMuons_->Fill( deltaR ,pileUpWeight1BX );
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
