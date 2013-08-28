// -*- C++ -*-
//
// Package:    MyPhotonUserDataLargestPdgId
// Class:      MyPhotonUserDataLargestPdgId
// 
/**\class MyPhotonUserDataLargestPdgId MyPhotonUserDataLargestPdgId.cc MyPackage/MyPhotonUserDataAdder/src/MyPhotonUserDataLargestPdgId.cc

 Description: Adds user data to pat::Photon, that cannot be added on configuration level.

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen
//         Created:  Tue Feb 12 16:37:52 CET 2013
// $Id: MyPhotonUserDataLargestPdgId.cc,v 1.1 2013/08/03 16:18:01 htholen Exp $
//
//


// system include files
#include <memory>
#include <map>
#include <sstream>
#include <TH1.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "PFIsolation/SuperClusterFootprintRemoval/interface/SuperClusterFootprintRemoval.h"

class MyPhotonUserDataLargestPdgId : public edm::EDProducer {
   public:
      explicit MyPhotonUserDataLargestPdgId(const edm::ParameterSet&);
      ~MyPhotonUserDataLargestPdgId();

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
      std::map<int, int> _largestPdgIds;
};

MyPhotonUserDataLargestPdgId::MyPhotonUserDataLargestPdgId(const edm::ParameterSet& cfg) :
    _srcPhoton(cfg.getParameter<edm::InputTag>( "srcPhoton" ))
{
  produces<std::vector<pat::Photon> >();
}

MyPhotonUserDataLargestPdgId::~MyPhotonUserDataLargestPdgId()
{
}

void
MyPhotonUserDataLargestPdgId::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
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

        ////////////////////////////////////////////// largestAncestorPdgId ///
        // mc truth: find largest ancestor pdg id
        int largestPdgId = 0;
        if (!iEvent.isRealData() && ph.genParticlesSize() > 0) {
            const reco::GenParticle *gp = ph.genParticle();
            do {
                int pdgId = abs(gp->pdgId());
                if (largestPdgId < pdgId) {
                    largestPdgId = pdgId;
                }
                gp = (const reco::GenParticle*) gp->mother();
            } while (gp->numberOfMothers() > 0);
            // the last one (proton) is not looked at...
        }
        ph.addUserFloat("largestAncestorPdgId", largestPdgId);
        _largestPdgIds[largestPdgId]++;

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
MyPhotonUserDataLargestPdgId::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MyPhotonUserDataLargestPdgId::endJob() {
    edm::Service<TFileService> fs;
    TH1D* pdgHisto = fs->make<TH1D>(
        "largestAncestorPdgId",
        ";largest pdg ID among ancestors;number of photons",
        _largestPdgIds.size(), -.5, _largestPdgIds.size() + .5);
    std::map<int, int>::iterator iter;
    for (iter = _largestPdgIds.begin(); iter != _largestPdgIds.end(); ++iter) {
        std::stringstream stream;
        stream << iter->first;
        pdgHisto->Fill(stream.str().c_str(), iter->second);
    }
}

// ------------ method called when starting to processes a run  ------------
void 
MyPhotonUserDataLargestPdgId::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MyPhotonUserDataLargestPdgId::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MyPhotonUserDataLargestPdgId::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MyPhotonUserDataLargestPdgId::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MyPhotonUserDataLargestPdgId::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MyPhotonUserDataLargestPdgId);
