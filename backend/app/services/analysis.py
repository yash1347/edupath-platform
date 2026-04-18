from collections import OrderedDict

from app.models import CareerPath

SUBJECTS = ("Maths", "Physics", "Chemistry", "Biology")

SUBJECT_WEIGHTS = {
    "ai-ml-engineer": {"Maths": 1.35, "Physics": 1.0, "Chemistry": 0.45, "Biology": 0.3},
    "data-scientist": {"Maths": 1.4, "Physics": 0.75, "Chemistry": 0.4, "Biology": 0.35},
    "full-stack-web-developer": {"Maths": 0.9, "Physics": 0.6, "Chemistry": 0.35, "Biology": 0.25},
    "cybersecurity-analyst": {"Maths": 1.0, "Physics": 0.95, "Chemistry": 0.35, "Biology": 0.2},
    "healthcare-professional": {"Maths": 0.3, "Physics": 0.7, "Chemistry": 1.1, "Biology": 1.45},
}

KEYWORD_BONUSES = {
    "ai-ml-engineer": {"ai": 24, "machine learning": 24, "python": 14, "automation": 10, "math": 10, "algorithms": 16},
    "data-scientist": {"data": 22, "analytics": 18, "statistics": 18, "sql": 12, "business": 8, "research": 8},
    "full-stack-web-developer": {"web": 20, "frontend": 18, "backend": 18, "react": 16, "javascript": 18, "html": 12, "css": 12, "design": 8},
    "cybersecurity-analyst": {"security": 24, "cyber": 24, "network": 18, "linux": 14, "forensics": 14, "ethical hacking": 20},
    "healthcare-professional": {"medical": 24, "medicine": 24, "doctor": 24, "healthcare": 20, "biology": 12, "neet": 18, "patient": 10},
}

EDUCATION_BONUSES = {
    "10th": {"full-stack-web-developer": 8, "ai-ml-engineer": 4, "cybersecurity-analyst": 4},
    "12th": {"healthcare-professional": 8, "data-scientist": 6, "ai-ml-engineer": 6},
    "graduation": {"data-scientist": 8, "ai-ml-engineer": 8, "cybersecurity-analyst": 6, "full-stack-web-developer": 6},
    "postgraduate": {"data-scientist": 10, "ai-ml-engineer": 10, "cybersecurity-analyst": 8, "healthcare-professional": 6},
}


def band_for_marks(marks: int) -> str:
    if marks >= 80:
        return "Strong"
    if marks >= 60:
        return "Average"
    return "Weak"


def analyze_marks(
    marks: dict[str, int],
    interest: str = "",
    skills: str = "",
    education_level: str = "",
) -> dict:
    ordered_marks = OrderedDict((subject, int(marks[subject])) for subject in SUBJECTS)
    strong_subjects = [subject for subject, score in ordered_marks.items() if score >= 75]
    weak_subjects = [subject for subject, score in ordered_marks.items() if score < 60]

    return {
        "strong_subjects": strong_subjects,
        "weak_subjects": weak_subjects,
        "score_bands": {subject: band_for_marks(score) for subject, score in ordered_marks.items()},
        "matches": score_careers(ordered_marks, interest, skills, education_level),
    }


def score_careers(marks: OrderedDict[str, int], interest: str, skills: str, education_level: str) -> list[dict]:
    profile_text = f"{interest} {skills}".lower()
    education = education_level.lower()
    results = []

    for career_slug, weights in SUBJECT_WEIGHTS.items():
        subject_score = sum(marks[subject] * weight for subject, weight in weights.items()) / 4
        keyword_score = sum(bonus for keyword, bonus in KEYWORD_BONUSES[career_slug].items() if keyword in profile_text)
        education_score = 0
        for token, boosts in EDUCATION_BONUSES.items():
            if token in education:
                education_score += boosts.get(career_slug, 0)

        total_score = round(subject_score + keyword_score + education_score, 2)
        results.append(
            {
                "career_slug": career_slug,
                "score": total_score,
                "rationale": build_rationale(career_slug, marks, keyword_score, education_score),
            }
        )

    return sorted(results, key=lambda item: item["score"], reverse=True)


def build_rationale(career_slug: str, marks: OrderedDict[str, int], keyword_score: float, education_score: float) -> str:
    strongest_subject = max(marks, key=marks.get)
    reasons = [f"Your best current academic signal is {strongest_subject}."]
    if keyword_score:
        reasons.append("Your interests and stated skills align with this direction.")
    if education_score:
        reasons.append("Your current education stage makes the timing realistic.")
    if not keyword_score and not education_score:
        reasons.append("This is mainly driven by your subject profile, so project exposure will matter.")
    return " ".join(reasons)


def confidence_from_matches(matches: list[dict]) -> float:
    if not matches:
        return 50.0
    top_score = matches[0]["score"]
    runner_up = matches[1]["score"] if len(matches) > 1 else max(top_score * 0.65, 1)
    spread = max(top_score - runner_up, 0)
    confidence = min(95.0, max(52.0, 60.0 + (spread / max(top_score, 1)) * 40.0))
    return round(confidence, 1)


def find_career_by_slug(career_paths: list[CareerPath], slug: str) -> CareerPath:
    for career_path in career_paths:
        if career_path.slug == slug:
            return career_path
    raise ValueError(f"Career path not found for slug '{slug}'")
