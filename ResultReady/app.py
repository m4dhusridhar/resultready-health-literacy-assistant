"""
ResultReady

AI-powered patient education assistant for laboratory reports.

Purpose
-------
Help patients:
1. Understand reported laboratory results.
2. Learn what commonly reported tests measure.
3. Identify reults outside laboratory reference ranges.
4. Prepare meaningful questions for conversations with healthcare providers.

This application is intended for educational purposes only and 
does not provide diagnoses, treatment recommendations, or
professional medical advice. 

Author
------
Madhumitha Sridhar
"""

import streamlit as st

from services.report_service import ReportService

st.set_page_config(
    page_title="ResultReady",
    page_icon="🧪",
    layout="wide",
)


@st.cache_resource
# Create and cache the report processing service so it
# persists across Streamlit reruns and avoids repeated
# initialization of AI-related components.
def get_report_service():
    return ReportService()


st.title("🩺 ResultReady")

st.markdown(
    """
    ### Understanding Results. Empowering Conversations.

    Transform complex laboratory reports into clear, patient-friendly explanations.
    Understand reported results, learn what key tests measure, and prepare meaningful
    questions for conversations with your healthcare provider.
    """
)

st.warning(
    "Educational Use Only: ResultReady is designed to help patients better understand "
    "laboratory reports and prepare questions for conversations with healthcare professionals. "
    "It does not diagnose medical conditions, provide medical advice, recommend treatments, "
    "or replace professional medical judgment. Results outside laboratory reference ranges "
    "do not automatically indicate a medical condition, and interpretation depends on "
    "symptoms, medical history, medications, and other clinical information. "
    "Please upload only synthetic, de-identified, or appropriately authorized reports."
)

# Create and cache the report processing service so it
# persists across Streamlit reruns and avoids repeated
# initialization of AI-related components.
uploaded_file = st.file_uploader(
    "Upload a laboratory report PDF",
    type=["pdf"],
)


if "report_text" not in st.session_state:
    st.session_state.report_text = None

if "report" not in st.session_state:
    st.session_state.report = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

# Execute the complete processing pipeline:
#
# PDF Upload
# -> Text Extraction
# -> Laboratory Result Extraction
# -> Patient Education Generation
# -> Appointment Preparation Questions
if uploaded_file is not None:

    if st.button(
        "Analyze Report",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Extracting and analyzing the report..."
            ):

                service = get_report_service()

                report_text, report, analysis = (
                    service.process_pdf(
                        uploaded_file
                    )
                )

                st.session_state.report_text = report_text
                st.session_state.report = report
                st.session_state.analysis = analysis

            st.success(
                "Report analysis completed."
            )

        except Exception as exc:

            st.error(
                f"Analysis failed: {exc}"
            )


report = st.session_state.report
analysis = st.session_state.analysis

# Execute the complete processing pipeline:
#
# PDF Upload
# -> Text Extraction
# -> Laboratory Result Extraction
# -> Patient Education Generation
# -> Appointment Preparation Questions
if report and analysis:

    overview_tab, prep_tab, results_tab, raw_tab = st.tabs(
        [
            "Understanding Your Results",
            "Questions To Discuss With Your Healthcare Provider",
            "Results Outside Reference Range",
            "Technical View",
        ]
    )

    # --------------------------------------------------
    # Understanding Your Results
    # --------------------------------------------------

    with overview_tab:

        st.info(
            analysis.get(
                "overall_summary",
                "No summary available."
            )
        )

        sections = analysis.get(
            "results_to_discuss",
            []
        )

        for section in sections:

            st.markdown("---")

            st.subheader(
                section.get(
                    "category",
                    "Result Group"
                )
            )

            tests = section.get(
                "tests",
                []
            )

            if tests:

                st.write(
                    "**Tests outside the laboratory reference range:**"
                )

                for test in tests:
                    st.write(
                        f"• {test}"
                    )

            what_it_measures = section.get(
                "what_it_measures",
                ""
            )

            if what_it_measures:

                st.write(
                    "**What this measures:**"
                )

                st.write(
                    what_it_measures
                )

            why_reviewed = section.get(
                "why_doctors_review_it",
                ""
            )

            if why_reviewed:

                st.write(
                    "**Why healthcare professionals commonly review these together:**"
                )

                st.write(
                    why_reviewed
                )

    # --------------------------------------------------
    # Appointment Prep
    # --------------------------------------------------

    with prep_tab:

        st.subheader(
            "Preparing For Your Appointment"
        )

        st.write(
            "Consider discussing the following topics with your healthcare provider."
        )

        general_questions = analysis.get(
            "appointment_prep",
            []
        )

        if general_questions:

            st.subheader(
                "General Questions"
            )

            for question in general_questions:

                st.write(
                    f"✅ {question}"
                )

        sections = analysis.get(
            "results_to_discuss",
            []
        )

        for section in sections:

            questions = section.get(
                "questions_for_doctor",
                []
            )

            if questions:

                st.markdown("---")

                st.subheader(
                    section.get(
                        "category",
                        "Questions"
                    )
                )

                for question in questions:

                    st.write(
                        f"• {question}"
                    )

    # --------------------------------------------------
    # Structured Results
    # --------------------------------------------------

    with results_tab:

        st.subheader(
            "Extracted Lab Results"
        )

        rows = []

        for result in report.get(
            "abnormal_results",
            []
        ):

            rows.append(
                {
                    "Test":
                        result.get(
                            "test_name",
                            ""
                        ),

                    "Value":
                        result.get(
                            "value",
                            ""
                        ),

                    "Unit":
                        result.get(
                            "unit",
                            ""
                        ),

                    "Flag":
                        result.get(
                            "flag",
                            ""
                        ),
                }
            )

        st.dataframe(
            rows,
            hide_index=True,
            use_container_width=True,
        )

    # --------------------------------------------------
    # Technical View
    # --------------------------------------------------

    with raw_tab:
        show_debug = st.checkbox(
    "Show Technical Details"
        )

        if show_debug:
            st.subheader(
                "Extracted Report"
            )

            st.json(
                report
            )

            st.subheader(
                "Generated Analysis"
            )

            st.json(
                analysis
            )
st.divider()

st.caption(
    "ResultReady is an educational tool designed to improve health literacy "
    "and support conversations between patients and healthcare professionals."
)