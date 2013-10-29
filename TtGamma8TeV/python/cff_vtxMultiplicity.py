
import FWCore.ParameterSet.Config as cms

# Number of Vertices
vertexHisto = cms.EDAnalyzer(
    "MyVertexCountHisto",
    src = cms.InputTag("offlinePrimaryVertices"),
)
vertexHistoGood = vertexHisto.clone(
    src = cms.InputTag("goodOfflinePrimaryVertices"),
)
vertexHistoPu = cms.EDAnalyzer(
    "MyVertexCountHisto",
    src = cms.InputTag("offlinePrimaryVertices"),
    weights = cms.untracked.InputTag("puWeight", "PUWeight")
)
vertexHistoPuTrue = vertexHistoPu.clone(
    weights = cms.untracked.InputTag("puWeight", "PUWeightTrue")
)
vertexHistoComb = vertexHistoPu.clone(
    weights = cms.untracked.InputTag("weightComb")
)
vertexHistoGoodPu  = vertexHistoPu.clone(
    src = cms.InputTag("goodOfflinePrimaryVertices"),
)
vertexHistoGoodPuTrue   = vertexHistoGoodPu.clone(
    weights = cms.untracked.InputTag("puWeight", "PUWeightTrue")
)
vertexHistoGoodComb = vertexHistoGood.clone(
    weights = cms.untracked.InputTag("weightComb")
)


from MyPackage.TtGamma8TeV.cff_preSel import preSel

vtxMultPath = cms.Path(
     preSel
    * vertexHisto
    * vertexHistoGood
    * vertexHistoPu
    * vertexHistoPuTrue
    * vertexHistoComb
    * vertexHistoGoodPu
    * vertexHistoGoodPuTrue
    * vertexHistoGoodComb
)
