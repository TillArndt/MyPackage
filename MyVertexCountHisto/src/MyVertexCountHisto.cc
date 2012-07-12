// -*- C++ -*-
//
// Package:    MyVertexCountHisto
// Class:      MyVertexCountHisto
// 
/**\class MyVertexCountHisto MyVertexCountHisto.cc MyPackage/MyVertexCountHisto/src/MyVertexCountHisto.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen
//         Created:  Tue Jun 12 15:47:18 CEST 2012
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

#include "TH1.h"
//
// class declaration
//

class MyVertexCountHisto : public edm::EDAnalyzer {
   public:
      explicit MyVertexCountHisto(const edm::ParameterSet&);
      ~MyVertexCountHisto();

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
      TH1D * histo_;
      edm::InputTag vertices_;
      edm::InputTag weights_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
MyVertexCountHisto::MyVertexCountHisto(const edm::ParameterSet& iConfig):
  vertices_(iConfig.getParameter<edm::InputTag>("src")),
  weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag()))
{
   //now do what ever initialization is needed
  edm::Service<TFileService> fs;
  histo_ = fs->make<TH1D>("vertexCount" , ";Vertex Multiplicity;Number of events" , 30 , 0.5 , 30.5 );
}


MyVertexCountHisto::~MyVertexCountHisto()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
MyVertexCountHisto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;

    // vertices Handle
    edm::Handle<std::vector<reco::Vertex> > vertices;
    iEvent.getByLabel(vertices_, vertices);

    // Reweight Handle
    double pileUpWeight = 1.;
    if (weights_.encode().size() > 0) {
        edm::Handle<double> puWeight;
        iEvent.getByLabel(weights_, puWeight);
        pileUpWeight = *puWeight.product();
        if(iEvent.isRealData() || isnan(pileUpWeight)){
            pileUpWeight=1.;
        }
    }

    histo_->Fill(vertices->size(), pileUpWeight);

}


// ------------ method called once each job just before starting event loop  ------------
void 
MyVertexCountHisto::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MyVertexCountHisto::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
MyVertexCountHisto::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MyVertexCountHisto::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MyVertexCountHisto::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MyVertexCountHisto::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MyVertexCountHisto::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MyVertexCountHisto);
