// -*- C++ -*-
//
// Package:    PDFWeight
// Class:      PDFWeight
// 
/**\class PDFWeight PDFWeight.cc MyPackage/PDFWeight/src/PDFWeight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Thu Nov 21 13:05:34 CET 2013
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


//
// class declaration
//

class PDFWeight : public edm::EDProducer {
   public:
      explicit PDFWeight(const edm::ParameterSet&);
      ~PDFWeight();

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
      int uncertMode_;
};

//
// constructors and destructor
//
PDFWeight::PDFWeight(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    uncertMode_(iConfig.getParameter<int>("uncertMode"))
{
    produces<double>("");
    produces<double>("central");
}


PDFWeight::~PDFWeight()
{
}


// ------------ method called to produce the data  ------------
void
PDFWeight::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    std::auto_ptr<double> eventWeightOut(new double);
    std::auto_ptr<double> eventWeightCentralOut(new double);
    *eventWeightOut = 1.;
    *eventWeightCentralOut = 1.;

    if (iEvent.isRealData  || 0 == uncertMode_) {
        iEvent.put(eventWeightOut, "");
        iEvent.put(eventWeightCentralOut, "central");
        return;
    }

    edm::Handle<std::vector<double> > weightVector;
    iEvent.getByLabel(src_, weightVector);

    double centralWeight = weightVector->at(0);
    *eventWeightCentralOut = centralWeight;
    iEvent.put(eventWeightCentralOut, "central");

    if (true) { //uncertMode_ > 0) {
        double minWeight = centralWeight;
        double maxWeight = centralWeight;
        for (unsigned i=1; i<weightVector->size(); i+=2) {
           std::cout << "Event weight for PDF variation +" << (j+1)/2 << ": " << weightVector[j] << std::endl;
           std::cout << "Event weight for PDF variation -" << (j+1)/2 << ": " << weightVector[j+1] << std::endl;
//            if (minWeight > weightVector->at(i))
//                minWeight = weightVector->at(i);
//            if (maxWeight < weightVector->at(i))
//                maxWeight = weightVector->at(i);
        }
        iEvent.put(eventWeightOut, "");
    }
}

// ------------ method called once each job just before starting event loop  ------------
void 
PDFWeight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PDFWeight::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
PDFWeight::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
PDFWeight::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
PDFWeight::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
PDFWeight::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PDFWeight::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PDFWeight);
