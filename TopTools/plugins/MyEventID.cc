// -*- C++ -*-
//
// Package:    MyEventID
// Class:      MyEventID
// 
/**\class MyEventID MyEventID.cc MyEventID/MyEventID/src/MyEventID.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Yvonne Kuessel
//         Created:  Thu Nov 10 14:56:45 CET 2011
// $Id: MyEventID.cc,v 1.1 2011/11/16 11:15:30 htholen Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//
// class declaration
//
#include <sstream>
#include <fstream>
#include <iostream>

class MyEventID : public edm::EDAnalyzer {
   public:
      explicit MyEventID(const edm::ParameterSet&);
      ~MyEventID();

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

  std::string cutname_;
  std::ofstream f_;

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
MyEventID::MyEventID(const edm::ParameterSet& iConfig):
  cutname_(iConfig.getParameter<std::string>("cutname"))
{
   using namespace edm;
   using namespace std;
   //now do what ever initialization is needed
   f_.open(cutname_.c_str(),ios::out);    
}


MyEventID::~MyEventID()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
   f_.close();
}


//
// member functions
//

// ------------ method called for each event  ------------
void
MyEventID::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   f_<< iEvent.eventAuxiliary().id() << std::endl;

#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
MyEventID::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MyEventID::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
MyEventID::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MyEventID::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MyEventID::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MyEventID::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MyEventID::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MyEventID);
