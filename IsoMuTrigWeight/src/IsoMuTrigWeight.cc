// -*- C++ -*-
//
// Package:    IsoMuTrigWeight
// Class:      IsoMuTrigWeight
// 
/**\class IsoMuTrigWeight IsoMuTrigWeight.cc MyPackage/IsoMuTrigWeight/src/IsoMuTrigWeight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Mon Nov 18 19:50:13 CET 2013
// $Id$
//
//


// system include files
#include <memory>
#include <string>
#include <math.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "TFile.h"
#include "TKey.h"
#include "TGraphAsymmErrors.h"
//
// class declaration
//

class IsoMuTrigWeight : public edm::EDProducer {
   public:
      explicit IsoMuTrigWeight(const edm::ParameterSet&);
      ~IsoMuTrigWeight();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      void shiftUp(TGraphAsymmErrors* graph);
      void shiftDown(TGraphAsymmErrors* graph);

      // ----------member data ---------------------------
      TFile * sfFile_;
      TGraphAsymmErrors * sf_09_;
      TGraphAsymmErrors * sf_12_;
      TGraphAsymmErrors * sf_21_;
};

//
// constructors and destructor
//
IsoMuTrigWeight::IsoMuTrigWeight(const edm::ParameterSet& iConfig)
{
    produces<double>();

    sfFile_ = new TFile(iConfig.getParameter<std::string>("sfFile").c_str());
    sf_09_ = (TGraphAsymmErrors*) sfFile_->GetKey("IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Barrel_0to0p9_pt25-500_2012ABCD")->ReadObj();
    sf_12_ = (TGraphAsymmErrors*) sfFile_->GetKey("IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Transition_0p9to1p2_pt25-500_2012ABCD")->ReadObj();
    sf_21_ = (TGraphAsymmErrors*) sfFile_->GetKey("IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Endcaps_1p2to2p1_pt25-500_2012ABCD")->ReadObj();

    int uncertMode = iConfig.getUntrackedParameter<int>("uncertMode", 0);
    if (uncertMode > 0) {
        shiftUp(sf_09_);
        shiftUp(sf_12_);
        shiftUp(sf_21_);
    }
    if (uncertMode > 0) {
        shiftDown(sf_09_);
        shiftDown(sf_12_);
        shiftDown(sf_21_);
    }

}


IsoMuTrigWeight::~IsoMuTrigWeight()
{
    delete sf_09_;
    delete sf_12_;
    delete sf_21_;
    delete sfFile_;
}


void
IsoMuTrigWeight::shiftUp(TGraphAsymmErrors * graph) {
    for (int i=0; i < graph->GetN(); ++i) {
        double x, y;
        graph->GetPoint(i, x, y);
        graph->SetPoint(i, x, y + graph->GetErrorYhigh(i));
    }
}


void
IsoMuTrigWeight::shiftDown(TGraphAsymmErrors * graph) {
    for (int i=0; i < graph->GetN(); ++i) {
        double x, y;
        graph->GetPoint(i, x, y);
        graph->SetPoint(i, x, y - std::fabs(graph->GetErrorYlow(i)));
    }
}


// ------------ method called to produce the data  ------------
void
IsoMuTrigWeight::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    std::auto_ptr<double> eventWeightOut(new double);
    *eventWeightOut = 1.;

    // only on MC!
    if (iEvent.isRealData()) {
        iEvent.put(eventWeightOut);
        return;
    }

    edm::Handle<edm::View<pat::Muon> > muon;
    iEvent.getByLabel("tightmuons", muon);

    double pt = (*muon)[0].pt();
    double eta = (*muon)[0].eta();

    if (eta < 0.9) {
        *eventWeightOut = sf_09_->Eval(pt);
    } else if (eta < 1.2) {
        *eventWeightOut = sf_12_->Eval(pt);
    } else {
        *eventWeightOut = sf_21_->Eval(pt);
    }

    iEvent.put(eventWeightOut);
    return;
}

// ------------ method called once each job just before starting event loop  ------------
void 
IsoMuTrigWeight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
IsoMuTrigWeight::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
IsoMuTrigWeight::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
IsoMuTrigWeight::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
IsoMuTrigWeight::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
IsoMuTrigWeight::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
IsoMuTrigWeight::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(IsoMuTrigWeight);
