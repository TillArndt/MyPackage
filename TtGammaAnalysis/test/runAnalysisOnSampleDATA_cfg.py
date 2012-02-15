
from MyPackage.TtGammaAnalysis.myttbarPatTupleDATA_cfg import *
import sys

input = "/user/tholen/eventFiles/Samplelist_Data.txt"
if len(sys.argv) > 3:
    input= sys.argv[3]
    print "input proddetails set to "+input
else:
    print "default proddetails are used: "+input
    
from YKuessel.TopCharge.sourceFiles_cfi import *
dictOfLists = ReadProdDetails(input)
sourceType = (dictOfLists["abbreviation"])[0]
itsdata = False
knownsample=False
if len(sys.argv) < 3:    
    print " \n \n Please add one argument from list:"
    for sample in dictOfLists["abbreviation"]:
      print sample
else:
    sourceType = sys.argv[2]
    for line, sample in enumerate(dictOfLists["abbreviation"]):
      if sourceType == sample:
          print "\n \n sample is in list of known samples..."
          print "lumi: " +  (dictOfLists["lumi"])[line]
          if (dictOfLists["lumi"])[line] != "-1":
              itsdata=True
          print "maxEvents: " + (dictOfLists["subset"])[line]
          process.maxEvents.input  = int((dictOfLists["subset"])[line])          
          process.source.fileNames = GetFileNames(sourceType, input, "merged")
          process.out.fileName = "file:/user/tholen/eventFiles/subsamples_Data/"+sourceType+".root"
          process.TFileService.fileName = "output/runFullAnalysis_"+sourceType+".root"
          knownsample=True
if not knownsample:
    print " \n \n sample not known. please add one from list."
    for sample in dictOfLists["abbreviation"]:
        print sample
