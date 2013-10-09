// -*- C++ -*-
//
// Package:    TopPtProducer
// Class:      TopPtProducer
// 
/**\class TopPtProducer TopPtProducer.cc MyPackage/TopPtProducer/src/TopPtProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Heiner Tholen,32 4-B20,+41227676487,
//         Created:  Mon Aug 19 15:44:44 CEST 2013
// $Id$
//
//


// system include files
#include <memory>
#include <vector>
#include <math.h>
#include <TH1D.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//
// class declaration
//

class TopPtProducer : public edm::EDProducer {
   public:
      explicit TopPtProducer(const edm::ParameterSet&);
      ~TopPtProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
      bool two2fiveMode_;
      TH1D *massTop_;
      TH1D *massAntiTop_;
      TH1D *hypo_;
};

//
// constructors and destructor
//
TopPtProducer::TopPtProducer(const edm::ParameterSet& iConfig):
    two2fiveMode_(iConfig.getUntrackedParameter<bool>("two2fiveMode",false))
{
    edm::Service<TFileService> fs;
    if (two2fiveMode_) {
        massTop_      = fs->make<TH1D>("massTop",       ";top quark mass / GeV;events", 150, 100., 250.);
        massAntiTop_  = fs->make<TH1D>("massAntiTop",   ";anti-top quark mass / GeV;events", 150, 100., 250.);
        hypo_         = fs->make<TH1D>("hypothesis",   ";hypothesis;events", 3, 0.5, 3.5);
    }
    produces<double>("ptTop");
    produces<double>("ptAntiTop");
}

TopPtProducer::~TopPtProducer()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
TopPtProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace reco;
    using namespace reco;
    using namespace std;

    double ptTop        = 0.;
    double ptAntiTop    = 0.;
    Handle<vector<GenParticle> > gens;
    iEvent.getByLabel(InputTag("genParticles"), gens);

    if (two2fiveMode_) {
        // get final state particles (it's 5 final states)
        GenParticle Wp, Wm, b, bbar, gam;
        for (vector<GenParticle>::const_iterator gp = gens->begin(); gp != gens->end(); ++gp){
            if (gp->numberOfDaughters() == 5) {
                for (int i = 0; i < 5; ++i) {
                    GenParticle * dau = (GenParticle*) gp->daughter(i);
                    if (abs(dau->pdgId()) == 22)
                        gam = *dau;
                    else if (dau->pdgId() == 24)
                        Wp = *dau;
                    else if (dau->pdgId() == -24)
                        Wm = *dau;
                    else if (dau->pdgId() == 5)
                        b = *dau;
                    else if (dau->pdgId() == -5)
                        bbar = *dau;
                }

                // find photon association closest to top masses
                // hypo 1: photon radiated of initial state
                // hypo 2: photon coming from t decay
                // hypo 3: photon coming from tbar decay
                static const double TOPMASS = 172.5;

                Candidate::LorentzVector hyp1t_vec      = Wp.p4() + b.p4();
                Candidate::LorentzVector hyp1tbar_vec   = Wm.p4() + bbar.p4();
                double hyp1T_dev       = fabs(hyp1t_vec.M() - TOPMASS);
                double hyp1Tbar_dev    = fabs(hyp1tbar_vec.M() - TOPMASS);
                double hyp1DevSum      = hyp1T_dev + hyp1Tbar_dev;

                Candidate::LorentzVector hyp2t_vec      = hyp1t_vec + gam.p4();
                Candidate::LorentzVector hyp2tbar_vec   = hyp1tbar_vec;
                double hyp2T_dev       = fabs(hyp2t_vec.M() - TOPMASS);
                double hyp2DevSum      = hyp2T_dev + hyp1Tbar_dev;

                Candidate::LorentzVector hyp3t_vec      = hyp1t_vec;
                Candidate::LorentzVector hyp3tbar_vec   = hyp1tbar_vec + gam.p4();
                double hyp3Tbar_dev    = fabs(hyp3tbar_vec.M() - TOPMASS);
                double hyp3DevSum      = hyp1T_dev + hyp3Tbar_dev;

                // find the smallest mass deviation solution / assign pt's / record masses
                if (hyp1DevSum < hyp2DevSum && hyp1DevSum < hyp3DevSum) {
                    if (hyp1DevSum < 50.) {
                        hypo_->Fill(1.);
                        ptTop       = hyp1t_vec.pt();
                        ptAntiTop   = hyp1tbar_vec.pt();
                        massTop_->Fill(hyp1t_vec.M());
                        massAntiTop_->Fill(hyp1tbar_vec.M());
                    }
                } else if (hyp2DevSum < hyp3DevSum) {
                    if (hyp2DevSum < 50.) {
                        hypo_->Fill(2.);
                        ptTop       = hyp2t_vec.pt();
                        ptAntiTop   = hyp2tbar_vec.pt();
                        massTop_->Fill(hyp2t_vec.M());
                        massAntiTop_->Fill(hyp2tbar_vec.M());
                    }
                } else {
                    if (hyp3DevSum < 50.) {
                        hypo_->Fill(3.);
                        ptTop       = hyp3t_vec.pt();
                        ptAntiTop   = hyp3tbar_vec.pt();
                        massTop_->Fill(hyp3t_vec.M());
                        massAntiTop_->Fill(hyp3tbar_vec.M());
                    }
                }

                break; // done..
            }
        }


    } else {
        // get top quarks
        GenParticle local_top;
        GenParticle local_topBar;
        const GenParticle* top      = 0;
        const GenParticle* topBar   = 0;
        for (vector<GenParticle>::const_iterator i = gens->begin(); i != gens->end(); ++i){
             if (!top && i->pdgId() ==  6) {
                local_top = *i;
                top = &local_top;
             }
             if (!topBar && i->pdgId() == -6) {
                local_topBar = *i;
                topBar = &local_topBar;
             }
             if (top && topBar) break;
        }

        // get top pt
        ptTop       = local_top.pt();
        ptAntiTop   = local_topBar.pt();
    }


    // write out
    auto_ptr<double> ptTop_ptr(new double);
    auto_ptr<double> ptAntiTop_ptr(new double);
    *ptTop_ptr = ptTop;
    *ptAntiTop_ptr = ptAntiTop;
    iEvent.put(ptTop_ptr, "ptTop");
    iEvent.put(ptAntiTop_ptr, "ptAntiTop");
}

// ------------ method called once each job just before starting event loop  ------------
void 
TopPtProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TopPtProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
TopPtProducer::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TopPtProducer::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TopPtProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TopPtProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TopPtProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TopPtProducer);
