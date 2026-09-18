"""
ResultReady AI Extraction and Analysis Engine

This module coordinates all AI-powered functionality for the
ResultReady application.

Responsibilities
----------------
1. Extract structured laboratory data from report text.
2. Generate patient-friendly educational explanations.
3. Generate appointment preparation guidance.

Design Principles
-----------------
- Education, not diagnosis
- Structured JSON outputs
- Responsible AI guardrails
- Healthcare-provider-centered conversations

The AI components are intentionally restricted from:
- Diagnosing medical conditions
- Recommending treatments
- Prescribing medications
- Providing professional medical advice

Author
------
Madhumitha Sridhar
"""

import json
import json

from parser.prompt_builder import (
    ANALYSIS_SYSTEM_PROMPT,
    EXTRACTION_SYSTEM_PROMPT,
    build_analysis_prompt,
    build_extraction_prompt,
)
from services.nvidia_client import NvidiaClient


class LabReportAI:
    """
    Orchestrates AI-powered extraction and educational analysis

    This class serves as the primary interface between the
    application and the NVIDIA-hosted language model.

    Workflow:
    1. Extract structured laboratory information
    2. Generate patient-friendly educational content
    3. Generate appointment preparation guidance

    This component does not provide diagnoses, treatment recommendations, or professional medical advice.
    """
    def __init__(self) -> None:
        # Initialize the AI extraction service and NVIDIA client.
        self.client = NvidiaClient()

    def extract_report(
        self,
        report_text: str,
    ) -> dict:

        """
        Extracts flagged laboratory results and other relevant information from the report text.
        Parameters:
        - report_text (str): The text content of the laboratory report.

        Returns:
        - dict: A dictionary containing the extracted information, including flagged results and other relevant data.
        """

        print("\n========== EXTRACTION START ==========")

        # Build a structured extraction prompt that requests
        # only laboratory results explicitly flagged within
        # the report.
        prompt = build_extraction_prompt(
            report_text=report_text,
        )

        print("PROMPT LENGTH:", len(prompt))

        # Request structured JSON extraction from the model.
        raw_response = self.client.complete(
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=2000,
            temperature=0.0,
        )

        # Debug logging can be enabled during development.
        print("\n===== RAW RESPONSE =====")
        print(raw_response)
        print("========================")

        try:
            # Validate that the model returned valid JSON before
            # continuing to downstream processing.
            data = json.loads(raw_response)
        except Exception as e:
            print("JSON PARSE ERROR:")
            print(e)

            raise ValueError(
                "Model returned invalid JSON."
            )

        print("========== EXTRACTION END ==========\n")

        return data

    def analyze_report(
        self,
        report: dict,
    ) -> dict:
        """
        Generate patient-friendly educational content.

        Parameters:
        - report (dict): The structured laboratory report data extracted from the previous step.

        Returns:
        - dict: A dictionary containing patient-friendly educational content, including an overall summary, results to discuss, and appointment preparation guidance.

        Notes:
        This workflow intentionally avoids providing diagnoses, treatment recommendations, or professional medical advice. The generated content is for educational purposes only.
        """

        print("\n========== ANALYSIS START ==========")

        # Generate a patient-education prompt that transforms
        # structured laboratory results into understandable
        # explanations and discussion topics.
        prompt = build_analysis_prompt(
            report=report,
        )

        raw_response = self.client.complete(
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=2500,
            temperature=0.0,
        )

        print("\n===== ANALYSIS RESPONSE =====")
        print("RAW RESPONSE LENGTH:")
        print(len(raw_response))

        print("\nLAST 200 CHARACTERS:")
        print(raw_response[-200:])
        print("=============================")

        try:
            data = json.loads(raw_response)
        except Exception as e:
            print("ANALYSIS JSON ERROR:")
            print(e)

            raise ValueError(
                "Model returned invalid analysis JSON."
            )

        print("========== ANALYSIS END ==========\n")

        return data