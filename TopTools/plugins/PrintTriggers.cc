// -*- C++ -*-
//
// Package:    PrintTriggers
// Class:      PrintTriggers
// 
/**\class PrintTriggers PrintTriggers.cc Dilepton/Selection/plugins/PrintTriggers.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Bastian Kargoll
//         Created:  Mon Dec 21 18:06:19 CET 2009
// $Id: PrintTriggers.cc,v 1.1 2010/06/10 13:36:45 kuessel Exp $
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

#include "DataFormats/PatCandidates/interface/TriggerPath.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

//
// class decleration
//

class PrintTriggers : public edm::EDAnalyzer {
   public:
      explicit PrintTriggers(const edm::ParameterSet&);
      ~PrintTriggers();


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------
      edm::InputTag triggerSource_;
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
PrintTriggers::PrintTriggers(const edm::ParameterSet& iConfig)

{
  triggerSource_    = iConfig.getParameter<edm::InputTag>( "triggerSource" );
}


PrintTriggers::~PrintTriggers()
{

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
PrintTriggers::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   edm::Handle<pat::TriggerEvent> triggerEvent ; 
   iEvent.getByLabel(triggerSource_,triggerEvent);

   std::cout << "There are " << triggerEvent->paths()->size() << " stored TriggerPaths in total, which are:" << std:: endl;
   for(unsigned int i=0; i!= triggerEvent->paths()->size(); i++){
     std::cout << triggerEvent->paths()->at(i).name() << std::endl;
   }

}


// ------------ method called once each job just before starting event loop  ------------
void 
PrintTriggers::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PrintTriggers::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(PrintTriggers);
