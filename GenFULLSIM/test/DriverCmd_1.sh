
cmsDriver.py MyPackage/GenFULLSIM/python/Hadronizer_TuneZ2star_8TeV_generic_LHE_pythia_tauola_cff.py \
--step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:7E33v2 \
--conditions START53_V7A::All \
--pileup 2012_Summer_50ns_PoissonOOTPU \
--datamix NODATAMIXER \
--eventcontent RAWSIM \
--datatier RAWSIM \
--no_exec \
--fileout out_STEP1.root \
--filein /store/user/htholen/LHE2EDM_WHIZARD_2to5_ttA/LHE2EDM_WHIZARD_2to5_ttA/48c4bb9326314478036b3ab92a9a4664/LHEtoEDM_NONE_181_1_X3P.root \
-n -1 \


#--beamspot Realistic8TeVCollision \
#--step GEN,DIGI,L1,DIGI2RAW,HLT:7E33v2 \
#--beamspot Realistic8TeV2012Collision \
#  --python_filename config_step1_cfg.py \
#--pileup 2012_Summer_50ns_PoissonOOTPU \

