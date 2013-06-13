import sys
from FWCore.ParameterSet.VarParsing import VarParsing as VP
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import pickRelValInputFiles

def options() :
    options = VP('standard')
    options.output = "topTuple.root"
    options.maxEvents = -1
    

    options.register('procName', default = "PAT2", mytype = VP.varType.string)
    options.register('isData', default = False, mytype = VP.varType.bool)
    options.register('skim', default = True, mytype = VP.varType.bool)
    options.register('btag', default = False, mytype = VP.varType.bool)
#    options.register('outputModule', default = True, mytype = VP.varType.bool)
    options.register('quiet', default = False, mytype = VP.varType.bool)
    options.register('requireLepton', default = True, mytype = VP.varType.bool)
    options.register('globalTag', mytype = VP.varType.string )
    options.register('postfix','TR', mytype = VP.varType.string )
    options.register('btags', mytype = VP.varType.string, mult = VP.multiplicity.list )
    options.register('doElectronEA', default = True, mytype = VP.varType.bool)
    options.register('noJetSmearing', default = False, mytype = VP.varType.bool)

    try:
        for key in options._register.keys():
            setattr(options, key, cms_var.get(key, getattr(options, key)))
    except NameError:
        print "cms_var is not in __builtin__"

    print sys.argv
    if not "-create" in sys.argv:
        options.parseArguments()
    else:
        print "Found '-create' in sys.argv! Omitting options.parseArguments()"
    options._tagOrder =[]



    defaultGT = ('GR_R_53_V18' if options.isData else 'START53_V15')

    # FT_53_V21_AN4
    # START53_V23

    sync53 = 'file:/user/kuessel/files/Synchfiles/syncExercise53.root'
    diffStep1="file:/user/kuessel/CMSSW/Synch/CMSSW_5_3_8_patch3/src/pickevents.root"
    subset="file:/user/kuessel/CMSSW/Synch/CMSSW_5_3_8_patch3/src/testSkim.root"
    skim="/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_103_1_lgS.root"
    defaultFiles = [skim]
#    defaultFiles = [subset]
#    defaultFiles = [diffStep1] 
    
    options.files = defaultFiles
    if not options.globalTag : 
        options.globalTag = defaultGT

    options.btags = ['combinedSecondaryVertex','jetProbability']

    if not options.quiet : print options
    return options
