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
#include <vector>
#include <string>
#include <iostream>

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
      edm::InputTag weights_;
      std::string label_;
      std::vector<double> weightCounters_;
};

//
// constructors and destructor
//
PDFWeight::PDFWeight(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    weights_(iConfig.getParameter<edm::InputTag>("weights")),
    label_(iConfig.getParameter<std::string>("label"))
{
}


PDFWeight::~PDFWeight()
{
}


// ------------ method called to produce the data  ------------
void
PDFWeight::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;

    if (iEvent.isRealData()) {
        return;
    }

    edm::Handle<std::vector<double> > pdfWeightHndl;
    iEvent.getByLabel(src_, pdfWeightHndl);

    if (!weightCounters_.size()) {  // first event: initialize vector
        weightCounters_.resize(pdfWeightHndl->size(), 0.);
    }

    edm::Handle<double> outerWeightHndl;
    iEvent.getByLabel(weights_, outerWeightHndl);
    double outerEventWeight = *outerWeightHndl.product();
    weightCounters_[0] += outerEventWeight;

    double nominal = pdfWeightHndl->at(0);
    double weightFactor = outerEventWeight / nominal;
    for (unsigned i=1; i<pdfWeightHndl->size(); i+=1) {
        weightCounters_[i] += weightFactor * pdfWeightHndl->at(i);
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
    using namespace std;
    for (unsigned i=0; i<weightCounters_.size(); ++i) {
        cout << "PDFWeightEventCountPrinter: InputTag:  label = PDFWeight" << label_ << i
             << ", instance =  " << weightCounters_[i]
             << endl;
    }
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
