// -*- C++ -*-
//
// Package:    FilterJEC
// Class:      FilterJEC
// 
/**\class FilterJEC FilterJEC.cc MyPackage/FilterJEC/src/FilterJEC.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Tue Nov  5 11:23:54 CET 2013
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
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

//
// class declaration
//

class FilterJEC : public edm::EDFilter {
   public:
      explicit FilterJEC(const edm::ParameterSet&);
      ~FilterJEC();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual bool beginRun(edm::Run&, edm::EventSetup const&);
      virtual bool endRun(edm::Run&, edm::EventSetup const&);
      virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      float getJetUncert(float pt, float eta);
      bool passesJetCuts(const std::vector<float> &jet_pts);

   std::vector<double> cuts_;
   edm::InputTag src_;
   JetCorrectionUncertainty *uncert_;
};

//
// constructors and destructor
//
FilterJEC::FilterJEC(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    uncert_(new JetCorrectionUncertainty(
        *(new JetCorrectorParameters(
            iConfig.getParameter<std::string>("inputFile")
        ))
    ))
{
    cuts_.push_back(iConfig.getParameter<double>("cut1"));
    cuts_.push_back(iConfig.getParameter<double>("cut2"));
    cuts_.push_back(iConfig.getParameter<double>("cut3"));
    cuts_.push_back(iConfig.getParameter<double>("cut4"));
    // check that cuts are in descending order
    for (unsigned i=0; i<3; ++i) {
        assert(cuts_.at(i) >= cuts_.at(i+1));
    }
}

FilterJEC::~FilterJEC()
{
    delete uncert_;
}


//
// member functions
//

float
FilterJEC::getJetUncert(float pt, float eta) {
    uncert_->setJetPt(pt);
    uncert_->setJetEta(eta);
    return uncert_->getUncertainty(false);  // only down variation for now
}

bool
FilterJEC::passesJetCuts(const std::vector<float> &jet_pts) {
    // pat jets are pt ordered..
    for (unsigned i=0; i<4; ++i) {
        if (jet_pts.at(i) < cuts_.at(i)) {
            return false;
        }
    }
    return true;
}

// ------------ method called on each new Event  ------------
bool
FilterJEC::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    std::vector<float> jet_pts;
    edm::Handle<std::vector<pat::Jet> > src;
    iEvent.getByLabel(src_, src);
    std::vector<pat::Jet>::const_iterator jets = src->begin();
    for (; jets != src->end(); ++jets) {
        std::cout << getJetUncert(jets->pt(), jets->eta()) << std::endl;
        jet_pts.push_back(
            // uncerts are relative and have sign
            (jets->pt()) * (1 + getJetUncert(jets->pt(), jets->eta()))
        );
    }
    return passesJetCuts(jet_pts);
}

// ------------ method called once each job just before starting event loop  ------------
void 
FilterJEC::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FilterJEC::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
FilterJEC::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
FilterJEC::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
FilterJEC::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
FilterJEC::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FilterJEC::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(FilterJEC);
