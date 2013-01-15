
cmsDriver.py \
MyPackage/GenProduction/python/MyHadronizer8TeV_cff.py \
-s GEN,FASTSIM,HLT:7E33v4 \
--conditions auto:startup_7E33v4 \
--pileup=2012_Summer_inTimeOnly \
--eventcontent=AODSIM \
--filetype=LHE \
--filein=file:/NON_EXISTENT \
--fileout=file:/NON_EXISTENT \
-n -1 \
--no_exec 

