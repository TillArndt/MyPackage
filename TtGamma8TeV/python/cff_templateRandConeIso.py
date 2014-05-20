import cff_photonIDCuts as pho_cuts
import cff_templateCreation as tmpl_cr

import FWCore.ParameterSet.Config as cms

def add_path(process):
    ################################################# path for Random Cone Signal template ###

    process.FiltRandCone = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut =cms.string("userFloat('randomConeIsoCharged') >= 0"),
	filter = cms.bool(False)
    )

    process.PlotRandCone = pho_cuts.make_histo_analyzer(
        "FiltRandCone",
        pho_cuts.histo_pre["randomConeIso"]
    )

    process.pathTmpltRandCone = cms.Path(
        process.preSel
        * process.FiltRandCone
        * process.PlotRandCone
    )
    return [process.pathTmpltRandCone]
