// -*- C++ -*-
//
// Package:    TopPtProducer
// Class:      TopPtHisto
// 
/**\class TopPtHisto TopPtHisto.cc MyPackage/TopPtProducer/src/TopPtHisto.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Mon Aug 19 15:44:44 CEST 2013
// $Id$
//
//


// system include files
#include <memory>
#include <vector>
#include <TH1D.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

//
// class declaration
//

class TopPtHisto : public edm::EDAnalyzer {
   public:
      explicit TopPtHisto(const edm::ParameterSet&);
      ~TopPtHisto();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
      edm::InputTag weights_;
      bool emptyWeightInputTag_;
      TH1D *ptTop_;
      TH1D *ptAntiTop_;
};

//
// constructors and destructor
//
TopPtHisto::TopPtHisto(const edm::ParameterSet& iConfig):
    weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag())),
    emptyWeightInputTag_(weights_.encode() == std::string(""))
{
    edm::Service<TFileService> fs;
    ptTop_      = fs->make<TH1D>("ptTop",       ";top quark P_{T} / GeV;events", 70, 0., 700.);
    ptAntiTop_  = fs->make<TH1D>("ptAntiTop",   ";anti-top quark P_{T} / GeV;events", 70, 0., 700.);
}

TopPtHisto::~TopPtHisto()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
TopPtHisto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;

    Handle<double> ptTop;
    Handle<double> ptAntiTop;
    iEvent.getByLabel(edm::InputTag("topPtTTbar", "ptTop"), ptTop);
    iEvent.getByLabel(edm::InputTag("topPtTTbar", "ptAntiTop"), ptAntiTop);

    // event weight
    double eventWeight = 1.;
    if (!emptyWeightInputTag_) {
        float weight = 1.;
        edm::Handle<double> weightHandle;
        iEvent.getByLabel(weights_, weightHandle);
        weight = *weightHandle.product();
        if (isnan(weight)) {
            weight = 1.;
        }
        eventWeight *= weight;
    }

    // Fill control histograms
    if (*ptTop > 1e-37)
        ptTop_->Fill(*ptTop, eventWeight);
    if (*ptAntiTop > 1e-37)
        ptAntiTop_->Fill(*ptAntiTop, eventWeight);
}

// ------------ method called once each job just before starting event loop  ------------
void 
TopPtHisto::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TopPtHisto::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
TopPtHisto::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TopPtHisto::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TopPtHisto::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TopPtHisto::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TopPtHisto::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TopPtHisto);
