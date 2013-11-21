sample = "NOSAMPLE"
try:
    sample = cms_var.get("sample", sample)
except NameError:
    pass

import FWCore.ParameterSet.Config as cms

pdf_set_name = "cteq61.LHgrid"

pdfWeightVector = cms.EDProducer("PdfWeightProducer",
    GenTag = cms.untracked.InputTag("genParticles"),
    PdfInfoTag = cms.untracked.InputTag("generator"),
    PdfSetNames = cms.untracked.vstring(pdf_set_name)
)

# Fix POWHEG if buggy (this PDF set will also appear on output,
# so only two more PDF sets can be added in PdfSetNames if not "")
if sample[:4] == "TTPo":
    pdfWeightVector.FixPOWHEG = cms.untracked.string(pdf_set_name)

pdfWeight = cms.EDProducer("PDFWeight",
    src = cms.InputTag("pdfWeightVector:cteq61"),
    uncertMode = cms.int32(0),
)

pdfWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src = cms.InputTag("pdfWeight"),
    name = cms.untracked.string("histo"),
    title = cms.untracked.string(";pdf weight;events"),
    nbins = cms.untracked.int32(100),
    min = cms.untracked.double(0.),
    max = cms.untracked.double(2.),
)

pdfCentralWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src = cms.InputTag("pdfWeight", "central"),
    name = cms.untracked.string("histo"),
    title = cms.untracked.string(";pdf weight;events"),
    nbins = cms.untracked.int32(100),
    min = cms.untracked.double(0.),
    max = cms.untracked.double(2.),
)

trigWeightSequence = cms.Sequence(
    pdfWeightVector *
    pdfWeight *
    pdfWeightHisto *
    pdfCentralWeightHisto
)