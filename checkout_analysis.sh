# commands  check out full analysis
# Heiners Checkout, change for my Version not done
source /afs/cern.ch/cms/cmsset_default.sh
cmsrel CMSSW_5_3_11_patch6
cd CMSSW_5_3_11_patch6/
git clone https://github.com/heinzK1X/CmsToolsAC3b.git
cd python
ln -s ../CmsToolsAC3b/cmstoolsac3b
cd ../src
cmsenv
git cms-addpkg PhysicsTools/PatAlgos
git cms-merge-topic -u vadler:53X-tagset133511
git cms-addpkg PhysicsTools/PatUtils
git cms-merge-topic -u vadler:53X-tagset133511-newBTagging
git cms-merge-topic -u vadler:53X-tagset133511-newEGIsolation
git cms-merge-topic -u cms-tau-pog:CMSSW_5_3_X
scram b -j 9

git remote add -f EGamma-EGammaAnalysisTools https://github.com/ETHZ/EGamma-EGammaAnalysisTools
git merge -s ours --no-commit EGamma-EGammaAnalysisTools/V00-00-30
git read-tree --prefix=EGamma/EGammaAnalysisTools -u EGamma-EGammaAnalysisTools/V00-00-30
git commit -m 'Merge EGammaAnalysisTools in CMSSW'
git checkout EGamma

git clone https://github.com/peruzzim/SCFootprintRemoval.git
cd SCFootprintRemoval/
git checkout V01-01
cd ../
mkdir PFIsolation
mv SCFootprintRemoval PFIsolation/SuperClusterFootprintRemoval
scram b -j 9

git clone https://github.com/HeinAtCERN/TTGammaModules.git
git clone https://github.com/HeinAtCERN/MyProducts.git
git clone https://github.com/HeinAtCERN/MyPackage.git
scram b -j 9

cd ..
svn co https://ekptrac.physik.uni-karlsruhe.de/public/theta/tags/testing theta
cd theta
make
cd ../python
ln -s ../theta/utils2/theta_auto/
cd ../src

