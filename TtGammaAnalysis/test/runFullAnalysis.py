#!/net/software_cms/slc5_amd64_gcc434/cms/cmssw/CMSSW_4_2_8/external/slc5_amd64_gcc434/bin/python

import os
from YKuessel.TopCharge.sourceFiles_cfi import *

input = "/user/tholen/eventFiles/Samplelist_Backgrounds.txt"
dictOfLists = ReadProdDetails(input)

for i, sample in enumerate(dictOfLists["abbreviation"]):
    cmsRun='cmsRun test/runAnalysisOnSample_cfg.py ' + str(sample) + ' &> output/runFullAnalysis_' + str(sample) + '.log'
    if (i % 4 != 3):
        cmsRun = cmsRun + " &"
    print cmsRun
    os.system(cmsRun)

        
