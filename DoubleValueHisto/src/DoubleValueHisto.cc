// -*- C++ -*-
//
// Package:    DoubleValueHisto
// Class:      DoubleValueHisto
// 
/**\class DoubleValueHisto DoubleValueHisto.cc MyPackage/DoubleValueHisto/src/DoubleValueHisto.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Tue Aug 20 17:20:27 CEST 2013
// $Id$
//
//


// system include files
#include <memory>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
//
// class declaration
//

class DoubleValueHisto : public edm::EDAnalyzer {
   public:
      explicit DoubleValueHisto(const edm::ParameterSet&);
      ~DoubleValueHisto();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------
      edm::InputTag src_;
      edm::InputTag weights_;
      bool emptyWeightInputTag_;
      TH1D *histo_;
};

//
// constructors and destructor
//
DoubleValueHisto::DoubleValueHisto(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag())),
    emptyWeightInputTag_(weights_.encode() == std::string(""))
{
   //now do what ever initialization is needed
  edm::Service<TFileService> fs;
  histo_ = fs->make<TH1D>(
    iConfig.getUntrackedParameter<std::string>("name", "histo").c_str(),
    iConfig.getUntrackedParameter<std::string>("title", "histo").c_str(),
    iConfig.getUntrackedParameter<int>("nbins"),
    iConfig.getUntrackedParameter<double>("min"),
    iConfig.getUntrackedParameter<double>("max")
  );

}


DoubleValueHisto::~DoubleValueHisto()
{
}


//
// member functions
//

// ------------ method called for each event  ------------
void
DoubleValueHisto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

    Handle<double> handle;
    iEvent.getByLabel(src_, handle);

    double eventWeight = 1.;
    if (!emptyWeightInputTag_) {
        float weight = 1.;
        edm::Handle<double> weightHandle;
        iEvent.getByLabel(weights_, weightHandle);
        weight = *weightHandle.product();
        if (isnan(weight)) {
            weight = 1.;
        }
        eventWeight *= weight;
    }

    histo_->Fill(*handle, eventWeight);
}


// ------------ method called once each job just before starting event loop  ------------
void 
DoubleValueHisto::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
DoubleValueHisto::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
DoubleValueHisto::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
DoubleValueHisto::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
DoubleValueHisto::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
DoubleValueHisto::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
DoubleValueHisto::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DoubleValueHisto);
