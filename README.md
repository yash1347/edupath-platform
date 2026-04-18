# EduPath AI

EduPath AI is a production-style career roadmap platform for students after 10th, 12th, or graduation. It analyzes marks and interests, recommends a realistic career direction, builds a phase-based roadmap, generates an adaptive weekly study plan, and tracks subject and roadmap progress.

## Tech stack

- Frontend: React, Axios, Recharts
- Backend: FastAPI, SQLAlchemy ORM
- Database: PostgreSQL-ready schema with a local SQLite fallback for immediate startup

## Project structure

```text
Edupath/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── services/
│   │   │   ├── analysis.py
│   │   │   └── planner.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── seed.py
│   ├── .env
│   ├── .env.example
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api.js
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
└── README.md
```

## Core features shipped

- User analysis system with strong subjects, weak subjects, recommended career, and confidence score
- Career roadmap system with Beginner, Intermediate, and Advanced phases
- Smart adaptive study planner with breaks, revision, and progress-aware balancing
- Progress tracking for roadmap steps and subject-level completion
- Career insights using seeded real quotes with practical context
- Dashboard charts for marks bands, strong vs weak distribution, and confidence level
- Future-ready product cards for AI chatbot, community sharing, and routine planner

## Database design

Main tables:

- `users`
- `career_paths`
- `roadmap_steps`
- `career_insights`
- `analyses`
- `subject_scores`
- `career_matches`
- `study_plans`
- `study_plan_entries`
- `roadmap_progress`
- `subject_progress`

Relationships:

- One user has many analyses, study plans, roadmap progress records, and subject progress records
- One career path has many roadmap steps and insights
- One analysis stores many subject scores and top career matches
- One study plan stores many study plan entries

## Run locally

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Notes:

- Current local `.env` uses SQLite so the app starts immediately.
- For PostgreSQL, replace `DATABASE_URL` in `backend/.env` with your Postgres connection string.
- Seed data is inserted automatically on startup.

### 2. Frontend

```bash
cd frontend
npm install
npm start
```

The React app runs on `http://localhost:3000` and talks to the API at `http://127.0.0.1:8000`.

## Verified checks

- Backend module import smoke test succeeded
- Backend seed + analysis smoke test succeeded
- Frontend test suite passed
- Frontend production build passed

## Example student profile

Use this in the UI:

- Name: `Test Student`
- Email: `test@example.com`
- Education level: `After 12th`
- Interests: `AI and machine learning`
- Skills: `Python basics and problem solving`
- Maths: `88`
- Physics: `81`
- Chemistry: `64`
- Biology: `45`

## API overview

- `GET /health`
- `GET /api/v1/bootstrap`
- `POST /api/v1/analysis`
- `GET /api/v1/dashboard/{user_id}`
- `POST /api/v1/roadmap-steps/{step_id}/complete`
- `POST /api/v1/subject-progress`
- `POST /api/v1/study-plan/refresh`
