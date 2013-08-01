
// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/ServiceRegistry/interface/Service.h"

#include <map>
#include <string>
#include "TVector3.h"
// #include "Math/VectorUtil.h" 

#include "TTree.h"
#include "TH1F.h"
#include "TH2.h"
#include <TString.h>
#include "TMath.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include <DataFormats/BTauReco/interface/SoftLeptonTagInfo.h>
#include <DataFormats/TrackReco/interface/Track.h>
#include <DataFormats/BTauReco/interface/SoftLeptonTagInfo.h>
#include "Math/Vector4D.h"
#include <sstream>
#include "TProfile.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include <DataFormats/JetReco/interface/GenJet.h>
#include "AnalysisDataFormats/TopObjects/interface/TtSemiLeptonicEvent.h"
#include "AnalysisDataFormats/TopObjects/interface/TtSemiLepEvtPartons.h"
#include "TGraphAsymmErrors.h"
#include "MyPackage/CheckObjects/interface/checkObject.h"

checkObject::checkObject(const edm::ParameterSet& conf):
  hists_(),
  bTagAlgorithm_(conf.getParameter<std::string>("bTagAlgorithm")),
  srcObjects_(conf.getParameter<edm::InputTag>("srcObjects")),
  srcPUWeight_(conf.getParameter<edm::InputTag> ("srcPUWeight")),
  objectType_(conf.getParameter<std::string>("objectType"))
{
  edm::Service<TFileService> fs;
  std::string type(";");
  if(objectType_=="patJet"){
    type = ";jets: ";
  }
  if(objectType_=="patMuon"){
    type = ";muon: ";
  }

  // book histograms:
  hists_["Mult"]=fs->make<TH1F>("Mult"      , (type+"multiplicity;          Count"      ).c_str()  ,  16, -0.5,  15.5);
  hists_["Charge"]=fs->make<TH1F>("Charge"  , (type+"charge;                Count"      ).c_str()  ,  20 , -1.5, 1.5);
  hists_["Pt"  ]=fs->make<TH1F>("Pt"        , (type+"p_{T} / GeV;           Count"      ).c_str()  ,  50, 0., 150.);
  hists_["1Pt"  ]=fs->make<TH1F>("1Pt"      , (type+"1^{st} leading,  p_{T} / GeV;Count").c_str()  ,  50, 0., 250.);
  hists_["2Pt"  ]=fs->make<TH1F>("2Pt"      , (type+"2^{nd} leading,  p_{T} / GeV;Count").c_str()  ,  50, 0., 250.);
  hists_["3Pt"  ]=fs->make<TH1F>("3Pt"      , (type+"3^{rd} leading,  p_{T} / GeV;Count").c_str()  ,  50, 0., 200.);
  hists_["4Pt"  ]=fs->make<TH1F>("4Pt"      , (type+"4^{th} leading,  p_{T} / GeV;Count").c_str()  ,  50, 0., 200.);
  hists_["5Pt"  ]=fs->make<TH1F>("5Pt"      , (type+"5^{th} leading,  p_{T} / GeV;Count").c_str()  ,  50, 0., 200.);
  hists_["Eta"  ]=fs->make<TH1F>("Eta"      , (type+"#eta;                  Count"      ).c_str()  ,  50, -3., 3.);
  hists_["1Eta"  ]=fs->make<TH1F>("1Eta"    , (type+"1^{st} leading,  #eta; Count"      ).c_str()  ,  50, -3., 3.);
  hists_["2Eta"  ]=fs->make<TH1F>("2Eta"    , (type+"2^{nd} leading,  #eta; Count"      ).c_str()  ,  50, -3., 3.);
  hists_["3Eta"  ]=fs->make<TH1F>("3Eta"    , (type+"3^{rd} leading,  #eta; Count"      ).c_str()  ,  50, -3., 3.);
  hists_["4Eta"  ]=fs->make<TH1F>("4Eta"    , (type+"4^{th} leading,  #eta; Count"      ).c_str()  ,  50, -3., 3.);
  hists_["5Eta"  ]=fs->make<TH1F>("5Eta"    , (type+"5^{th} leading,  #eta; Count"      ).c_str()  ,  50, -3., 3.);
  hists_["Phi"  ]=fs->make<TH1F>("Phi"      , (type+"#phi;                  Count"      ).c_str()  ,  50, -3.2, 3.2);
  hists_["1Phi"  ]=fs->make<TH1F>("1Phi"    , (type+"1^{st} leading,  #phi; Count"      ).c_str()  ,  50, -3.2, 3.2);
  hists_["2Phi"  ]=fs->make<TH1F>("2Phi"    , (type+"2^{nd} leading,  #phi; Count"      ).c_str()  ,  50, -3.2, 3.2);
  hists_["3Phi"  ]=fs->make<TH1F>("3Phi"    , (type+"3^{rd} leading,  #phi; Count"      ).c_str()  ,  50, -3.2, 3.2);
  hists_["4Phi"  ]=fs->make<TH1F>("4Phi"    , (type+"4^{th} leading,  #phi; Count"      ).c_str()  ,  50, -3.2, 3.2);
  hists_["5Phi"  ]=fs->make<TH1F>("5Phi"    , (type+"5^{th} leading,  #phi; Count"      ).c_str()  ,  50, -3.2, 3.2);
  hists_["Btag"  ]=fs->make<TH1F>("Btag"    , (type+"b-tag;                 Count"      ).c_str()  ,  50, -1., 10.);
  hists_["1Btag"  ]=fs->make<TH1F>("1Btag"  , (type+"1^{st} leading,  b-tag;Count"      ).c_str()  ,  50, -1., 10.);
  hists_["2Btag"  ]=fs->make<TH1F>("2Btag"  , (type+"2^{nd} leading,  b-tag;Count"      ).c_str()  ,  50, -1., 10.);
  hists_["3Btag"  ]=fs->make<TH1F>("3Btag"  , (type+"3^{rd} leading,  b-tag;Count"      ).c_str()  ,  50, -1., 10.);
  hists_["4Btag"  ]=fs->make<TH1F>("4Btag"  , (type+"4^{th} leading,  b-tag;Count"      ).c_str()  ,  50, -1., 10.);
  hists_["5Btag"  ]=fs->make<TH1F>("5Btag"  , (type+"5^{th} leading,  b-tag;Count"      ).c_str()  ,  50, -1., 10.);

}


