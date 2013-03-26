
cmsDriver.py \
MyPackage/GenProduction/python/MyHadronizer8TeV_cff.py \
-s GEN,FASTSIM,HLT:8E33v1 \
--conditions auto:startup_8E33v1 \
--pileup=2012_Summer_inTimeOnly \
--eventcontent=AODSIM \
--filetype=LHE \
--filein=file:/NON_EXISTENT \
--fileout=file:/NON_EXISTENT \
-n -1 \
--no_exec 

