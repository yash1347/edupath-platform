from app.services.analysis import analyze_marks


def analyze_subjects(data):
    result = analyze_marks(data)
    return result["strong_subjects"], result["weak_subjects"]


def suggest_career(marks, interest):
    result = analyze_marks(marks, interest=interest, skills="", education_level="")
    return result["matches"][0]["career_slug"]
