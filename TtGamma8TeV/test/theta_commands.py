import os
import theta_auto
theta_auto.config.workdir = os.getcwd()
theta_auto.config.report = theta_auto.html_report(os.path.join(theta_auto.config.workdir, 'index.html'))
theta_auto.config.theta_dir = "/afs/cern.ch/work/h/htholen/private/cmsWorkingDir/CMSSW_5_3_11_patch6/theta"
model = theta_auto.build_model_from_rootfile("ThetaHistos.root", include_mc_uncertainties=True)
model.set_signal_processes(["real"])
model.add_lognormal_uncertainty("fake_rate", 1., "fake")
res = theta_auto.mle(model, "data", 1, chi2=True)
print res
par_values = {"beta_signal":res["real"]["beta_signal"][0][0], "fake_rate":res["real"]["fake_rate"][0][0]}
bkg_val = model.get_coeff("chhadiso", "fake").get_value(par_values)
bkg_err = bkg_val * res["real"]["fake_rate"][0][1] / res["real"]["fake_rate"][0][0]
sig_val = res["real"]["beta_signal"][0][0]
sig_err = res["real"]["beta_signal"][0][1]

