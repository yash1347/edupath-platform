from collections import defaultdict

from app.models import CareerPath, StudyPlan, StudyPlanEntry, SubjectProgress, User

DAYS = [
    ("Monday", 1),
    ("Tuesday", 2),
    ("Wednesday", 3),
    ("Thursday", 4),
    ("Friday", 5),
    ("Saturday", 6),
    ("Sunday", 7),
]


def generate_study_plan(
    user: User,
    career_path: CareerPath,
    weak_subjects: list[str],
    strong_subjects: list[str],
    subject_progress: list[SubjectProgress],
) -> StudyPlan:
    progress_lookup = {item.subject_name: item.completion_percentage for item in subject_progress}
    focus_subjects = build_focus_subjects(career_path.required_subjects, weak_subjects, strong_subjects)

    plan = StudyPlan(
        user_id=user.id,
        focus_career_id=career_path.id,
        title=f"{career_path.title} weekly focus sprint",
        status="active",
        adaptive_summary=build_adaptive_summary(weak_subjects, progress_lookup),
    )

    entries = []
    for day_name, day_order in DAYS:
        entries.extend(build_day_schedule(day_name, day_order, focus_subjects, progress_lookup))

    plan.entries = entries
    return plan


def build_focus_subjects(required_subjects_csv: str, weak_subjects: list[str], strong_subjects: list[str]) -> list[dict]:
    base_subjects = [subject.strip() for subject in required_subjects_csv.split(",") if subject.strip()]
    priorities = defaultdict(lambda: {"hours": 2.0, "objective": "Revise concepts and solve practice questions."})

    for subject in base_subjects:
        if subject in weak_subjects:
            priorities[subject] = {
                "hours": 2.5,
                "objective": "Recover weak concepts with focused revision and active practice.",
            }
        elif subject in strong_subjects:
            priorities[subject] = {
                "hours": 1.25,
                "objective": "Maintain strength through short practice and spaced review.",
            }
        else:
            priorities[subject] = {
                "hours": 2.0,
                "objective": "Study concepts and solve practice questions."
            }

    return [{"subject": subject, **payload} for subject, payload in priorities.items()]


def build_day_schedule(day_name: str, day_order: int, focus_subjects: list[dict], progress_lookup: dict[str, int]) -> list[StudyPlanEntry]:
    day_entries: list[StudyPlanEntry] = []

    if day_name in {"Saturday", "Sunday"}:
        day_entries.append(
            StudyPlanEntry(
                day_name=day_name,
                day_order=day_order,
                session_type="Revision",
                subject_name="Revision Block",
                duration_hours=2.0,
                objective="Review mistakes from the week and attempt a timed practice set.",
                is_break=False,
            )
        )
        day_entries.append(
            StudyPlanEntry(
                day_name=day_name,
                day_order=day_order,
                session_type="Reflection",
                subject_name="Weekly Reflection",
                duration_hours=0.5,
                objective="Check progress, update priorities, and reset the next week.",
                is_break=False,
            )
        )
        return day_entries

    active_subjects = focus_subjects[:3] if day_order % 2 else focus_subjects[1:4] or focus_subjects[:3]
    for index, subject in enumerate(active_subjects):
        completion = progress_lookup.get(subject["subject"], 0)
        hours = max(1.0, round(subject["hours"] - (completion / 100) * 0.75, 2))
        day_entries.append(
            StudyPlanEntry(
                day_name=day_name,
                day_order=day_order,
                session_type="Deep Work" if index == 0 else "Practice",
                subject_name=subject["subject"],
                duration_hours=hours,
                objective=subject["objective"],
                is_break=False,
            )
        )
        if index < len(active_subjects) - 1:
            day_entries.append(
                StudyPlanEntry(
                    day_name=day_name,
                    day_order=day_order,
                    session_type="Break",
                    subject_name="Break",
                    duration_hours=0.5,
                    objective="Take a real break before the next session.",
                    is_break=True,
                )
            )

    day_entries.append(
        StudyPlanEntry(
            day_name=day_name,
            day_order=day_order,
            session_type="Light Review",
            subject_name="Daily Recall",
            duration_hours=0.5,
            objective="End with quick recall, flashcards, or self-testing.",
            is_break=False,
        )
    )
    return day_entries


def build_adaptive_summary(weak_subjects: list[str], progress_lookup: dict[str, int]) -> str:
    if weak_subjects:
        return f"More hours were assigned to {', '.join(weak_subjects)} because they need recovery work."
    if progress_lookup:
        strongest = max(progress_lookup, key=progress_lookup.get)
        return f"Study time was reduced slightly for {strongest} because your recorded progress is improving."
    return "The plan balances concept-building, revision, and recovery breaks across the week."
