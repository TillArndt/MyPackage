// -*- C++ -*-
//
// Package:    ShilpiWeight
// Class:      ShilpiWeight
//
/**\class ShilpiWeight ShilpiWeight.cc MyPackage/ShilpiWeight/src/ShilpiWeight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Mon Aug  5 14:57:50 CEST 2013
// $Id$
//
//


// system include files
#include <memory>
#include <string>
#include <math.h>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

//
// class declaration
//

class ShilpiWeight : public edm::EDProducer {
   public:
      explicit ShilpiWeight(const edm::ParameterSet&);
      ~ShilpiWeight();

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
      edm::InputTag weights_;
      edm::InputTag src_;
      double sum_;
};

//
// constructors and destructor
//
ShilpiWeight::ShilpiWeight(const edm::ParameterSet& iConfig):
    weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag())),
    src_(iConfig.getParameter<edm::InputTag>("src")),
    sum_(0.)
{
    produces<double>();
}


ShilpiWeight::~ShilpiWeight()
{

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
ShilpiWeight::produce(edm::Event& evt, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;
    Handle<vector<pat::Photon> > src;
    evt.getByLabel(src_, src);

    static const double p0 = 8.98715e-03;
    static const double p1 = 1.26266e+04;
    static const double p2 = 3.31640e+00;
//    static const double p0 = 3.3587/100.;
//    static const double p1 = 2788.18/100.;
//    static const double p2 = 1.67674;
    double fr = 0.;
    std::vector<pat::Photon>::const_iterator ph = src->begin();
    for (; ph != src->end(); ++ph) {
        double expo = pow(ph->pt(),p2);
        fr += p0 + (p1/expo);
    }

    if (!evt.isRealData() && weights_.encode() != std::string("")) {
        Handle<double> weight;
        evt.getByLabel(weights_, weight);
        fr *= *weight;
    }

    std::auto_ptr<double> fr_ptr(new double);
    *fr_ptr = fr;
    evt.put(fr_ptr);
    sum_ += fr;
}

// ------------ method called once each job just before starting event loop  ------------
void
ShilpiWeight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
ShilpiWeight::endJob()
{
    std::cout
    << "WeightedEventCountPrinter: InputTag:  label = ShilpiSumDirect, instance =  "
    << sum_
    << std::endl;
}

// ------------ method called when starting to processes a run  ------------
void
ShilpiWeight::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void
ShilpiWeight::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void
ShilpiWeight::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void
ShilpiWeight::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
ShilpiWeight::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ShilpiWeight);
