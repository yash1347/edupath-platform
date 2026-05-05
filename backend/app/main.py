from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from jose import JWTError, jwt
from passlib.context import CryptContext
import openai

from app.core.config import get_settings
from app.database import Base, SessionLocal, engine, get_db
from app.models import (
    Admin,
    Analysis,
    CareerMatch,
    CareerPath,
    RoadmapProgress,
    RoadmapStep,
    StudyPlan,
    SubjectProgress,
    SubjectScore,
    User,
)
from app.schemas import (
    ActionResponse,
    BootstrapResponse,
    DashboardResponse,
    GovtJobResponse,
    ProgressUpdateRequest,
    StatusResponse,
    StudentAnalysisRequest,
    StudyPlanRefreshRequest,
    SubjectProgressUpdateRequest,
    ChatRequest,
    ChatResponse,
    AdminLoginRequest,
    TokenResponse,
    AdminDashboardUserResponse,
    CareerRecommendationResponse,
    RoadmapPhaseResponse,
    RoadmapStepResponse,
    RoadmapStepUpdateRequest,
)
from app.seed import seed_database
from app.data.govt_jobs import GOVT_JOBS_CATALOG
from app.services.analysis import analyze_marks, confidence_from_matches, find_career_by_slug
from app.services.planner import generate_study_plan
from app.services.ml_prediction import predict_career

settings = get_settings()

SECRET_KEY = os.getenv("SECRET_KEY", "EDUPATH-super-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/admin/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin is None:
        raise credentials_exception
    return admin



@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=StatusResponse)
def healthcheck() -> StatusResponse:
    return StatusResponse(status="ok", service=settings.app_name)


@app.get(f"{settings.api_prefix}/bootstrap", response_model=BootstrapResponse)
def bootstrap_data(db: Session = Depends(get_db)) -> BootstrapResponse:
    careers = db.query(CareerPath).order_by(CareerPath.title).all()
    return BootstrapResponse(
        education_levels=["10th", "12th", "Graduation", "Postgraduate"],
        supported_subjects=["Maths", "Physics", "Chemistry", "Biology"],
        career_paths=[career.title for career in careers],
        future_ready_features=[
            "AI career chatbot with contextual roadmaps",
            "Community roadmap sharing and peer accountability",
            "Routine planner with daily energy-based scheduling",
        ],
    )


CAREER_SALARY_MAP = {
    "ai-ml-engineer": "₹40,000 - ₹70,000 / month",
    "data-scientist": "₹35,000 - ₹60,000 / month",
    "full-stack-web-developer": "₹30,000 - ₹50,000 / month",
    "cybersecurity-analyst": "₹30,000 - ₹55,000 / month",
    "healthcare-professional": "₹40,000 - ₹80,000 / month",
    "chartered-accountant": "₹35,000 - ₹60,000 / month",
    "corporate-lawyer": "₹35,000 - ₹65,000 / month",
    "business-manager": "₹55,000 - ₹95,000 / month",
}


@app.get(f"{settings.api_prefix}/opportunities", response_model=list[CareerRecommendationResponse])
def get_opportunities(db: Session = Depends(get_db)):
    careers = db.query(CareerPath).order_by(CareerPath.title).all()
    return [
        CareerRecommendationResponse(
            slug=c.slug,
            title=c.title,
            summary=c.summary,
            difficulty_level=c.difficulty_level,
            time_required=c.time_required,
            outlook=c.outlook,
            fit_reason=c.fit_reason,
            required_subjects=[i.strip() for i in c.required_subjects.split(",") if i.strip()],
            estimated_salary=CAREER_SALARY_MAP.get(c.slug, "Not available"),
        )
        for c in careers
    ]


@app.get(f"{settings.api_prefix}/govt-jobs", response_model=list[GovtJobResponse])
def get_govt_jobs():
    return GOVT_JOBS_CATALOG


