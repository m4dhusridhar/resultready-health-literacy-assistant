from typing import Literal, Optional

from pydantic import BaseModel, Field


FlagType = Literal["high", "low", "normal", "abnormal", "unknown"]


class PatientInformation(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    patient_id: Optional[str] = None
    collection_date: Optional[str] = None
    report_date: Optional[str] = None


class LabResult(BaseModel):
    test_name: str
    value: Optional[float] = None
    value_text: Optional[str] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    reported_flag: FlagType = "unknown"
    section: Optional[str] = None
    source_text: Optional[str] = None


class ExtractedLabReport(BaseModel):
    laboratory_name: Optional[str] = None
    report_title: Optional[str] = None
    patient: PatientInformation = Field(
        default_factory=PatientInformation
    )
    results: list[LabResult] = Field(default_factory=list)
    extraction_warnings: list[str] = Field(default_factory=list)


class PatientExplanation(BaseModel):
    test_name: str
    reported_flag: FlagType
    explanation: str
    questions_for_clinician: list[str] = Field(default_factory=list)


class ReportAnalysis(BaseModel):
    overall_summary: str
    explanations: list[PatientExplanation] = Field(default_factory=list)
    doctor_summary: str
    limitations: list[str] = Field(default_factory=list)