checkObject::~checkObject()
{
}



// ------------ method called to for each event  ------------
void
checkObject::analyze(const edm::Event& event, const edm::EventSetup& setup)
{
  using namespace edm;
  using namespace std;

  //***********************************************
  //  Input
  //***********************************************
   
  edm::Handle<edm::View<pat::Jet> > jets;
  edm::Handle<edm::View<pat::Muon> > muons;
  edm::Handle<edm::View<pat::Photon> > photons;
  edm::Handle<edm::View<pat::Electron> > electrons;
  edm::Handle<edm::View<reco::GenParticle> > genparticles;
  edm::Handle<double> puWeight;
  event.getByLabel(srcPUWeight_, puWeight);
  double weight= *puWeight.product();
  edm::LogInfo("checkCorrs")<<"pileUpWeight="<<weight<<std::endl;
  if(event.isRealData()){
    weight=1;
  }
  
  //***********************************************
  //  analyze the objects
  //***********************************************

  if(objectType_=="patJet"){
    event.getByLabel(srcObjects_, jets);   
    analyzeCollection(jets, weight);
  }
  if(objectType_=="patMuon"){
    event.getByLabel(srcObjects_, muons);   
    analyzeCollection(muons, weight);
  }
  if(objectType_=="patElectron"){
    event.getByLabel(srcObjects_, electrons);   
    analyzeCollection(electrons, weight);
  }
  if(objectType_=="patPhoton"){
    event.getByLabel(srcObjects_, photons);   
    analyzeCollection(photons, weight);
  }
  if(objectType_=="recoGenParticle"){
    event.getByLabel(srcObjects_, genparticles);   
    analyzeCollection(genparticles, weight);
  }

}

				       
				
// ------------ method called once each job just before starting event loop  ------------
void 
checkObject::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
checkObject::endJob() 
{
}

//define this as a plug-in
DEFINE_FWK_MODULE(checkObject);
