from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Admin(TimestampMixin, Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    education_level: Mapped[str] = mapped_column(String(80), nullable=False)
    interests: Mapped[str] = mapped_column(Text, default="", nullable=False)
    skills: Mapped[str] = mapped_column(Text, default="", nullable=False)

    analyses: Mapped[list["Analysis"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    study_plans: Mapped[list["StudyPlan"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    roadmap_progress: Mapped[list["RoadmapProgress"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    subject_progress: Mapped[list["SubjectProgress"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class CareerPath(TimestampMixin, Base):
    __tablename__ = "career_paths"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty_level: Mapped[str] = mapped_column(String(40), nullable=False)
    time_required: Mapped[str] = mapped_column(String(80), nullable=False)
    outlook: Mapped[str] = mapped_column(Text, nullable=False)
    fit_reason: Mapped[str] = mapped_column(Text, nullable=False)
    required_subjects: Mapped[str] = mapped_column(Text, nullable=False)
    keyword_profile: Mapped[str] = mapped_column(Text, nullable=False)

    roadmap_steps: Mapped[list["RoadmapStep"]] = relationship(
        back_populates="career_path",
        cascade="all, delete-orphan",
        order_by="RoadmapStep.step_order",
    )
    insights: Mapped[list["CareerInsight"]] = relationship(
        back_populates="career_path",
        cascade="all, delete-orphan",
    )
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="recommended_career")


class RoadmapStep(TimestampMixin, Base):
    __tablename__ = "roadmap_steps"
    __table_args__ = (UniqueConstraint("career_path_id", "step_order", name="uq_career_step_order"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    career_path_id: Mapped[int] = mapped_column(ForeignKey("career_paths.id"), nullable=False)
    phase: Mapped[str] = mapped_column(String(40), nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    skill: Mapped[str] = mapped_column(String(120), nullable=False)
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[str] = mapped_column(String(60), nullable=False)
    outcome: Mapped[str] = mapped_column(Text, nullable=False)

    career_path: Mapped["CareerPath"] = relationship(back_populates="roadmap_steps")
    progress_entries: Mapped[list["RoadmapProgress"]] = relationship(
        back_populates="roadmap_step",
        cascade="all, delete-orphan",
    )


class CareerInsight(TimestampMixin, Base):
    __tablename__ = "career_insights"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_path_id: Mapped[int] = mapped_column(ForeignKey("career_paths.id"), nullable=False)
    quote: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(120), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=False)

    career_path: Mapped["CareerPath"] = relationship(back_populates="insights")


class Analysis(TimestampMixin, Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    recommended_career_id: Mapped[int] = mapped_column(ForeignKey("career_paths.id"), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    strong_subjects: Mapped[str] = mapped_column(Text, nullable=False)
    weak_subjects: Mapped[str] = mapped_column(Text, nullable=False)
    analysis_notes: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(back_populates="analyses")
    recommended_career: Mapped["CareerPath"] = relationship(back_populates="analyses")
    subject_scores: Mapped[list["SubjectScore"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan",
    )
    career_matches: Mapped[list["CareerMatch"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan",
    )


class SubjectScore(TimestampMixin, Base):
    __tablename__ = "subject_scores"
    __table_args__ = (UniqueConstraint("analysis_id", "subject_name", name="uq_analysis_subject"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"), nullable=False, index=True)
    subject_name: Mapped[str] = mapped_column(String(60), nullable=False)
    marks: Mapped[int] = mapped_column(Integer, nullable=False)
    performance_band: Mapped[str] = mapped_column(String(30), nullable=False)

    analysis: Mapped["Analysis"] = relationship(back_populates="subject_scores")


class CareerMatch(TimestampMixin, Base):
    __tablename__ = "career_matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"), nullable=False, index=True)
    career_path_id: Mapped[int] = mapped_column(ForeignKey("career_paths.id"), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)

    analysis: Mapped["Analysis"] = relationship(back_populates="career_matches")


class StudyPlan(TimestampMixin, Base):
    __tablename__ = "study_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    focus_career_id: Mapped[int] = mapped_column(ForeignKey("career_paths.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)
    adaptive_summary: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(back_populates="study_plans")
    entries: Mapped[list["StudyPlanEntry"]] = relationship(
        back_populates="study_plan",
        cascade="all, delete-orphan",
        order_by="StudyPlanEntry.day_order",
    )


class StudyPlanEntry(TimestampMixin, Base):
    __tablename__ = "study_plan_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    study_plan_id: Mapped[int] = mapped_column(ForeignKey("study_plans.id"), nullable=False, index=True)
    day_name: Mapped[str] = mapped_column(String(20), nullable=False)
    day_order: Mapped[int] = mapped_column(Integer, nullable=False)
    session_type: Mapped[str] = mapped_column(String(40), nullable=False)
    subject_name: Mapped[str] = mapped_column(String(80), nullable=False)
    duration_hours: Mapped[float] = mapped_column(Float, nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    is_break: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    study_plan: Mapped["StudyPlan"] = relationship(back_populates="entries")


class RoadmapProgress(TimestampMixin, Base):
    __tablename__ = "roadmap_progress"
    __table_args__ = (UniqueConstraint("user_id", "roadmap_step_id", name="uq_user_roadmap_step"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    roadmap_step_id: Mapped[int] = mapped_column(ForeignKey("roadmap_steps.id"), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship(back_populates="roadmap_progress")
    roadmap_step: Mapped["RoadmapStep"] = relationship(back_populates="progress_entries")


class SubjectProgress(TimestampMixin, Base):
    __tablename__ = "subject_progress"
    __table_args__ = (UniqueConstraint("user_id", "subject_name", name="uq_user_subject"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    subject_name: Mapped[str] = mapped_column(String(60), nullable=False)
    completion_percentage: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user: Mapped["User"] = relationship(back_populates="subject_progress")
