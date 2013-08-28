// -*- C++ -*-
//
// Package:    MyPhotonUserDataAdder
// Class:      MyPhotonUserDataSCFootRm
// 
/**\class MyPhotonUserDataSCFootRm MyPhotonUserDataSCFootRm.cc MyPackage/MyPhotonUserDataAdder/src/MyPhotonUserDataSCFootRm.cc

 Description: Adds user data to pat::Photon, that cannot be added on configuration level.

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen
//         Created:  Tue Feb 12 16:37:52 CET 2013
// $Id: MyPhotonUserDataSCFootRm.cc,v 1.2 2013/08/28 07:51:24 htholen Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "PFIsolation/SuperClusterFootprintRemoval/interface/SuperClusterFootprintRemoval.h"

class MyPhotonUserDataSCFootRm : public edm::EDProducer {
   public:
      explicit MyPhotonUserDataSCFootRm(const edm::ParameterSet&);
      ~MyPhotonUserDataSCFootRm();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event& evt, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
      edm::InputTag _srcPhoton;
};

MyPhotonUserDataSCFootRm::MyPhotonUserDataSCFootRm(const edm::ParameterSet& cfg) :
    _srcPhoton(cfg.getParameter<edm::InputTag>( "srcPhoton" ))
{
  produces<std::vector<pat::Photon> >();
}

MyPhotonUserDataSCFootRm::~MyPhotonUserDataSCFootRm()
{
}

void
MyPhotonUserDataSCFootRm::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;
    Handle<vector<pat::Photon> > photons;
    iEvent.getByLabel(_srcPhoton, photons);

    SuperClusterFootprintRemoval remover(iEvent,iSetup);
    // this is the index of the vertex selected in the event
    static const int vertexforchargediso = 0;

    auto_ptr<vector<pat::Photon> > photonColl( new vector<pat::Photon> (*photons) );
    for (unsigned int i = 0; i< photonColl->size();++i) {
        pat::Photon & ph = (*photonColl)[i];

        ////////////////////////////////////////////// SC footprint removal ///
        reco::SuperClusterRef scref(ph.superCluster());
        ph.addUserFloat("chargedisoSCfootRm", remover.PFIsolation("charged",scref,vertexforchargediso));
        ph.addUserFloat("neutralisoSCfootRm", remover.PFIsolation("neutral",scref));
        ph.addUserFloat("photonisoSCfootRm",  remover.PFIsolation("photon",scref));
    }

    iEvent.put( photonColl);
}

// ------------ method called once each job just before starting event loop  ------------
void 
MyPhotonUserDataSCFootRm::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MyPhotonUserDataSCFootRm::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
MyPhotonUserDataSCFootRm::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MyPhotonUserDataSCFootRm::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MyPhotonUserDataSCFootRm::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MyPhotonUserDataSCFootRm::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MyPhotonUserDataSCFootRm::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MyPhotonUserDataSCFootRm);
