// -*- C++ -*-
//
// Package:    FilterJER
// Class:      FilterJER
// 
/**\class FilterJER FilterJER.cc MyPackage/FilterJER/src/FilterJER.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Thu Nov  7 14:48:57 CET 2013
// $Id$
//
//


// system include files
#include <memory>
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJet.h"

#include "TH1.h"
//
// class declaration
//

class FilterJER : public edm::EDFilter {
   public:
      explicit FilterJER(const edm::ParameterSet&);
      ~FilterJER();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual bool beginRun(edm::Run&, edm::EventSetup const&);
      virtual bool endRun(edm::Run&, edm::EventSetup const&);
      virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      double getNewPt(const pat::Jet& jet, TH1F& factors);
      bool passesJetCuts(std::vector<float> &jet_pts);

      // ----------member data ---------------------------
      std::vector<double> cuts_;
      edm::InputTag src_;
      TH1F cFactorPlus_, cFactorMinus_;
};

static const float ETA_BINS[6] = {0.0, 0.5, 1.1, 1.7, 2.3, 5.0};

//
// constructors and destructor
//
FilterJER::FilterJER(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    cFactorPlus_("cPlus",  "cPlus",  5, ETA_BINS),
    cFactorMinus_("cMinus", "cMinus", 5, ETA_BINS)
{
    cuts_.push_back(iConfig.getParameter<double>("cut1"));
    cuts_.push_back(iConfig.getParameter<double>("cut2"));
    cuts_.push_back(iConfig.getParameter<double>("cut3"));
    cuts_.push_back(iConfig.getParameter<double>("cut4"));
    // check that cuts are in descending order
    for (unsigned i=0; i<3; ++i) {
        assert(cuts_.at(i) >= cuts_.at(i+1));
    }

    // These are factors of factors:  c_plus / c
    cFactorPlus_.SetBinContent(1, 1.115 / 1.052);
    cFactorPlus_.SetBinContent(2, 1.114 / 1.057);
    cFactorPlus_.SetBinContent(3, 1.161 / 1.096);
    cFactorPlus_.SetBinContent(4, 1.228 / 1.134);
    cFactorPlus_.SetBinContent(5, 1.488 / 1.288);
    cFactorMinus_.SetBinContent(1, 0.990 / 1.052);
    cFactorMinus_.SetBinContent(2, 1.001 / 1.057);
    cFactorMinus_.SetBinContent(3, 1.032 / 1.096);
    cFactorMinus_.SetBinContent(4, 1.042 / 1.134);
    cFactorMinus_.SetBinContent(5, 1.089 / 1.288);
}


FilterJER::~FilterJER()
{
}

//
// member functions
//
double
FilterJER::getNewPt(const pat::Jet& jet, TH1F& factors) {
    // Formula for smearing: pT->max[0.,pTgen+c*(pT–pTgen)]
    double jetPt = jet.pt();
    double c_factor = factors.GetBinContent(factors.FindBin(jet.eta()));
    double genJetPt = jet.genJet()->pt();
    return genJetPt + c_factor * (jetPt - genJetPt);
}

bool
FilterJER::passesJetCuts(std::vector<float> &jet_pts) {
    std::sort(jet_pts.begin(), jet_pts.end());
    for (unsigned i=0; i<4; ++i) {
        if (jet_pts.at(i) < cuts_.at(i)) {
            return false;
        }
    }
    return true;
}

// ------------ method called on each new Event  ------------
bool
FilterJER::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    std::vector<float> jet_pts_plus;
    std::vector<float> jet_pts_minus;

    edm::Handle<std::vector<pat::Jet> > src;
    iEvent.getByLabel(src_, src);
    std::vector<pat::Jet>::const_iterator jets = src->begin();
    for (; jets != src->end(); ++jets) {
        jet_pts_plus.push_back(getNewPt(*jets, cFactorPlus_));
        jet_pts_minus.push_back(getNewPt(*jets, cFactorMinus_));
    }
    return passesJetCuts(jet_pts_plus) && passesJetCuts(jet_pts_minus);
}

// ------------ method called once each job just before starting event loop  ------------
void 
FilterJER::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FilterJER::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
FilterJER::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
FilterJER::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
FilterJER::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
FilterJER::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FilterJER::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(FilterJER);
