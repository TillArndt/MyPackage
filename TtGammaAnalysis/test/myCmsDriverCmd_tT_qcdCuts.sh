
cmsDriver.py \
MyPackage/TtGammaAnalysis/python/myGenFragment.py \
-s GEN,FASTSIM,HLT:GRun \
--conditions=FrontierConditions_GlobalTag,START42_V13::All \
--eventcontent=RECOSIM \
--filetype=LHE \
--filein=file:/home/home2/institut_3b/tholen/dev/ttgamma/forProduction20120207/tT_qcdPaperCuts.lhef \
--fileout=file:/user/tholen/eventFiles/fastSimAndReco/whizard_tT_qcdPaperCuts.root \
-n 1000000 \
--no_exec 

