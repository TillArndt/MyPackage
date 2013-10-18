// -*- C++ -*-
//
// Package:    TopPtProducer
// Class:      TopPtWeight
// 
/**\class TopPtWeight TopPtWeight.cc MyPackage/TopPtProducer/src/TopPtWeight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Mon Aug 19 15:44:44 CEST 2013
// $Id: TopPtWeight.cc,v 1.1 2013/10/09 14:06:38 htholen Exp $
//
//


// system include files
#include <memory>
#include <math.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

//
// class declaration
//

class TopPtWeight : public edm::EDProducer {
   public:
      explicit TopPtWeight(const edm::ParameterSet&);
      ~TopPtWeight();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      double sf(double pt);

      // ----------member data ---------------------------
      edm::InputTag weights_;
      bool emptyWeightInputTag_;
      int uncertMode_; // can be 0, -1, +1 for no, minus, and plus sys uncert
      double weightsSum_;
      double nEvents_;
};

//
// constructors and destructor
//
TopPtWeight::TopPtWeight(const edm::ParameterSet& iConfig):
    weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag())),
    emptyWeightInputTag_(weights_.encode() == std::string("")),
    uncertMode_(iConfig.getUntrackedParameter<int>("uncertMode", 0)),
    weightsSum_(0.),
    nEvents_(0.)
{
    produces<double>();
}

TopPtWeight::~TopPtWeight()
{
}


//
// member functions
//
double
TopPtWeight::sf(double x)
{
    if (fabs(x) < 1e-37)
        return 1.;
    else
        return exp(0.159 - 0.00141*x);
}

// ------------ method called to produce the data  ------------
void
TopPtWeight::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    double newEventWeight = 1.;

    if(!iEvent.isRealData()) {
        // calculate event weight
        if (uncertMode_ > -1) {
            edm::Handle<double> ptTop;
            edm::Handle<double> ptAntiTop;
            iEvent.getByLabel(edm::InputTag("topPtTTbar", "ptTop"), ptTop);
            iEvent.getByLabel(edm::InputTag("topPtTTbar", "ptAntiTop"), ptAntiTop);
            newEventWeight = sqrt(
                sf(*ptTop.product()) * sf(*ptAntiTop.product())
            );
        }
        if (uncertMode_ > 0) {
            newEventWeight = newEventWeight * newEventWeight;
        }

        weightsSum_ += newEventWeight;
        nEvents_ += 1.;

        // if chained to prior weight function
        if (!emptyWeightInputTag_) {
            float weight = 1.;
            edm::Handle<double> weightHandle;
            iEvent.getByLabel(weights_, weightHandle);
            weight = *weightHandle.product();
            if (isnan(weight)) {
                weight = 1.;
            }
            newEventWeight *= weight;
        }
    }

    // store in event
    std::auto_ptr<double> eventWeightOut(new double);
    *eventWeightOut = newEventWeight;
    iEvent.put(eventWeightOut);
}

// ------------ method called once each job just before starting event loop  ------------
void 
TopPtWeight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TopPtWeight::endJob()
{
    std::cout
    << "WeightedEventCountPrinter: InputTag:  label = AverageTopPtWeight, instance =  "
    << weightsSum_ / nEvents_
    << std::endl
    << "weightsSum: " << weightsSum_
    << " nEvents: " << nEvents_
    << std::endl;
}

// ------------ method called when starting to processes a run  ------------
void 
TopPtWeight::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TopPtWeight::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TopPtWeight::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TopPtWeight::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TopPtWeight::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TopPtWeight);
