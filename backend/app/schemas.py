from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StudentAnalysisRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    phone: str | None = None
    state: str | None = None
    education_level: str = Field(min_length=2, max_length=80)
    stream: str | None = None
    interests: str = Field(max_length=400, default="")
    skills: str = Field(max_length=400, default="")
    dream: str = Field(max_length=400, default="")
    maths: int = Field(ge=0, le=100)
    physics: int = Field(ge=0, le=100)
    chemistry: int = Field(ge=0, le=100)
    biology: int = Field(ge=0, le=100)


class SubjectScoreResponse(BaseModel):
    subject: str
    marks: int
    band: str


class CareerMatchResponse(BaseModel):
    career_slug: str
    title: str
    score: float
    rationale: str


class InsightResponse(BaseModel):
    quote: str
    author: str
    source: str
    context: str


class RoadmapStepResponse(BaseModel):
    id: int
    phase: str
    step_order: int
    title: str
    description: str
    skill: str
    resource: str
    duration: str
    outcome: str
    completed: bool = False


class RoadmapPhaseResponse(BaseModel):
    phase: str
    steps: list[RoadmapStepResponse]


class CareerRecommendationResponse(BaseModel):
    slug: str
    title: str
    summary: str
    difficulty_level: str
    time_required: str
    outlook: str
    fit_reason: str
    required_subjects: list[str]
    estimated_salary: str


class GovtJobResponse(BaseModel):
    id: str
    title: str
    qualification: str
    exam_body: str
    age_criteria: str
    selection_process: list[str]
    syllabus_summary: str
    estimated_salary: str


class StudyPlanEntryResponse(BaseModel):
    day_name: str
    day_order: int
    session_type: str
    subject_name: str
    duration_hours: float
    objective: str
    is_break: bool


class StudyPlanResponse(BaseModel):
    id: int
    title: str
    status: str
    adaptive_summary: str
    weekly_hours: float
    entries: list[StudyPlanEntryResponse]


class DashboardResponse(BaseModel):
    user_id: int
    student_name: str
    created_at: datetime
    confidence_score: float
    strong_subjects: list[str]
    weak_subjects: list[str]
    message: str
    marks_breakdown: list[SubjectScoreResponse]
    recommended_career: CareerRecommendationResponse
    career_matches: list[CareerMatchResponse]
    roadmap: list[RoadmapPhaseResponse]
    study_plan: StudyPlanResponse
    insights: list[InsightResponse]
    subject_progress: dict[str, int]
    completion_summary: dict[str, int]
    success_probability: float
    future_ready_features: list[str]


class ProgressUpdateRequest(BaseModel):
    user_id: int


class SubjectProgressUpdateRequest(BaseModel):
    user_id: int
    subject_name: str
    completion_percentage: int = Field(ge=0, le=100)


class StudyPlanRefreshRequest(BaseModel):
    user_id: int


class BootstrapResponse(BaseModel):
    education_levels: list[str]
    supported_subjects: list[str]
    career_paths: list[str]
    future_ready_features: list[str]


class StatusResponse(BaseModel):
    status: Literal["ok"]
    service: str


class ActionResponse(BaseModel):
    message: str
    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    user_id: int
    message: str


class ChatResponse(BaseModel):
    response: str


class AdminLoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class AdminDashboardUserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None = None
    state: str | None = None
    interests: str = ""
    education_level: str
    recommended_path: str | None = None
    success_probability: float | None = None
    completed_steps: int = 0
    total_steps: int = 0


class RoadmapStepUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    skill: str | None = None
    resource: str | None = None
    duration: str | None = None
    outcome: str | None = None
