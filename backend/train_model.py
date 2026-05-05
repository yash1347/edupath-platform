import os
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Synthetic Data Generation
NUM_SAMPLES = 2000

CAREERS = [
    "ai-ml-engineer",
    "data-scientist",
    "full-stack-web-developer",
    "cybersecurity-analyst",
    "healthcare-professional",
    "chartered-accountant",
    "corporate-lawyer",
    "business-manager"
]

def generate_synthetic_data():
    data = []
    for _ in range(NUM_SAMPLES):
        career = random.choice(CAREERS)
        
        # Base distributions based on career
        if career == "ai-ml-engineer":
            maths = random.randint(75, 100)
            physics = random.randint(70, 95)
            chemistry = random.randint(50, 80)
            biology = random.randint(40, 70)
            interests = random.choice(["artificial intelligence, coding, robots", "machine learning, automation, math", "programming, algorithms"])
            skills = random.choice(["python, logical thinking", "c++, math", "problem solving, coding"])
            edu = random.choice(["12th", "Graduation", "Postgraduate"])
            
        elif career == "data-scientist":
            maths = random.randint(80, 100)
            physics = random.randint(60, 90)
            chemistry = random.randint(50, 80)
            biology = random.randint(40, 70)
            interests = random.choice(["data, statistics, analytics", "business intelligence, numbers", "research, trends"])
            skills = random.choice(["sql, python", "statistics, excel", "data visualization"])
            edu = random.choice(["Graduation", "Postgraduate"])
            
        elif career == "full-stack-web-developer":
            maths = random.randint(60, 90)
            physics = random.randint(50, 85)
            chemistry = random.randint(40, 75)
            biology = random.randint(40, 70)
            interests = random.choice(["web design, apps, software", "internet, building websites", "coding, UI/UX"])
            skills = random.choice(["html, css, javascript", "react, node", "creativity, coding"])
            edu = random.choice(["10th", "12th", "Graduation"])
            
        elif career == "cybersecurity-analyst":
            maths = random.randint(65, 95)
            physics = random.randint(65, 95)
            chemistry = random.randint(40, 80)
            biology = random.randint(40, 70)
            interests = random.choice(["hacking, security, networks", "cyber, computers, privacy", "investigation, tech"])
            skills = random.choice(["linux, networking", "ethical hacking, scripting", "problem solving, attention to detail"])
            edu = random.choice(["12th", "Graduation"])
            
        elif career == "healthcare-professional":
            maths = random.randint(40, 80)
            physics = random.randint(65, 95)
            chemistry = random.randint(75, 100)
            biology = random.randint(80, 100)
            interests = random.choice(["medicine, helping people, biology", "healthcare, doctors, anatomy", "science, patients"])
            skills = random.choice(["empathy, memory", "science, hard work", "biology, chemistry"])
            edu = random.choice(["12th", "Graduation"])
            
        elif career == "chartered-accountant":
            maths = random.randint(75, 100)
            physics = random.randint(40, 80)
            chemistry = random.randint(40, 70)
            biology = random.randint(40, 70)
            interests = random.choice(["finance, money, business", "accounts, taxation, auditing", "economics, stock market"])
            skills = random.choice(["numbers, accounting", "analytical skills, excel", "hard work, memory"])
            edu = random.choice(["12th", "Graduation"])
            
        elif career == "corporate-lawyer":
            maths = random.randint(40, 80)
            physics = random.randint(40, 70)
            chemistry = random.randint(40, 70)
            biology = random.randint(40, 70)
            interests = random.choice(["law, debate, justice", "corporate law, reading, politics", "business law, arguments"])
            skills = random.choice(["reading, communication", "logical reasoning, public speaking", "writing, analysis"])
            edu = random.choice(["12th", "Graduation"])
            
        elif career == "business-manager":
            maths = random.randint(60, 95)
            physics = random.randint(40, 80)
            chemistry = random.randint(40, 70)
            biology = random.randint(40, 70)
            interests = random.choice(["leadership, business, startups", "marketing, management, sales", "strategy, operations"])
            skills = random.choice(["communication, leadership", "teamwork, problem solving", "networking, strategy"])
            edu = random.choice(["Graduation", "Postgraduate"])
            
        data.append({
            "maths": maths,
            "physics": physics,
            "chemistry": chemistry,
            "biology": biology,
            "interests": interests,
            "skills": skills,
            "education_level": edu,
            "career": career
        })
        
    return pd.DataFrame(data)

def train_and_save_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    # Save a sample just for reference (optional)
    df.to_csv(os.path.join(os.path.dirname(__file__), "synthetic_dataset.csv"), index=False)
    
    X = df.drop("career", axis=1)
    y = df["career"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing
    numeric_features = ["maths", "physics", "chemistry", "biology"]
    numeric_transformer = StandardScaler()
    
    text_features = "interests" # We'll combine text features later or use separate Tfidf
    # We will combine interests and skills into a single text feature for simplicity in pipeline
    # Wait, pipeline ColumnTransformer can apply TfidfVectorizer to specific columns
    # but TfidfVectorizer expects a 1D array. So we apply it separately to 'interests' and 'skills'
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["education_level"]),
            ("text_int", TfidfVectorizer(max_features=50), "interests"),
            ("text_skill", TfidfVectorizer(max_features=50), "skills"),
        ]
    )
    
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))
    
    model_path = os.path.join(os.path.dirname(__file__), "app", "ml_model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
