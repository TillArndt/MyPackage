// -*- C++ -*-
//
// Package:    MCatNLOWeight
// Class:      MCatNLOWeight
// 
/**\class MCatNLOWeight MCatNLOWeight.cc MyPackage/MCatNLOWeight/src/MCatNLOWeight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Till Michael Arndt,,,
//         Created:  Mi 30. Okt 11:41:01 CET 2013
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

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

//
// class declaration
//

class MCatNLOWeight : public edm::EDProducer {
   public:
      explicit MCatNLOWeight(const edm::ParameterSet&);
      ~MCatNLOWeight();

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
      edm::InputTag genInfo_;
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
MCatNLOWeight::MCatNLOWeight(const edm::ParameterSet& iConfig):
  genInfo_(edm::InputTag("generator"))
{
    produces<double>();
  
}


MCatNLOWeight::~MCatNLOWeight()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
MCatNLOWeight::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   Handle<GenEventInfoProduct> genInfoHndl;
   iEvent.getByLabel(genInfo_, genInfoHndl);

   double weight = genInfoHndl->weight();
   int mcSign = weight/abs(weight);

   std::auto_ptr<double> mcatnloEventWeight(new double);
   *mcatnloEventWeight = mcSign;
   iEvent.put(mcatnloEventWeight);

 
}

// ------------ method called once each job just before starting event loop  ------------
void 
MCatNLOWeight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MCatNLOWeight::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
MCatNLOWeight::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MCatNLOWeight::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MCatNLOWeight::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MCatNLOWeight::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MCatNLOWeight::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MCatNLOWeight);
