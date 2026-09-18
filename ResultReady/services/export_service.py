import json

from parser.lab_schema import (
    ExtractedLabReport,
    ReportAnalysis,
)


def create_json_export(
    report: ExtractedLabReport,
    analysis: ReportAnalysis,
) -> str:
    payload = {
        "report": report.model_dump(),
        "analysis": analysis.model_dump(),
    }

    return json.dumps(
        payload,
        indent=2,
        ensure_ascii=False,
    )


def create_doctor_summary_export(
    report: ExtractedLabReport,
    analysis: ReportAnalysis,
) -> str:
    patient_name = report.patient.name or "Not provided"
    collection_date = (
        report.patient.collection_date or "Not provided"
    )

    lines = [
        "LAB REPORT EXPLAINER",
        "CLINICIAN DISCUSSION SUMMARY",
        "",
        f"Patient: {patient_name}",
        f"Collection date: {collection_date}",
        f"Laboratory: {report.laboratory_name or 'Not provided'}",
        "",
        "STRUCTURED RESULTS",
    ]

    for result in report.results:
        displayed_value = (
            str(result.value)
            if result.value is not None
            else result.value_text or "Not provided"
        )

        lines.append(
            f"- {result.test_name}: "
            f"{displayed_value} "
            f"{result.unit or ''} "
            f"[{result.reported_flag}] "
            f"Reference: "
            f"{result.reference_range or 'Not provided'}"
        )

    lines.extend(
        [
            "",
            "DOCTOR-READY SUMMARY",
            analysis.doctor_summary,
            "",
            "LIMITATIONS",
        ]
    )

    if analysis.limitations:
        for limitation in analysis.limitations:
            lines.append(f"- {limitation}")
    else:
        lines.append(
            "- Interpretation depends on the complete clinical context."
        )

    lines.extend(
        [
            "",
            "Disclaimer: This AI-generated summary is for "
            "informational and demonstration purposes only. "
            "It does not provide a diagnosis and does not replace "
            "review by a qualified healthcare professional.",
        ]
    )

    return "\n".join(lines)