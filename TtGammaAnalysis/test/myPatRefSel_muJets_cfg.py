
# myPatrefsel_mujets_cfg.py

from UserCode.HTholen.patRefSel_muJets_cfg import *

process.maxEvents.input = 10000

process.pfNoTauPF.enable = False

process.pfSelectedElectronsPF.cut=cms.string('')

process.step0a = triggerResults.clone(
  triggerConditions = [ 'HLT_IsoMu17_v*' ]
)

process.isoValElectronWithNeutralPF.deposits  = cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepElectronWithNeutralPF"),
        deltaR = cms.double(0.4),##default 0.3
        weight = cms.string('1'),
        vetos = cms.vstring('Threshold(0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))

process.isoValElectronWithChargedPF.deposits= cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepElectronWithChargedPF"),
        deltaR = cms.double(0.4),##default 0.3
        weight = cms.string('1'),
        vetos = cms.vstring(),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))

process.isoValElectronWithPhotonsPF.deposits=cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepElectronWithPhotonsPF"),
        deltaR = cms.double(0.4),##default 0.3
        weight = cms.string('1'),
        vetos = cms.vstring('Threshold(0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))


