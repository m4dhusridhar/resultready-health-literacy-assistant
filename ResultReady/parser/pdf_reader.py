"""
PDF Text Extraction Utilities

This module is responsible for extracting machine-readable text
from laboratory report PDFs.

Responsibilities
----------------
1. Read PDF documents.
2. Extract text from each page.
3. Normalize and clean extracted content.
4. Return text suitable for downstream AI processing.

Current Limitations
-------------------
- Supports text-based PDFs only.
- Does not perform OCR.
- Scanned/image-only PDFs must be processed through an OCR
  service before extraction.

Author
------
Madhumitha Sridhar
"""

from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader


def _clean_text(text: str) -> str:
    """
    Normalize extracted PDF text.

    Parameters:
    - text (str): Raw text extracted from the PDF.

    Returns:
    - str: Cleaned and normalized text, with extraneous whitespace removed.
    """
    lines = []

    # Process text line-by-line and normalize spacing.
    for line in text.splitlines():
        # Collapse repeated spaces and tabs into a single space.
        cleaned_line = " ".join(line.split())

        # Exclude empty lines.
        if cleaned_line:
            lines.append(cleaned_line)

    return "\n".join(lines)


def extract_text_from_pdf(pdf_source: str | Path | BinaryIO) -> str:
    """
    Extract text from a text-based PDF.

    Parameters:
    - pdf_source (str | Path | BinaryIO): The path to the PDF file or a file-like object.

    Returns:
    - str: The extracted and cleaned text from the PDF.
    """
    reader = PdfReader(pdf_source)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        if page_text.strip():
            pages.append(
                f"--- PAGE {page_number} ---\n{page_text}"
            )

    combined_text = "\n\n".join(pages)
    cleaned_text = _clean_text(combined_text)

    if not cleaned_text:
        raise ValueError(
            "No readable text was found in this PDF. "
            "The file may be scanned and may require OCR."
        )

    return cleaned_text