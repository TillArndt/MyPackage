// -*- C++ -*-
//
// Package:    WeightedEventCountProducer
// Class:      WeightedEventCountProducer
// 

/**\class WeightedEventCountProducer WeightedEventCountProducer.cc
Description: An event counter that can store the number of events in the lumi block

*/


// system include files
#include <memory>
#include <string>
#include <vector>
#include <algorithm>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "MyProducts/MergeableFloatCounter/interface/MergeableFloatCounter.h"


class WeightedEventCountProducer : public edm::EDProducer {
public:
  explicit WeightedEventCountProducer(const edm::ParameterSet&);
  ~WeightedEventCountProducer();

private:
  virtual void produce(edm::Event &, const edm::EventSetup &);
  virtual void beginLuminosityBlock(edm::LuminosityBlock &, const edm::EventSetup &);
  virtual void endLuminosityBlock(edm::LuminosityBlock &, const edm::EventSetup &);
      
  // ----------member data ---------------------------

  float eventsProcessedInLumi_;
  edm::InputTag eventWeight_;
  bool emptyWeightInputTag_;
};

using namespace edm;
using namespace std;

WeightedEventCountProducer::WeightedEventCountProducer(const edm::ParameterSet& iConfig):
  eventWeight_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag())),
  emptyWeightInputTag_(eventWeight_.encode() == std::string(""))
{
  produces<edm::MergeableFloatCounter, edm::InLumi>();
}


WeightedEventCountProducer::~WeightedEventCountProducer(){}


void
WeightedEventCountProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

  float weight = 1.;
  if ((!iEvent.isRealData()) && (!emptyWeightInputTag_)) {
    edm::Handle<double> weightHandle;
    iEvent.getByLabel(eventWeight_, weightHandle);
    weight = *weightHandle.product();
    if (isnan(weight)) {
      weight = 1.;
    }
  }

  eventsProcessedInLumi_ += weight;
  return;
}


void 
WeightedEventCountProducer::beginLuminosityBlock(LuminosityBlock & theLuminosityBlock, const EventSetup & theSetup) {
  eventsProcessedInLumi_ = 0.;
  return;
}


void 
WeightedEventCountProducer::endLuminosityBlock(LuminosityBlock & theLuminosityBlock, const EventSetup & theSetup) {
  LogTrace("EventCounting") << "endLumi: adding " << eventsProcessedInLumi_ << " events" << endl;

  auto_ptr<edm::MergeableFloatCounter> numEventsPtr(new edm::MergeableFloatCounter);
  numEventsPtr->value = eventsProcessedInLumi_;
  theLuminosityBlock.put(numEventsPtr);

  return;
}



//define this as a plug-in
DEFINE_FWK_MODULE(WeightedEventCountProducer);
