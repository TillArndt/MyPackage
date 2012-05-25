// -*- C++ -*-
//
// Package:    Two2SevenMerger
// Class:      Two2SevenMerger
// 
/**\class Two2SevenMerger Two2SevenMerger.cc MyPackage/Two2SevenMerger/src/Two2SevenMerger.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen
//         Created:  Wed May 23 20:38:31 CEST 2012
// $Id$
//
//


// system include files
#include <memory>
#include <vector>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//
// class declaration
//

class Two2SevenMerger : public edm::EDFilter {
   public:
      explicit Two2SevenMerger(const edm::ParameterSet&);
      ~Two2SevenMerger();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual bool beginRun(edm::Run&, edm::EventSetup const&);
      virtual bool endRun(edm::Run&, edm::EventSetup const&);
      virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
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
Two2SevenMerger::Two2SevenMerger(const edm::ParameterSet& iConfig)
{
   //edm::Service<TFileService> fs;
}


Two2SevenMerger::~Two2SevenMerger()
{
}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
Two2SevenMerger::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;
    using reco::GenParticle;

    // Why all this?
    // I want to sort out events, that have been simulated with ttgamma matrix element.

    Handle<vector<reco::GenParticle> > genParticles;
    iEvent.getByLabel(InputTag("genParticles"), genParticles);

    Handle<TtGenEvent> ttGenEvent;
    iEvent.getByLabel(InputTag("genEvt"), ttGenEvent);

    // if not semimuonic, this is surely not simulated in ttgamma ME
    if (!ttGenEvent->isTtBar()) return true;
    if (!ttGenEvent->isSemiLeptonic(WDecay::kMuon)) return true;

    // find legs and all particles
    vector<const GenParticle*> legs;
    vector<const GenParticle*> all;
    const GenParticle* gp = ttGenEvent->lepton();
    if (!gp) gp = ttGenEvent->leptonBar();
    legs.push_back(gp);
    all.push_back(gp);
    gp = ttGenEvent->leptonicDecayB();
    legs.push_back(gp);
    all.push_back(gp);
    gp = ttGenEvent->hadronicDecayB();
    legs.push_back(gp);
    all.push_back(gp);
    gp = ttGenEvent->hadronicDecayQuark();
    legs.push_back(gp);
    all.push_back(gp);
    gp = ttGenEvent->hadronicDecayQuarkBar();
    legs.push_back(gp);
    all.push_back(gp);
    all.push_back(ttGenEvent->leptonicDecayW());
    all.push_back(ttGenEvent->hadronicDecayW());
    const GenParticle* tlep = ttGenEvent->leptonicDecayTop();
    all.push_back(tlep);
    const GenParticle* thad = ttGenEvent->hadronicDecayTop();
    all.push_back(thad);

    cout << "thad->numberOfDaughters() " << thad->numberOfDaughters() << endl;



    // get interesting photons (where mom is quark)
    vector<reco::GenParticle>::const_iterator genPart = genParticles->begin();
    for ( ; genPart != genParticles->end(); ++genPart) {

        if (genPart->pdgId() == 22) {}
            //cout << genPart->pt() << endl;


    }
    return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
Two2SevenMerger::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
Two2SevenMerger::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
Two2SevenMerger::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
Two2SevenMerger::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
Two2SevenMerger::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
Two2SevenMerger::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
Two2SevenMerger::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(Two2SevenMerger);
