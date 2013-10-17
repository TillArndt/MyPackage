// checkSelectionSaveFilters.cc
//
// Plugin to save information about event and event contents in a tree
//
// Created on Jan 27, 2010, 15:00
//

// system include files
#include <memory>
#include <map>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include <DataFormats/Candidate/interface/Candidate.h>
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include <DataFormats/Math/interface/deltaR.h>

#include <DataFormats/Common/interface/HLTGlobalStatus.h>
#include <FWCore/Common/interface/TriggerNames.h>
#include <DataFormats/Common/interface/TriggerResults.h>

#include "Math/Vector4D.h"
#include "TTree.h"
#include "TH1.h"
#include "TMath.h"
//
// class decleration
//

class CheckSelection : public edm::EDAnalyzer {
public:
  explicit CheckSelection(const edm::ParameterSet&);
  ~CheckSelection();

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  // ----------member data ---------------------------

  std::string processName_;
  std::vector<std::string> pathNames_;
  TH1F * cutflow_;
  int firstEvent_;
  edm::InputTag weights_;
};

//
// constructors and destructor
//
CheckSelection::CheckSelection(const edm::ParameterSet& conf):
  processName_( conf.getParameter< std::string >( "processName" )),
  pathNames_( conf.getParameter< std::vector< std::string > >( "pathNames" )),
  weights_(conf.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag()))
{
  firstEvent_=0;
}


CheckSelection::~CheckSelection()
{
}

// ------------ method called to for each event  ------------
void
CheckSelection::analyze(const edm::Event& event, const edm::EventSetup& setup)
{

  double weight = 1.;
  double pileupweight = 1.;
  if (weights_.encode().size() > 0) {
      edm::Handle<double> puWeight;
      event.getByLabel(weights_, puWeight);
      pileupweight = *puWeight.product();
      if(event.isRealData() || isnan(pileupweight)){
          pileupweight=1.;
      }
  }

  using namespace edm;
  using namespace pat;

  // use the TFileService
  edm::Service<TFileService> fs;

  // ***************save outcome of filters in branches**********************

  edm::TriggerResultsByName triggerResults = event.triggerResultsByName(processName_);
  uint numPathsSelected=pathNames_.size();
  uint numPaths=triggerResults.size();
  std::string substring="ModulePath";

  // it's not possible to do this in the begin job/contructor, as iEvent is not known there
  if(!firstEvent_){
    edm::LogInfo("CheckSelection")<<"Processing first Event. Initialize Cutflow histo."<<std::endl;
    cutflow_ = fs->make<TH1F> ("cutflow", ";cutflow;selected events / step", numPathsSelected , -0.5, numPathsSelected-0.5 );
    edm::LogInfo("CheckSelection")<<"BinRange: -0.5 - "<< numPathsSelected-0.5 <<std::endl;
    for(unsigned int j=0; j<numPathsSelected; j++){
	for(unsigned int i=0; i<numPaths; i++){
            std::string triggerName = triggerResults.triggerName(i);
         	if(triggerName==pathNames_[j]){
		  std::string binlabel=pathNames_[j];
		  if(triggerName.find(substring)!=std::string::npos){
	 	    binlabel = triggerName.replace( triggerName.find(substring), substring.size() , "");
		  }
		  cutflow_->GetXaxis()->SetBinLabel(j+1,TString(binlabel) );
		  edm::LogInfo("CheckSelection")<<"Setting bin name "<< binlabel<<" for bin j=  "<< j <<std::endl;
	        }
	        else{
	            edm::LogInfo("CheckSelection")<<"path "<< triggerName<< " was not selected."<<std::endl;
	        }
        }
    }
  }
  firstEvent_++;
  // loop over all filter results for every event
  edm::LogInfo("CheckSelection")<<"filling the firing filter" <<std::endl;
  bool fired=true;
  for(unsigned int i=0; i< numPathsSelected; i++) { //loop the bins
    if(fired){
      TString triggerName =pathNames_[i];
      edm::LogInfo("CheckSelection")<<"checking "<< triggerName <<std::endl;
      for(unsigned int j=0; j<numPaths; j++){
        if(triggerName==triggerResults.triggerName(j)){
          edm::LogInfo("CheckSelection")<<"filter selected "<< triggerName <<" and "<<triggerResults.triggerName(j) <<std::endl;
          if(!triggerResults.error(j) && triggerResults.accept(j)){
            edm::LogInfo("CheckSelection")<<"its firing " <<std::endl;

            cutflow_->Fill(i, weight);
            edm::LogInfo("CheckSelection")<<"path after btag cut fill with weight: "<< pileupweight <<std::endl;
            break;
          }
          else {
            edm::LogInfo("CheckSelection")<<"its not firing. "<<std::endl;
            fired=false;
            break;
          }
        }
      }
    }
  }
}

// ------------ method called once each job just before starting event loop  ------------
void
CheckSelection::beginJob()
{
  // call beginJob of RWTH 3B plugins (if necessary)

}

// ------------ method called once each job just after ending the event loop  ------------
void
CheckSelection::endJob()
{
  // call endJob of RWTH 3B plugins (if necessary)

}

//define this as a plug-in
DEFINE_FWK_MODULE(CheckSelection);