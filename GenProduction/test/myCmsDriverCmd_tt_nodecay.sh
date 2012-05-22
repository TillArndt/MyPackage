
cmsDriver.py \
MyPackage/GenProduction/python/myGenFragmentPythia8noMatch.py \
-s GEN,FASTSIM,HLT:GRun \
--conditions=FrontierConditions_GlobalTag,START44_V10::All \
--pileup=E7TeV_Fall2011_Reprocess_inTimeOnly \
--eventcontent=RECOSIM \
--filetype=LHE \
--filein=file:/net/data_cms/institut_3b/tholen/lhef/tt_nodecay/tt_nodecay_0.lhe \
--fileout=file:/net/data_cms/institut_3b/tholen/test/tt_nodecay.root \
-n 10000 \
--no_exec 