@app.post(f"{settings.api_prefix}/admin/login", response_model=TokenResponse)
def admin_login(payload: AdminLoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == payload.email).first()
    if not admin or not pwd_context.verify(payload.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    return TokenResponse(access_token=access_token, token_type="bearer")


@app.get(f"{settings.api_prefix}/admin/users", response_model=list[AdminDashboardUserResponse])
def get_admin_users(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    users = db.query(User).options(
        joinedload(User.analyses).joinedload(Analysis.recommended_career),
        joinedload(User.roadmap_progress)
    ).all()
    
    response = []
    for user in users:
        latest_analysis = max(user.analyses, key=lambda a: a.created_at) if user.analyses else None
        
        recommended_path = latest_analysis.recommended_career.title if latest_analysis else None
        confidence = latest_analysis.confidence_score if latest_analysis else None
        
        completed_steps = sum(1 for p in user.roadmap_progress if p.completed)
        total_steps = len(latest_analysis.recommended_career.roadmap_steps) if latest_analysis else 0
        
        response.append(AdminDashboardUserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            state=user.state,
            interests=user.interests,
            education_level=user.education_level + (f" ({user.stream})" if user.stream else ""),
            recommended_path=recommended_path,
            success_probability=confidence,
            completed_steps=completed_steps,
            total_steps=total_steps
        ))
    return response


@app.get(f"{settings.api_prefix}/admin/careers", response_model=list[dict])
def get_admin_careers(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    careers = db.query(CareerPath).options(joinedload(CareerPath.roadmap_steps)).all()
    response = []
    for c in careers:
        phases = {}
        for step in c.roadmap_steps:
            phases.setdefault(step.phase, []).append({
                "id": step.id,
                "phase": step.phase,
                "step_order": step.step_order,
                "title": step.title,
                "description": step.description,
                "skill": step.skill,
                "resource": step.resource,
                "duration": step.duration,
                "outcome": step.outcome,
                "completed": False
            })
        roadmap = [{"phase": phase, "steps": steps} for phase, steps in phases.items()]
        response.append({
            "id": c.id,
            "slug": c.slug,
            "title": c.title,
            "roadmap": roadmap
        })
    return response


@app.put(f"{settings.api_prefix}/admin/roadmap-steps/{{step_id}}", response_model=ActionResponse)
def update_roadmap_step(step_id: int, payload: RoadmapStepUpdateRequest, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    step = db.get(RoadmapStep, step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Roadmap step not found")
    
    if payload.title is not None: step.title = payload.title
    if payload.description is not None: step.description = payload.description
    if payload.skill is not None: step.skill = payload.skill
    if payload.resource is not None: step.resource = payload.resource
    if payload.duration is not None: step.duration = payload.duration
    if payload.outcome is not None: step.outcome = payload.outcome
    
    db.commit()
    return ActionResponse(message="Roadmap step updated successfully")




@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
async def chat_with_gpt(payload: ChatRequest, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    latest_analysis = max(user.analyses, key=lambda a: a.created_at) if user.analyses else None
         
    context = ""
    career_title = ""
    if latest_analysis:
        career = latest_analysis.recommended_career
        career_title = career.title
        context = f"The student's recommended career is {career.title}. Their strong subjects are {latest_analysis.strong_subjects} and weak subjects are {latest_analysis.weak_subjects}."
        
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        import asyncio
        await asyncio.sleep(1.5) # Simulate API latency
        mock_response = f"I'm your AI counselor! (Simulated Mode - No API Key Found) I see you are aiming to be a {career_title}. That's a challenging but rewarding path. To succeed, focus on building strong daily habits around your core subjects and review your weak areas consistently. Keep going, {user.name}!"
        return ChatResponse(response=mock_response)
        
    client = openai.AsyncOpenAI(api_key=api_key)
    try:
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are an expert career counselor for EDUPATH. The user is a student named {user.name} ({user.education_level}). {context} Give concise, encouraging advice."},
                {"role": "user", "content": payload.message}
            ],
            max_tokens=300
        )
        return ChatResponse(response=completion.choices[0].message.content)
    except Exception as e:
        return ChatResponse(response=f"Error connecting to AI: {str(e)}")


@app.post(f"{settings.api_prefix}/analysis", response_model=DashboardResponse)
def create_analysis(payload: StudentAnalysisRequest, db: Session = Depends(get_db)) -> DashboardResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None:
        user = User(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            state=payload.state,
            education_level=payload.education_level,
            stream=payload.stream,
            interests=payload.interests,
            skills=payload.skills,
        )
        db.add(user)
        db.flush()
    else:
        user.name = payload.name
        user.phone = payload.phone
        user.state = payload.state
        user.education_level = payload.education_level
        user.stream = payload.stream
        user.interests = payload.interests
        user.skills = payload.skills

    marks = {
        "Maths": payload.maths,
        "Physics": payload.physics,
        "Chemistry": payload.chemistry,
        "Biology": payload.biology,
    }
    career_paths = db.query(CareerPath).options(
        joinedload(CareerPath.roadmap_steps),
        joinedload(CareerPath.insights),
    ).all()

    analysis_result = analyze_marks(
        marks,
        interest=payload.interests,
        skills=payload.skills,
        education_level=payload.education_level,
        stream=payload.stream,
        dream=payload.dream
    )
    
    # ML Model Prediction
    ml_result = predict_career(
        maths=payload.maths,
        physics=payload.physics,
        chemistry=payload.chemistry,
        biology=payload.biology,
        interests=payload.interests,
        skills=payload.skills,
        education_level=payload.education_level,
        stream=payload.stream,
        dream=payload.dream
    )
    
    matches = ml_result["matches"]
    confidence = ml_result["confidence_score"]
    recommended = find_career_by_slug(career_paths, ml_result["predicted_career"])

    analysis = Analysis(
        user=user,
        recommended_career=recommended,
        confidence_score=confidence,
        strong_subjects="|".join(analysis_result["strong_subjects"]),
        weak_subjects="|".join(analysis_result["weak_subjects"]),
        analysis_notes=build_student_message(
            analysis_result["strong_subjects"],
            analysis_result["weak_subjects"],
            recommended.title,
        ),
    )
    db.add(analysis)
    db.flush()

    for subject_name, marks_value in marks.items():
        db.add(
            SubjectScore(
                analysis_id=analysis.id,
                subject_name=subject_name,
                marks=marks_value,
                performance_band=analysis_result["score_bands"][subject_name],
            )
        )

    for match in matches[:3]:
        matched_path = find_career_by_slug(career_paths, match["career_slug"])
        db.add(
            CareerMatch(
                analysis_id=analysis.id,
                career_path_id=matched_path.id,
                score=match["score"],
                rationale=match["rationale"],
            )
        )

    current_plan = (
        db.query(StudyPlan)
        .filter(StudyPlan.user_id == user.id, StudyPlan.status == "active")
        .options(joinedload(StudyPlan.entries))
        .order_by(StudyPlan.created_at.desc())
        .first()
    )
    if current_plan:
        current_plan.status = "archived"

    user_subject_progress = db.query(SubjectProgress).filter(SubjectProgress.user_id == user.id).all()
    study_plan = generate_study_plan(
        user,
        recommended,
        analysis_result["weak_subjects"],
        analysis_result["strong_subjects"],
        user_subject_progress,
    )
    db.add(study_plan)
    db.commit()

    dashboard = fetch_dashboard_payload(user.id, db)
    if dashboard is None:
        raise HTTPException(status_code=500, detail="Failed to build dashboard response.")
    return dashboard


@app.post(f"{settings.api_prefix}/predict-career")
def api_predict_career(payload: StudentAnalysisRequest):
    result = predict_career(
        maths=payload.maths,
        physics=payload.physics,
        chemistry=payload.chemistry,
        biology=payload.biology,
        interests=payload.interests,
        skills=payload.skills,
        education_level=payload.education_level,
        stream=payload.stream,
        dream=payload.dream
    )
    return result


@app.get(f"{settings.api_prefix}/dashboard/{{user_id}}", response_model=DashboardResponse)
def get_dashboard(user_id: int, db: Session = Depends(get_db)) -> DashboardResponse:
    dashboard = fetch_dashboard_payload(user_id, db)
    if dashboard is None:
        raise HTTPException(status_code=404, detail="User dashboard not found.")
    return dashboard


@app.post(f"{settings.api_prefix}/roadmap-steps/{{step_id}}/complete", response_model=ActionResponse)
def complete_roadmap_step(
    step_id: int,
    payload: ProgressUpdateRequest,
    db: Session = Depends(get_db),
) -> ActionResponse:
    step = db.get(RoadmapStep, step_id)
    if step is None:
        raise HTTPException(status_code=404, detail="Roadmap step not found.")

    progress = (
        db.query(RoadmapProgress)
        .filter(
            RoadmapProgress.user_id == payload.user_id,
            RoadmapProgress.roadmap_step_id == step_id,
        )
        .first()
    )
    if progress is None:
        progress = RoadmapProgress(user_id=payload.user_id, roadmap_step_id=step_id, completed=True)
        db.add(progress)
    else:
        progress.completed = not progress.completed

    db.commit()
    return ActionResponse(message="Roadmap progress updated.")


@app.post(f"{settings.api_prefix}/subject-progress", response_model=ActionResponse)
def update_subject_progress(
    payload: SubjectProgressUpdateRequest,
    db: Session = Depends(get_db),
) -> ActionResponse:
    record = (
        db.query(SubjectProgress)
        .filter(
            SubjectProgress.user_id == payload.user_id,
            SubjectProgress.subject_name == payload.subject_name,
        )
        .first()
    )
    if record is None:
        record = SubjectProgress(
            user_id=payload.user_id,
            subject_name=payload.subject_name,
            completion_percentage=payload.completion_percentage,
        )
        db.add(record)
    else:
        record.completion_percentage = payload.completion_percentage

    db.commit()
    return ActionResponse(message="Subject progress saved.")


@app.post(f"{settings.api_prefix}/study-plan/refresh", response_model=DashboardResponse)
def refresh_study_plan(payload: StudyPlanRefreshRequest, db: Session = Depends(get_db)) -> DashboardResponse:
    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    latest_analysis = (
        db.query(Analysis)
        .filter(Analysis.user_id == user.id)
        .options(joinedload(Analysis.recommended_career))
        .order_by(Analysis.created_at.desc())
        .first()
    )
    if latest_analysis is None:
        raise HTTPException(status_code=404, detail="No analysis found for this user.")

    current_plan = db.query(StudyPlan).filter(StudyPlan.user_id == user.id, StudyPlan.status == "active").first()
    if current_plan:
        current_plan.status = "archived"

    subject_progress = db.query(SubjectProgress).filter(SubjectProgress.user_id == user.id).all()
    study_plan = generate_study_plan(
        user,
        latest_analysis.recommended_career,
        split_pipe_string(latest_analysis.weak_subjects),
        split_pipe_string(latest_analysis.strong_subjects),
        subject_progress,
    )
    db.add(study_plan)
    db.commit()

    dashboard = fetch_dashboard_payload(user.id, db)
    if dashboard is None:
        raise HTTPException(status_code=500, detail="Failed to refresh study plan.")
    return dashboard


def fetch_dashboard_payload(user_id: int, db: Session) -> DashboardResponse | None:
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .options(
            joinedload(User.analyses).joinedload(Analysis.subject_scores),
            joinedload(User.analyses).joinedload(Analysis.recommended_career).joinedload(CareerPath.roadmap_steps),
            joinedload(User.analyses).joinedload(Analysis.recommended_career).joinedload(CareerPath.insights),
            joinedload(User.analyses).joinedload(Analysis.career_matches),
            joinedload(User.study_plans).joinedload(StudyPlan.entries),
            joinedload(User.roadmap_progress),
            joinedload(User.subject_progress),
        )
        .first()
    )
    if user is None or not user.analyses:
        return None

    latest_analysis = max(user.analyses, key=lambda analysis: analysis.created_at)
    career = latest_analysis.recommended_career
    roadmap_completion = {entry.roadmap_step_id for entry in user.roadmap_progress if entry.completed}

    roadmap = []
    for phase in ("Beginner", "Intermediate", "Advanced"):
        phase_steps = [step for step in career.roadmap_steps if step.phase == phase]
        roadmap.append(
            {
                "phase": phase,
                "steps": [
                    {
                        "id": step.id,
                        "phase": step.phase,
                        "step_order": step.step_order,
                        "title": step.title,
                        "description": step.description,
                        "skill": step.skill,
                        "resource": step.resource,
                        "duration": step.duration,
                        "outcome": step.outcome,
                        "completed": step.id in roadmap_completion,
                    }
                    for step in phase_steps
                ],
            }
        )

    study_plan = max(user.study_plans, key=lambda plan: plan.created_at)
    subject_progress = {item.subject_name: item.completion_percentage for item in user.subject_progress}
    marks_breakdown = sorted(latest_analysis.subject_scores, key=lambda item: item.subject_name)
    completion_summary = {
        "completed_steps": sum(1 for phase in roadmap for step in phase["steps"] if step["completed"]),
        "total_steps": sum(len(phase["steps"]) for phase in roadmap),
    }

    career_lookup = {item.id: item for item in db.query(CareerPath).all()}

    completed_steps = completion_summary["completed_steps"]
    total_steps = completion_summary["total_steps"]
    roadmap_ratio = (completed_steps / total_steps) if total_steps > 0 else 0
    avg_subject_progress = (sum(subject_progress.values()) / max(len(subject_progress), 1)) / 100.0

    base_prob = latest_analysis.confidence_score
    predicted_success = base_prob * 0.4 + (roadmap_ratio * 100) * 0.4 + (avg_subject_progress * 100) * 0.2
    if completed_steps == 0 and sum(subject_progress.values()) == 0:
        predicted_success = latest_analysis.confidence_score
    success_probability = min(max(predicted_success, 10.0), 99.0)

    return DashboardResponse(
        user_id=user.id,
        student_name=user.name,
        created_at=latest_analysis.created_at,
        confidence_score=latest_analysis.confidence_score,
        strong_subjects=split_pipe_string(latest_analysis.strong_subjects),
        weak_subjects=split_pipe_string(latest_analysis.weak_subjects),
        message=latest_analysis.analysis_notes,
        marks_breakdown=[{"subject": item.subject_name, "marks": item.marks, "band": item.performance_band} for item in marks_breakdown],
        recommended_career={
            "slug": career.slug,
            "title": career.title,
            "summary": career.summary,
            "difficulty_level": career.difficulty_level,
            "time_required": career.time_required,
            "outlook": career.outlook,
            "fit_reason": career.fit_reason,
            "required_subjects": [item.strip() for item in career.required_subjects.split(",") if item.strip()],
            "estimated_salary": CAREER_SALARY_MAP.get(career.slug, "Not available"),
        },
        career_matches=[
            {
                "career_slug": career_lookup[match.career_path_id].slug,
                "title": career_lookup[match.career_path_id].title,
                "score": round(match.score, 2),
                "rationale": match.rationale,
            }
            for match in sorted(latest_analysis.career_matches, key=lambda item: item.score, reverse=True)
        ],
        roadmap=roadmap,
        study_plan={
            "id": study_plan.id,
            "title": study_plan.title,
            "status": study_plan.status,
            "adaptive_summary": study_plan.adaptive_summary,
            "weekly_hours": round(sum(entry.duration_hours for entry in study_plan.entries if not entry.is_break), 1),
            "entries": [
                {
                    "day_name": entry.day_name,
                    "day_order": entry.day_order,
                    "session_type": entry.session_type,
                    "subject_name": entry.subject_name,
                    "duration_hours": entry.duration_hours,
                    "objective": entry.objective,
                    "is_break": entry.is_break,
                }
                for entry in study_plan.entries
            ],
        },
        insights=[{"quote": insight.quote, "author": insight.author, "source": insight.source, "context": insight.context} for insight in career.insights],
        subject_progress=subject_progress,
        completion_summary=completion_summary,
        success_probability=round(success_probability, 1),
        future_ready_features=[
            "AI chatbot that can answer roadmap and exam-strategy questions",
            "Community roadmap sharing with public student playbooks",
            "Routine planner that adapts to attendance, sleep, and revision streaks",
        ],
    )


def split_pipe_string(value: str) -> list[str]:
    return [item for item in value.split("|") if item]


def build_student_message(strong_subjects: list[str], weak_subjects: list[str], career_title: str) -> str:
    if weak_subjects and strong_subjects:
        return f"{career_title} looks realistic for you, but {', '.join(weak_subjects)} need deliberate recovery so your progress stays sustainable."
    if strong_subjects:
        return f"{career_title} is a strong fit from your current profile. Use your strengths in {', '.join(strong_subjects)} to build momentum."
    return f"{career_title} is still possible, but your next gains will come from fixing fundamentals before chasing advanced topics."
