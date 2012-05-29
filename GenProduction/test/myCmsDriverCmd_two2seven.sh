
cmsDriver.py \
MyPackage/GenProduction/python/Hadronizer_MgmMatchTune4C_7TeV_madgraph_pythia8_cff.py \
-s GEN,FASTSIM,HLT:GRun \
--conditions=FrontierConditions_GlobalTag,START42_V13::All \
--pileup=E7TeV_Fall2011_Reprocess_inTimeOnly \
--eventcontent=AODSIM \
--filetype=LHE \
--filein=file:/user/tholen/lhef/two2seven/two2seven_0.lhe \
--fileout=file:/user/tholen/aodsim/two2seven/two2seven_0.root \
-n -1 \
--no_exec 

