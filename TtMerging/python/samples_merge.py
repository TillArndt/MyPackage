
import os
import cmstoolsac3b.sample as smp
import cmstoolsac3b.settings as settings

output_path = "/user/tholen/link_pcac3b04/eventFiles/fromGrid20130618/"

def _make_sample_inst(samplename, is_data_sample, input_files_list):
    class sample_subclass(smp.Sample):
        name = samplename
        is_data = is_data_sample
        lumi = 1000.
        input_files = input_files_list
        output_file = output_path
    return sample_subclass() # instance

def generate_das_samples():
    # find edm source files
    das_files = None
    das_file_folder = os.path.dirname(__file__)
    for cwd, ds, fs in os.walk(das_file_folder):
        das_files = list(f for f in fs if (f[:4]=="das_" and f[-4:]==".txt"))
        break
    print "INFO: generating samples from das files: " + str(das_files)

    # generate samples from source files
    smpls = {}
    for f in das_files:
        samplename = f[4:-4]
        is_data = "Run" in samplename
        with open(os.path.join(das_file_folder, f)) as f_handle:
            lines = []
            sample_count = 0
            for line in f_handle:
                lines.append(line.strip())
                if len(lines) == 50:
                    name = samplename + "_%03d" % sample_count
                    smpls[name] = _make_sample_inst(name, is_data, lines)
                    sample_count += 1
                    lines = []
            # remaining lines...
            if lines:
                name = samplename + "_%03d" % sample_count
                smpls[name] = _make_sample_inst(name, is_data, lines)

    return smpls
        

