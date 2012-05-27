__author__ = 'tholen'

import FWCore.ParameterSet.Config as cms

def get_weights(input_dir):

    puWeight=cms.EDProducer("EvtWeightPU",
        weights=cms.string(input_dir + "TopCharge/Weight3D_2.root"),
        PUInputFileMC=cms.string(input_dir + "MC_ReweightInput.root"),
        PUInputFileData=cms.string(input_dir + "pileupFiles4_6fb/Merged2_PileupTruth_FineBin_4_6_fb.root"),
        PUInputFileDataBX1=cms.string(input_dir + "pileupFiles_1BXOption/Merged_Pileup_4_6_fb.root"),
        PUInputHistoMC=cms.string("pileup_Data_Flat10Tail"),
        PUInputHistoMCBX1=cms.string("pileup_Data_SpikeSmear"),
        PUInputHistoData=cms.string("pileup")
    )
    return puWeight