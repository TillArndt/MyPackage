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

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "MyPackage/TopTriggerWeight/interface/TopTriggerEfficiencyProvider.h"

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
    edm::Handle<edm::View<pat::Muon> > muon;
    iEvent.getByLabel("tightmuons", muon);

    edm::Handle< std::vector<reco::PFJet> > jet;
    iEvent.getByLabel("ak5PFJets", jet);

    edm::Handle<std::vector<reco::Vertex> > vertex;
    iEvent.getByLabel("offlinePrimaryVertices", vertex);

    std::vector<double> weight = weight_provider_->get_weight(
        (*muon)[0].pt(),
        (*muon)[0].eta(),
        (*jet)[4].pt(),
        (*jet)[4].eta(),
        vertex->size(),
        jet->size(),
        false,
        TopTriggerEfficiencyProvider::NOMINAL
    );

    // store in event
    std::auto_ptr<double> eventWeightOut(new double);
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
