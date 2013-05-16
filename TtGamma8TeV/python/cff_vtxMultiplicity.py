
import FWCore.ParameterSet.Config as cms

# Number of Vertices
vertexHisto = cms.EDAnalyzer(
    "MyVertexCountHisto",
    src = cms.InputTag("offlinePrimaryVertices"),
)
vertexHistoGood = vertexHisto.clone(
    src = cms.InputTag("goodOfflinePrimaryVertices"),
)
vertexHisto1BX = cms.EDAnalyzer(
    "MyVertexCountHisto",
    src = cms.InputTag("offlinePrimaryVertices"),
    weights = cms.untracked.InputTag("puWeight", "Reweight1BX")
)
vertexHisto3D = vertexHisto1BX.clone(
    weights = cms.untracked.InputTag("puWeight", "Reweight3D")
)
vertexHistoGood1BX  = vertexHisto1BX.clone(
    src = cms.InputTag("goodOfflinePrimaryVertices"),
)
vertexHistoGood3D   = vertexHistoGood1BX.clone(
    weights = cms.untracked.InputTag("puWeight", "Reweight3D")
)

from MyPackage.TtGamma8TeV.cff_preSel import preSel

vtxMultPath = cms.Path(
    * preSel
    * vertexHisto
    * vertexHistoGood
    * vertexHisto1BX
    * vertexHisto3D
    * vertexHistoGood1BX
    * vertexHistoGood3D
)