// -*- C++ -*-
//
// Package:    MyPhotonUserDataAdder
// Class:      MyPhotonUserDataAdder
// 
/**\class MyPhotonUserDataAdder MyPhotonUserDataAdder.cc MyPackage/MyPhotonUserDataAdder/src/MyPhotonUserDataAdder.cc

 Description: Adds user data to pat::Photon, that cannot be added on configuration level.

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen
//         Created:  Tue Feb 12 16:37:52 CET 2013
// $Id: MyPhotonUserDataAdder.cc,v 1.2 2013/04/30 08:57:36 kuessel Exp $
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
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "DataFormats/Provenance/interface/Provenance.h"
#include "EGamma/EGammaAnalysisTools/src/PFIsolationEstimator.cc"

class MyPhotonUserDataAdder : public edm::EDProducer {
   public:
      explicit MyPhotonUserDataAdder(const edm::ParameterSet&);
      ~MyPhotonUserDataAdder();

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
      edm::InputTag _srcPhoton, _srcJet4rho, _srcElectron, _srcConversion, _srcBeamSpot, _srcPFColl, _srcVertices ;
      PFIsolationEstimator isolator;
};

MyPhotonUserDataAdder::MyPhotonUserDataAdder(const edm::ParameterSet& cfg) :
    _srcPhoton(cfg.getParameter<edm::InputTag>( "srcPhoton" )),
    _srcJet4rho(cfg.getParameter<edm::InputTag>( "srcJet4rho" )),
    _srcElectron(cfg.getParameter<edm::InputTag>( "srcElectron" )),
    _srcConversion(cfg.getParameter<edm::InputTag>( "srcConversion" )),
    _srcBeamSpot(cfg.getParameter<edm::InputTag>( "srcBeamSpot" )),
    _srcPFColl(cfg.getParameter<edm::InputTag>( "srcPFColl" )),
    _srcVertices(cfg.getParameter<edm::InputTag>( "srcVertices" ))
{
  isolator.initializePhotonIsolation(kTRUE);
  produces<std::vector<pat::Photon> >();
}

MyPhotonUserDataAdder::~MyPhotonUserDataAdder()
{
}

void
MyPhotonUserDataAdder::produce(edm::Event& evt, const edm::EventSetup&)
{
    using namespace edm;
    using namespace std;
    Handle<vector<pat::Photon> > photons;
    evt.getByLabel(_srcPhoton, photons);

    edm::Handle<vector<reco::PFCandidate> > pfColl;
    evt.getByLabel(_srcPFColl, pfColl);

    edm::Handle< reco::VertexCollection > vertices;
    evt.getByLabel(_srcVertices, vertices);

// TODO: get rho correction done
//    Handle<vector<pat::Jet> > jet4rho;
//    evt.getByLabel(_srcJet4rho, jet4rho);

    Handle<vector<pat::Electron> > electrons;
    evt.getByLabel(_srcElectron, electrons);

    Handle<vector<reco::Conversion> > conversions;
    evt.getByLabel(_srcConversion, conversions);

    Handle<reco::BeamSpot> beamSpot;
    evt.getByLabel(_srcBeamSpot, beamSpot);

    auto_ptr<vector<pat::Photon> > photonColl( new vector<pat::Photon> (*photons) );
    vector<reco::GsfElectron> gsfEleVec;
    Provenance prov;
    Handle<vector<reco::GsfElectron> > electronColl(&gsfEleVec, &prov);
    for (unsigned int i = 0; i< electrons->size();++i) {
        gsfEleVec.push_back((reco::GsfElectron) electrons->at(i));
    }
    for (unsigned int i = 0; i< photonColl->size();++i) {
        pat::Photon & ph = (*photonColl)[i];
        bool passelectronveto = !ConversionTools::hasMatchedPromptElectron(
                    ph.superCluster(),
                    electronColl,
                    conversions,
                    beamSpot->position()
        );
        if (passelectronveto) {
            ph.addUserFloat("passEleVeto", 1.);
        } else {
            ph.addUserFloat("passEleVeto", 0.);
        }
	//isolator.fGetIsolation( ph, &pfColl, (*vertices)[0], vertices);
	//cout<<"PF  charged:  "<<isolator.getIsolationCharged()<<" photon: "<<isolator.getIsolationPhoton()<<" neutral: "<<isolator.getIsolationNeutral()<<endl;
	//cout<<"PATPF  charged:  "<<ph.chargedHadronIso() <<" photon: "<<ph.photonIso()<<" neutral: "<<ph.neutralHadronIso()<<endl;
    }
    evt.put( photonColl);



/* this is an EventSetup example
   //Read SetupData from the SetupRecord in the EventSetup
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
*/
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
MyPhotonUserDataAdder::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MyPhotonUserDataAdder::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
MyPhotonUserDataAdder::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MyPhotonUserDataAdder::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MyPhotonUserDataAdder::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MyPhotonUserDataAdder::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MyPhotonUserDataAdder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MyPhotonUserDataAdder);
