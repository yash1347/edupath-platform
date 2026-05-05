import os
import joblib
import pandas as pd
from typing import Dict, Any

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_model.joblib")
_model = None

def load_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return _model

def predict_career(maths: int, physics: int, chemistry: int, biology: int, interests: str, skills: str, education_level: str, stream: str | None = None, dream: str = "") -> Dict[str, Any]:
    model = load_model()
    
    # Create a DataFrame for the input
    input_data = pd.DataFrame([{
        "maths": maths,
        "physics": physics,
        "chemistry": chemistry,
        "biology": biology,
        "interests": interests,
        "skills": skills,
        "education_level": education_level
    }])
    
    predicted_class = model.predict(input_data)[0]
    
    # Calculate confidence probabilities using predict_proba
    probabilities = model.predict_proba(input_data)[0]
    classes = model.classes_
    
    # Create a ranked list of matches
    matches = []
    for cls, prob in zip(classes, probabilities):
        matches.append({
            "career_slug": cls,
            "score": round(prob * 100, 2),
            "rationale": f"The ML model assigned a {round(prob * 100, 2)}% confidence to this career based on your profile."
        })
        
    matches = sorted(matches, key=lambda x: x["score"], reverse=True)
    
    return {
        "predicted_career": predicted_class,
        "confidence_score": matches[0]["score"],
        "matches": matches
    }
