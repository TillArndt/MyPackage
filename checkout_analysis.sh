
# commands to check out full analysis

source /afs/cern.ch/cms/cmsset_default.sh
cmsrel CMSSW_5_3_11_patch6
cd CMSSW_5_3_11_patch6/
git clone https://github.com/heinzK1X/CmsToolsAC3b.git
ln -s CmsToolsAC3b/cmstoolsac3b python/
cd src
cmsenv
git cms-addpkg PhysicsTools/PatAlgos
git cms-merge-topic -u vadler:53X-tagset133511
git cms-addpkg PhysicsTools/PatUtils
git cms-merge-topic -u vadler:53X-tagset133511-newBTagging
git cms-merge-topic -u vadler:53X-tagset133511-newEGIsolation
git cms-merge-topic -u cms-tau-pog:CMSSW_5_3_X

git remote add -f SCFootprintRemoval https://github.com/peruzzim/SCFootprintRemoval
git merge -s ours --no-commit SCFootprintRemoval/master
git read-tree --prefix=PFIsolation/SuperClusterFootprintRemoval -u SCFootprintRemoval/master
git commit -m 'Merge SCFootprintRemoval in CMSSW'
git checkout PFIsolation

git remote add -f EGamma-EGammaAnalysisTools https://github.com/ETHZ/EGamma-EGammaAnalysisTools
git merge -s ours --no-commit V00-00-21 EGamma-EGammaAnalysisTools/master
git read-tree --prefix=EGamma/EGammaAnalysisTools V00-00-21
git commit -m 'Merge EGammaAnalysisTools in CMSSW'
git checkout EGamma

git pull

