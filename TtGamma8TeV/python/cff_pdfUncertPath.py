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

pdfWeightCountersPre = cms.EDProducer("PDFWeight",
    src = cms.InputTag("pdfWeightVector:cteq61"),
    weights = cms.InputTag("weightComb"),
    label = cms.string("pre"),
)

pdfWeightCountersFid = cms.EDProducer("PDFWeight",
    src = cms.InputTag("pdfWeightVector:cteq61"),
    weights = cms.InputTag("weightComb"),
    label = cms.string("fid"),
)

pdfWeightCountersPost = pdfWeightCountersPre.clone(
    label = cms.string("post"),
)

from MyPackage.TtGamma8TeV.cff_preSel import preSel

def make_pdf_uncert_path(filter_fid, filter_full):
    return cms.Path(
        preSel *
        pdfWeightVector *
        pdfWeightCountersPre *
        filter_fid *
        pdfWeightCountersFid *
        filter_full *
        pdfWeightCountersPost
    )