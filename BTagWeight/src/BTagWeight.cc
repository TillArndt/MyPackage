// -*- C++ -*-
//
// Package:    BTagWeight
// Class:      BTagWeight
// 
/**\class BTagWeight BTagWeight.cc MyPackage/BTagWeight/src/BTagWeight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Sun Aug 18 18:01:25 CEST 2013
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
#include "DataFormats/PatCandidates/interface/Jet.h"
//#include "DataFormats/Candidate/interface/Candidate.h"

//
// class declaration
//

class BTagWeight : public edm::EDProducer {
   public:
      explicit BTagWeight(const edm::ParameterSet&);
      ~BTagWeight();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      virtual float sf(float pt);
      virtual float sfErr(float pt);
      virtual float weightBin0(const std::vector<float> &btagSFs);
      virtual float weightBin1(const std::vector<float> &btagSFs);
      virtual float bTagWeight(const std::vector<float> &btagSFs);

      // ----------member data ---------------------------
      edm::InputTag src_;
      edm::InputTag weights_;
      bool emptyWeightInputTag_;
      int errorMode_;
      bool twoBTagMode_;
};

//
// constructors and destructor
//
BTagWeight::BTagWeight(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag())),
    emptyWeightInputTag_(weights_.encode() == std::string("")),
    errorMode_(iConfig.getUntrackedParameter<int>("errorMode", 0)),
    twoBTagMode_(iConfig.getUntrackedParameter<bool>("twoBTagMode", false))
{
    produces<double>();
}


BTagWeight::~BTagWeight()
{
}

//
// member functions
//
float BTagWeight::sf(float pt)
{
    return (
        0.939158+(0.000158694*pt))+(-2.53962e-07*(pt*pt)
    ) + (
        errorMode_ * sfErr(pt)
    );
}


float BTagWeight::sfErr(float pt)
{
    static float ptmax[] = {
        30.,
        40.,
        50.,
        60.,
        70.,
        80.,
        100.,
        120.,
        160.,
        210.,
        260.,
        320.,
        400.,
        500.,
        600.,
        800.,
        9999999.
    };
    static float SFb_error[] = {
        0.0415694,
        0.023429,
        0.0261074,
        0.0239251,
        0.0232416,
        0.0197251,
        0.0217319,
        0.0198108,
        0.0193,
        0.0276144,
        0.0205839,
        0.026915,
        0.0312739,
        0.0415054,
        0.0740561,
        0.0598311,
        0.0598311 * 2.
    };
    int i_bin = 0;
    while (pt < ptmax[i_bin]) {
        ++i_bin;
    }
    return SFb_error[i_bin];
}


float BTagWeight::weightBin0(const std::vector<float> &btagSFs)
{
    // product over i of (1 - btagSFs[i])
    float weight = 1.;
    for (unsigned i = 0; i < btagSFs.size(); ++i) {
        weight *= (1 - btagSFs[i]);
    }
    return weight;
}


float BTagWeight::weightBin1(const std::vector<float> &btagSFs)
{
    // sum over weight_i
    // where weight_i is
    // the product over not_i of (1 - btagSFs[not_i]) * btagSFs[i]
    float weight_sum = 0.;
    for (unsigned i_tagged = 0; i_tagged < btagSFs.size(); ++i_tagged) {
        float weight_i = 1.;
        for (unsigned i = 0; i < btagSFs.size(); ++i) {
            if (i_tagged == i) {
                weight_i *= btagSFs[i];
            } else {
                weight_i *= (1 - btagSFs[i]);
            }
        }
        weight_sum += weight_i;
    }
    return weight_sum;
}


float BTagWeight::bTagWeight(const std::vector<float> &btagSFs)
{
    float weight = 1.;
    weight -= weightBin0(btagSFs);
    if (twoBTagMode_)
        weight -= weightBin1(btagSFs);
    return weight;
}


// ------------ method called to produce the data  ------------
void
BTagWeight::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    double newEventWeight = 1.;

    // calculate event weight
    edm::Handle<std::vector<pat::Jet> > src;
    iEvent.getByLabel(src_, src);
    std::vector<float> btagSFs;
    std::vector<pat::Jet>::const_iterator jets = src->begin();
    for (; jets != src->end(); ++jets) {
        btagSFs.push_back(sf(jets->pt()));
    }
    newEventWeight *= bTagWeight(btagSFs);

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

    // store in event
    std::auto_ptr<double> eventWeightOut(new double);
    *eventWeightOut = newEventWeight;
    iEvent.put(eventWeightOut);
}

// ------------ method called once each job just before starting event loop  ------------
void 
BTagWeight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
BTagWeight::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
BTagWeight::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
BTagWeight::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
BTagWeight::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
BTagWeight::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BTagWeight::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTagWeight);
