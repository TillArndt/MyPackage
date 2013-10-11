// -*- C++ -*-
//
// Package:    DoubleProduct
// Class:      DoubleProduct
// 
/**\class DoubleProduct DoubleProduct.cc MyPackage/DoubleProduct/src/DoubleProduct.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Thu Oct 10 18:27:06 CEST 2013
// $Id$
//
//


// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

//
// class declaration
//

class DoubleProduct : public edm::EDProducer {
   public:
      explicit DoubleProduct(const edm::ParameterSet&);
      ~DoubleProduct();

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
      std::vector<edm::InputTag> inputTags_;
};

//
// constructors and destructor
//
DoubleProduct::DoubleProduct(const edm::ParameterSet& iConfig)
{
    inputTags_ = iConfig.getParameter<std::vector<edm::InputTag> >("src");
    produces<double>();
}


DoubleProduct::~DoubleProduct()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
DoubleProduct::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    double prod = 1.;
    for (unsigned i = 0; i < inputTags_.size(); ++i) {
        edm::Handle<double> handle;
        iEvent.getByLabel(inputTags_.at(i), handle);
        if (!isnan(*handle.product()))
            prod *= *handle.product();
    }

    std::auto_ptr<double> out(new double);
    *out = prod;
    iEvent.put(out);
}

// ------------ method called once each job just before starting event loop  ------------
void 
DoubleProduct::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
DoubleProduct::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
DoubleProduct::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
DoubleProduct::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
DoubleProduct::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
DoubleProduct::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
DoubleProduct::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DoubleProduct);
