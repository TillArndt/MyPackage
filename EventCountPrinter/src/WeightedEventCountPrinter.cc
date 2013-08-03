// -*- C++ -*-
//
// Package:    WeightedEventCountPrinter
// Class:      WeightedEventCountPrinter
// 
/**\class WeightedEventCountPrinter WeightedEventCountPrinter.cc MyPackage/EventCountPrinter/src/WeightedEventCountPrinter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Fri Jun 21 12:28:08 CEST 2013
// $Id$
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

#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "MyProducts/MergeableFloatCounter/interface/MergeableFloatCounter.h"
//
// class declaration
//

class WeightedEventCountPrinter : public edm::EDAnalyzer {
   public:
      explicit WeightedEventCountPrinter(const edm::ParameterSet&);
      ~WeightedEventCountPrinter();

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
      float _eventCount;
      edm::InputTag _src;
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
WeightedEventCountPrinter::WeightedEventCountPrinter(const edm::ParameterSet& iConfig):
_eventCount(0.),
_src(iConfig.getParameter<edm::InputTag>("src"))
{
   //now do what ever initialization is needed

}


WeightedEventCountPrinter::~WeightedEventCountPrinter()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
WeightedEventCountPrinter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
}


// ------------ method called once each job just before starting event loop  ------------
void 
WeightedEventCountPrinter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
WeightedEventCountPrinter::endJob()
{
   std::cout << "WeightedEventCountPrinter: " << _src << " " << _eventCount << std::endl;
}

// ------------ method called when starting to processes a run  ------------
void 
WeightedEventCountPrinter::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
WeightedEventCountPrinter::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
WeightedEventCountPrinter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

void WeightedEventCountPrinter::endLuminosityBlock(const edm::LuminosityBlock & lumi, const edm::EventSetup & setup) {
   // Total number of events is the sum of the events in each of these luminosity blocks
   edm::Handle<edm::MergeableFloatCounter> evtCnt;
   lumi.getByLabel(_src, evtCnt);
   _eventCount += evtCnt->value;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
WeightedEventCountPrinter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(WeightedEventCountPrinter);
