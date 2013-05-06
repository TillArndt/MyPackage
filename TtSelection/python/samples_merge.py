
import os
import cmstoolsac3b.sample as smp

def generate_das_samples():

    # find edm source files
    das_files = None
    for cwd, ds, fs in os.walk(os.path.dirname(__file__)):
        das_files = list(f for f in fs if (f[:4]=="das_" and f[-3:]==".py"))
        break
    print "INFO: generating samples from das files: " + str(das_files)

    # generate samples from source files
    smpls = {}
    for f in das_files:
        samplename = f[4:-3]
        is_data_sample = "Run" in samplename
        class sample_subclass(smp.Sample):
            name = samplename
            is_data = is_data_sample
            lumi = 1000.
            input_files = "dummy"
            output_file = "/disk1/tholen/eventFiles/fromGrid20130502/"
            cfg_add_lines = [
                'process.load("MyPackage.TtSelection.'
                + f[:-3]
                + '")'
            ]
        smpls[samplename] = sample_subclass()

    # add single top sample that has no das entry
    smpls.update(smp._check_n_load(Tbar_tW))   

    # set Single Top legend
    for l in ("T_t", "Tbar_t","T_tW", "Tbar_tW"):
        smpls[l].legend = "Single Top"

    return smpls
        

class Tbar_tW(smp.Sample):
    lumi=1000.
    output_file = "/disk1/tholen/eventFiles/fromGrid20130502/"
    input_files = ['/store/user/kuessel/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_1_1_Vyz.root','/store/user/kuessel/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_7_1_Kfw.root']

