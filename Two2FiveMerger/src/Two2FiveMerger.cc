// -*- C++ -*-
//
// Package:    Two2FiveMerger
// Class:      Two2FiveMerger
// 
/**\class Two2FiveMerger Two2FiveMerger.cc MyPackage/Two2FiveMerger/src/Two2FiveMerger.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen
//         Created:  Wed May 23 20:38:31 CEST 2012
// $Id: Two2FiveMerger.cc,v 1.3 2012/06/05 22:09:46 htholen Exp $
//
//


// system include files
#include <memory>
#include <vector>
#include <iostream>
#include <TH1D.h>

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
#include "DataFormats/Math/interface/deltaR.h"

//
// class declaration
//

class Two2FiveMerger : public edm::EDFilter {
   public:
      explicit Two2FiveMerger(const edm::ParameterSet&);
      ~Two2FiveMerger();

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

      const double ptCut_;
      const double drCut_;
      const double legPtCut_;
      const bool is2to5_;
      TH1D *kickedPhotons_;
      TH1D *survivingPhotons_;
      TH1D *allPhotons_;
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
Two2FiveMerger::Two2FiveMerger(const edm::ParameterSet& iConfig) :
    ptCut_(iConfig.getParameter<double>("ptCut")),
    drCut_(iConfig.getParameter<double>("drCut")),
    legPtCut_(iConfig.getUntrackedParameter<double>("legPtCut", 0.)),
    is2to5_(iConfig.getUntrackedParameter<bool>("is2to5", false))
{
    edm::Service<TFileService> fs;
    kickedPhotons_      = fs->make<TH1D>("kickedPhotons",    ";photon e_{T} / GeV;number of photons", 70, 0., 700.);
    survivingPhotons_   = fs->make<TH1D>("survivingPhotons", ";photon e_{T} / GeV;number of photons", 70, 0., 700.);
    allPhotons_         = fs->make<TH1D>("allPhotons",       ";photon e_{T} / GeV;number of photons", 70, 0., 700.);
}


Two2FiveMerger::~Two2FiveMerger()
{
}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
Two2FiveMerger::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;
    using reco::GenParticle;
    using reco::deltaR;

    // Why all this?
    // I want to sort out events, that have been simulated with ttgamma matrix element.

    Handle<vector<reco::GenParticle> > genParticles;
    iEvent.getByLabel(InputTag("genParticles"), genParticles);

    Handle<TtGenEvent> ttGenEvent;
    iEvent.getByLabel(InputTag("genEvt"), ttGenEvent);

    // cannot treat non-ttbar at the moment
    if (!ttGenEvent->isTtBar()) return true;

    // find legs and all relevant particles
    vector<const GenParticle*> legs;
    vector<const GenParticle*> all;
    const GenParticle* top    = ttGenEvent->top();
    const GenParticle* topBar = ttGenEvent->topBar();
    if (is2to5_) {
        for (unsigned i = 0; i < top->numberOfDaughters(); ++i) {
            const GenParticle* gp = (GenParticle*) top->daughter(i);
            if (abs(gp->pdgId()) < 6 || abs(gp->pdgId()) == 24) {
                legs.push_back(gp);
                all.push_back(gp);
            }
        }
        for (unsigned i = 0; i < topBar->numberOfDaughters(); ++i) {
            const GenParticle* gp = (GenParticle*) topBar->daughter(i);
            if (abs(gp->pdgId()) < 6 || abs(gp->pdgId()) == 24) {
                legs.push_back(gp);
                all.push_back(gp);
            }
        }
    } else {
        legs.push_back(top);
        legs.push_back(topBar);
    }
    all.push_back(top);
    all.push_back(topBar);
    for (unsigned i = 0; i < top->numberOfMothers(); ++i)
        all.push_back((GenParticle*)top->mother(i));
    for (unsigned i = 0; i < topBar->numberOfMothers(); ++i)
        all.push_back((GenParticle*)topBar->mother(i));

    // check legs pt cut (which is 0. by default)
    if (legPtCut_ > 1e-43 && is2to5_) {
        for (unsigned i = 0; i < legs.size(); ++i) {
            // W boson doesn't count
            if (legs.at(i)->pt() < legPtCut_ && abs(legs.at(i)->pdgId()) != 24)
                return true;
        }
    }

    // find relevant photons
    vector<const GenParticle*> photons;
    for (unsigned i = 0; i < all.size(); ++i) {
        for (unsigned j = 0; j < all.at(i)->numberOfDaughters(); ++j) {
            const GenParticle* daughter = (const GenParticle*) all.at(i)->daughter(j);
            if (abs(daughter->pdgId()) == 22) {
                 photons.push_back(daughter);
                 allPhotons_->Fill(daughter->et());
            }
        }
    }

    // sort out fails (photons must fulfill both cuts)
    bool foundNoDrUnderCut = true;
    for (unsigned i = 0; i < photons.size(); ++i) {
        const GenParticle* photon = photons.at(i);
        if (photon->pt() > ptCut_) {
            for (unsigned j = 0; j < legs.size(); ++j) {
                const GenParticle* leg = legs.at(j);
                if (deltaR(*photon, *leg) < drCut_) {
                    foundNoDrUnderCut = false;
                    cout << "<Two2FiveMerger>: removing Event! "
                         << "Photon pt < ptCut: (" << photon->pt() << " > " << ptCut_
                         << ") and no deltaR to a leg smaller than " << drCut_ << endl;
                    break;
                }
            }
        }
    }

    if (photons.size() && foundNoDrUnderCut) {
        for (unsigned i = 0; i < photons.size(); ++i)
            kickedPhotons_->Fill(photons.at(i)->et());
        return false;
    } else {
        for (unsigned i = 0; i < photons.size(); ++i)
            survivingPhotons_->Fill(photons.at(i)->et());
    }
    return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
Two2FiveMerger::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
Two2FiveMerger::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
Two2FiveMerger::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
Two2FiveMerger::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
Two2FiveMerger::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
Two2FiveMerger::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
Two2FiveMerger::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(Two2FiveMerger);
