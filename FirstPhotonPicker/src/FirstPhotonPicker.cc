// -*- C++ -*-
//
// Package:    FirstPhotonPicker
// Class:      FirstPhotonPicker
// 
/**\class FirstPhotonPicker FirstPhotonPicker.cc MyPackage/FirstPhotonPicker/src/FirstPhotonPicker.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Thu Aug  1 09:57:43 CEST 2013
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
#include "DataFormats/PatCandidates/interface/Photon.h"

//
// class declaration
//

class FirstPhotonPicker : public edm::EDProducer {
   public:
      explicit FirstPhotonPicker(const edm::ParameterSet&);
      ~FirstPhotonPicker();

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
      edm::InputTag src_;
};

//
// constructors and destructor
//
FirstPhotonPicker::FirstPhotonPicker(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src"))
{
    produces<std::vector<pat::Photon> >();
}


FirstPhotonPicker::~FirstPhotonPicker()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
FirstPhotonPicker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    Handle<std::vector<pat::Photon> > src;
    iEvent.getByLabel(src_, src);
    std::vector<pat::Photon>* out = new std::vector<pat::Photon>();
    std::vector<pat::Photon>::const_iterator firstPhoton = src->begin();
    if (firstPhoton != src->end()) {
        out->push_back(*firstPhoton);
    }
    std::auto_ptr<std::vector<pat::Photon> > pOut(out);
    iEvent.put(pOut);
}

// ------------ method called once each job just before starting event loop  ------------
void 
FirstPhotonPicker::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FirstPhotonPicker::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
FirstPhotonPicker::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
FirstPhotonPicker::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
FirstPhotonPicker::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
FirstPhotonPicker::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FirstPhotonPicker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(FirstPhotonPicker);
