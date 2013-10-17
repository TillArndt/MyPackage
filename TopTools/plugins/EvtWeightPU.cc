// -*- C++ -*-
//
// Package:    EvtWeightPU
// Class:      EvtWeightPU
// 
/**\class EvtWeightPU EvtWeightPU.cc YKuessel/EvtWeightPU/src/EvtWeightPU.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Yvonne Kuessel
//         Created:  Sun Dec  4 17:31:36 CET 2011
// $Id: EvtWeightPU.cc,v 1.6 2013/08/03 16:18:31 htholen Exp $
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
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"


//
// class declaration
//

class EvtWeightPU : public edm::EDProducer {
   public:
      explicit EvtWeightPU(const edm::ParameterSet&);
      ~EvtWeightPU();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      std::string generatedFile_;
      std::string dataFile_;
      std::string GenHistName_;
      std::string DataHistName_;
      edm::LumiReWeighting LumiWeights_;
      bool isMCatNLO_;
      edm::InputTag genInfo_;
      edm::InputTag weights_;
      bool emptyWeightInputTag_;
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
EvtWeightPU::EvtWeightPU(const edm::ParameterSet& iConfig):	 
	generatedFile_(iConfig.getParameter<std::string>("generatedFile")),  
	dataFile_(iConfig.getParameter<std::string>("dataFile")),
	GenHistName_(iConfig.getParameter<std::string>("GenHistName")),  
	DataHistName_(iConfig.getParameter<std::string>("DataHistName")),
	isMCatNLO_(iConfig.getUntrackedParameter<bool>("isMCatNLO", false)),
	genInfo_(edm::InputTag("generator")),
	weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag())),
	emptyWeightInputTag_(weights_.encode() == std::string(""))
{
    produces<double>("PUWeight");
    produces<double>("PUWeightTrue");

    LumiWeights_ = edm::LumiReWeighting(generatedFile_,dataFile_,GenHistName_ , DataHistName_);
}


EvtWeightPU::~EvtWeightPU()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
EvtWeightPU::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  const edm::EventBase* iEventB = dynamic_cast<edm::EventBase*>(&iEvent);

  double MyPileUpWeight =1.;
  double MyPileUpWeightTrue=1.;

  if(!iEvent.isRealData()){
    MyPileUpWeight = LumiWeights_.weight( (*iEventB) );
    Handle<std::vector< PileupSummaryInfo > >  PupInfo;
    iEvent.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);
    std::vector<PileupSummaryInfo>::const_iterator PVI;

    float Tnpv = -1;
    for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {

       int BX = PVI->getBunchCrossing();
       if(BX == 0) { 
          Tnpv = PVI->getTrueNumInteractions();
          continue;
       }
    }
    MyPileUpWeightTrue = LumiWeights_.weight( Tnpv );

    if (isMCatNLO_) {
       Handle<GenEventInfoProduct> genInfoHndl;
       iEvent.getByLabel(genInfo_, genInfoHndl);

       double weight = genInfoHndl->weight();
       int mcSign = weight/abs(weight);
       MyPileUpWeight     *= mcSign;
       MyPileUpWeightTrue *= mcSign;
       edm::LogInfo("EvtWeightPU")<<"mcSign="<<mcSign<<std::endl;
    }
    edm::LogInfo("EvtWeightPU")<<"MyPileUpWeight="<<MyPileUpWeight<<std::endl;
    edm::LogInfo("EvtWeightPU")<<"MyPileUpWeightTrue="<<MyPileUpWeightTrue<<std::endl;

    // if chained to prior weight function
    if (!emptyWeightInputTag_) {
      float weight = 1.;
      edm::Handle<double> weightHandle;
      iEvent.getByLabel(weights_, weightHandle);
      weight = *weightHandle.product();
      if (isnan(weight)) {
        weight = 1.;
      }
      MyPileUpWeight        *= weight;
      MyPileUpWeightTrue    *= weight;
    }
  }

  // store in event
  std::auto_ptr<double> puEventWeight(new double);
  *puEventWeight = MyPileUpWeight;      
  iEvent.put(puEventWeight,"PUWeight");  
  std::auto_ptr<double> puEventWeightTrue(new double);
  *puEventWeightTrue = MyPileUpWeightTrue;  
  iEvent.put(puEventWeightTrue,"PUWeightTrue"); 

}

// ------------ method called once each job just before starting event loop  ------------
void 
EvtWeightPU::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EvtWeightPU::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
EvtWeightPU::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
EvtWeightPU::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
EvtWeightPU::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
EvtWeightPU::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EvtWeightPU::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(EvtWeightPU);
