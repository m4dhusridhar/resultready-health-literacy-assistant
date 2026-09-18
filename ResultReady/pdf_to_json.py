# Purpose: Main orchestrator for converting a PDF laboratory report into structured JSON using the Hugging Face Inference API
import json
from pathlib import Path

from parser.pdf_reader import (
    extract_text_from_pdf
)

from ai.prompt_builder import (
    build_extraction_prompt
)

from ai.extractor import (
    extract_structured_report
)


def convert_pdf_to_json(
    pdf_path,
    output_path
):

    print("Reading PDF...")

    raw_text = extract_text_from_pdf(
        pdf_path
    )

    print("Building prompt...")

    prompt = build_extraction_prompt(
        raw_text
    )

    prompt_file = Path(
        "output/extraction_prompt.txt"
    )

    with open(
        prompt_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(prompt)

    print(
        "Running AI extraction..."
    )

    structured_json = (
        extract_structured_report(
            prompt
        )
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(structured_json)

    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":

    input_pdf = Path(
        "data/HealthBridge_Diagnostics_V3_1.pdf"
    )

    output_json = Path(
        "output/normalized_lab_report.json"
    )

    convert_pdf_to_json(
        input_pdf,
        output_json
    )