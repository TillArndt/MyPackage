
cmsDriver.py STEP2 \
--step RAW2DIGI,L1Reco,RECO \
--conditions START53_V7N::All \
--pileup 2012_Summer_50ns_PoissonOOTPU \
--datamix NODATAMIXER \
--eventcontent AODSIM \
--datatier AODSIM \
--no_exec \
-n -1 \
--filein file:out_STEP1.root \
--fileout out_STEP2.root \


