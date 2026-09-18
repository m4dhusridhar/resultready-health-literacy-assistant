"""
ResultReady Prompt Definitions

This module contains all prompt engineering logic used by the
ResultReady application.

Prompt Categories
-----------------
1. Extraction Prompts
   Convert unstructured laboratory report text into structured JSON.

2. Analysis Prompts
   Generate patient-friendly educational content and appointment
   preparation guidance.

Design Principles
-----------------
- Education, not diagnosis
- Healthcare-provider-centered discussions
- Neutral, patient-friendly language
- Structured JSON output
- Responsible AI guardrails

Author
------
Madhumitha Sridhar
"""

import json

# System prompt used during structured extraction.
#
# Purpose:
# - Identify laboratory information
# - Return machine-readable JSON
# - Prevent explanations or commentary
#
# The extraction stage is intentionally lightweight.
# Clinical interpretation happens later during analysis.
EXTRACTION_SYSTEM_PROMPT = """
Extract laboratory information.

Return JSON only.

Do not explain.
Do not provide reasoning.
Do not provide markdown.
""".strip()


# System prompt used during patient education generation.
#
# This prompt intentionally prevents:
# - diagnoses
# - treatment recommendations
# - disease identification
# - clinical decision-making
#
# The goal is to improve patient understanding and
# appointment readiness rather than replace healthcare
# professionals.
#
# This is the primary Responsible AI guardrail within
# the application.
ANALYSIS_SYSTEM_PROMPT = """
You are a patient education assistant.

Your goal is to help patients understand laboratory reports and prepare for conversations with healthcare professionals.

You are NOT a diagnostic assistant.

You MUST NOT:

- diagnose conditions
- identify diseases
- infer causes
- suggest treatments
- recommend medications
- recommend supplements
- recommend procedures
- recommend additional testing
- speculate about underlying conditions

Use neutral, educational language.

Do not explain what laboratory values may indicate.

Do not discuss:

- diseases
- disorders
- deficiencies
- injuries
- inflammation
- diagnoses
- causes
- treatment options

Avoid phrases such as:

- indicates
- suggests
- may indicate
- may suggest
- consistent with
- caused by
- due to
- could represent
- likely reflects
- commonly seen in
- damage
- damaged
- deficiency
- deficient
- pathology
- complication
- risk factor for

Only explain:

1. What the test measures.
2. What is being measured or reported.
3. Why healthcare professionals commonly review it.
4. What other tests are commonly reviewed alongside it.

Questions should be general and educational.

Questions should help the patient have a productive conversation with a healthcare professional.

Questions should NOT suggest:

- additional testing
- imaging
- supplements
- medications
- procedures
- treatments

Good question examples:

- How should I understand this result in the context of my overall health?
- How does this compare with previous laboratory results?
- Are there factors that commonly influence this result?
- How is this result typically reviewed alongside other findings?

Always remind users that interpretation depends on symptoms, medical history, medications, and other clinical information.
""".strip()


def build_extraction_prompt(report_text: str) -> str:
    """
    Create the extraction prompt.

    Parameters:
    - report_text (str): The text content of the laboratory report.

    Returns:
    - str: The complete prompt for the AI model to extract structured data from the report.

    Notes:
    - Only H/L/High/Low/Abnormal values are returned.
    - Results without flags are intentionally excluded
    - No interpretation is performed during extraction
    """
    return f"""
Extract laboratory results.

IMPORTANT:

- Include ONLY results that are explicitly marked:
  H
  High
  L
  Low
  Abnormal

- Do NOT include results whose flag is blank.
- Copy values exactly as written.
- Copy units exactly as written.
- Copy flags exactly as written.
- Do not explain anything.
- Do not infer anything.
- Do not calculate anything.
- Do not add commentary.
- Return ONLY JSON.

Return exactly this format:

{{
  "laboratory_name": "",
  "patient_name": "",
  "abnormal_results": [
    {{
      "test_name": "",
      "value": "",
      "unit": "",
      "flag": ""
    }}
  ]
}}

REPORT:

{report_text}
"""


def build_analysis_prompt(report) -> str:
    """
    Create the patient education prompt.

    Parameters:
    - report (dict): The structured laboratory report data extracted from the previous step.

    Returns:
    - str: The complete prompt for the AI model to generate patient-friendly educational content and appointment

    Notes:
    This prompt is designed to:
    - improve health literacy
    - promote better healthcare conversations
    - avoid diagnostic language
    - avoid treatment recommendations
    """
    return f"""
You are creating educational content for patients.

The overall_summary field is REQUIRED.

The summary should:

1. Explain that some reported values fall outside laboratory reference ranges.
2. Explain that results outside a reference range do not automatically indicate a medical condition.
3. Explain that interpretation depends on symptoms, medical history, medications, and clinical context.
4. Explain that the purpose of this tool is to help the patient understand the report and prepare questions for a healthcare professional.

Do not use category names that imply a diagnosis.

Use category names such as:

- Iron-Related Results
- Liver-Related Tests
- Cholesterol and Triglycerides
- Glucose Results
- Vitamin D Results

Avoid category names such as:

- Anemia
- Iron Deficiency
- Prediabetes
- Liver Disease
- Hyperlipidemia
- Metabolic Syndrome

Return ONLY valid JSON.

Format:

{{
  "overall_summary": "",
  "results_to_discuss": [
    {{
      "category": "",
      "tests": [],
      "what_it_measures": "",
      "why_doctors_review_it": "",
      "questions_for_doctor": []
    }}
  ],
  "appointment_prep": []
}}

LAB DATA:

{json.dumps(report, indent=2)}
"""


def build_follow_up_prompt(
    report,
    analysis_json,
    question,
) -> str:
    """
    Create a follow-up question prompt.

    Parameters:
    - report (dict): The structured laboratory report data extracted from the previous step.
    - analysis_json (str): The JSON string containing the patient-friendly educational content generated in the previous step.
    - question (str): The specific question the patient wants to ask about their laboratory results.

    Returns:
    - str: The complete prompt for the AI model to generate a response to the patient's question

    Notes:
    Responses remain subject to the same patient education and Responsible AI restrictions as the
      primary analysis workflow.
    """
    return f"""
REPORT:

{json.dumps(report, indent=2)}

ANALYSIS:

{analysis_json}

QUESTION:

{question}
"""