from parser.ai_extractor import LabReportAI
from parser.pdf_reader import extract_text_from_pdf

text = extract_text_from_pdf(
    "data/healthbridge_diagnostics_v3_1.pdf"
)

ai = LabReportAI()

report = ai.extract_report(text)

print(report.model_dump_json(indent=2))