from sqlalchemy.orm import Session

from app.models import Admin, CareerInsight, CareerPath, RoadmapStep
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


CAREER_CATALOG = [
    {
        "slug": "ai-ml-engineer",
        "title": "AI / ML Engineer",
        "summary": "Build intelligent products by combining programming, mathematics, and model-building.",
        "difficulty_level": "High",
        "time_required": "18-30 months",
        "outlook": "Best for students who enjoy logic, experimentation, and building technology with real-world impact.",
        "fit_reason": "Strong maths and problem-solving make this path realistic, but it demands patience with theory and projects.",
        "required_subjects": "Maths, Physics, Computer Science, Statistics",
        "keyword_profile": "ai,machine learning,python,data,automation,algorithms,maths",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Strengthen coding and quantitative basics",
                "description": "Cover Python, algebra, functions, probability, and clean problem-solving habits before touching advanced ML.",
                "skill": "Python and applied maths",
                "resource": "CS50P, Khan Academy, Kaggle micro-courses",
                "duration": "8 weeks",
                "outcome": "You can solve beginner coding problems and read basic model-building tutorials.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "Build machine learning foundations",
                "description": "Learn supervised learning, feature engineering, evaluation metrics, and model debugging through small projects.",
                "skill": "Machine learning workflow",
                "resource": "Andrew Ng ML Specialization, scikit-learn projects",
                "duration": "12 weeks",
                "outcome": "You can train, evaluate, and explain baseline ML models.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "Ship a portfolio with specialization",
                "description": "Choose NLP, computer vision, or analytics automation and publish polished portfolio projects with documentation.",
                "skill": "Specialized AI portfolio",
                "resource": "Hugging Face tutorials, deployment projects, internships",
                "duration": "16 weeks",
                "outcome": "You are ready for internships, hackathons, and AI-focused entry roles.",
            },
        ],
        "insights": [
            {
                "quote": "Stay hungry, stay foolish.",
                "author": "Steve Jobs",
                "source": "Stanford Commencement Address",
                "context": "AI careers reward curiosity because the tools change quickly and the best builders keep learning.",
            },
            {
                "quote": "It's not a faith in technology. It's faith in people.",
                "author": "Steve Jobs",
                "source": "Rolling Stone interview",
                "context": "Useful AI work is not just model accuracy. It is building products that solve human problems.",
            },
        ],
    },
    {
        "slug": "data-scientist",
        "title": "Data Scientist",
        "summary": "Turn messy data into insights, forecasts, and business decisions using statistics and programming.",
        "difficulty_level": "High",
        "time_required": "15-24 months",
        "outlook": "A strong fit for students who like maths, patterns, and making decisions with evidence instead of guesswork.",
        "fit_reason": "High-scoring quantitative subjects and analytical interests usually translate well here.",
        "required_subjects": "Maths, Statistics, Economics, Computer Science",
        "keyword_profile": "data,analytics,statistics,sql,python,business,intelligence,maths",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Learn spreadsheet thinking and statistics",
                "description": "Start with descriptive statistics, Excel or Sheets, and a beginner Python workflow for data handling.",
                "skill": "Data literacy",
                "resource": "Khan Academy statistics, Excel case studies, pandas basics",
                "duration": "6 weeks",
                "outcome": "You can clean simple datasets and explain basic trends clearly.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "Query and visualize real datasets",
                "description": "Practice SQL, dashboards, exploratory analysis, and communicating recommendations from real-world datasets.",
                "skill": "Analytics workflow",
                "resource": "Mode SQL tutorials, Tableau Public, public datasets",
                "duration": "10 weeks",
                "outcome": "You can answer business-style questions from raw data.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "Build predictive case studies",
                "description": "Publish end-to-end case studies with hypotheses, evaluation, and tradeoffs rather than just notebooks.",
                "skill": "Decision-ready modelling",
                "resource": "Kaggle, open government data, portfolio blog",
                "duration": "12 weeks",
                "outcome": "You have a portfolio that looks closer to real analyst or junior DS work.",
            },
        ],
        "insights": [
            {
                "quote": "In God we trust. All others must bring data.",
                "author": "W. Edwards Deming",
                "source": "Management quote",
                "context": "This path values evidence. Clear reasoning matters more than flashy dashboards.",
            },
            {
                "quote": "Without data, you're just another person with an opinion.",
                "author": "W. Edwards Deming",
                "source": "Quality management quote",
                "context": "Data science is persuasive only when the underlying analysis is sound and reproducible.",
            },
        ],
    },
    {
        "slug": "full-stack-web-developer",
        "title": "Full-Stack Web Developer",
        "summary": "Design, build, and deploy web applications across frontend interfaces and backend systems.",
        "difficulty_level": "Medium",
        "time_required": "9-18 months",
        "outlook": "Great for students who like visible progress, practical building, and learning by creating projects.",
        "fit_reason": "This path can be entered faster than some others, but consistency and shipping projects matter a lot.",
        "required_subjects": "Maths, English, Computer Science, Design basics",
        "keyword_profile": "web,frontend,backend,react,javascript,html,css,node,api",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Master browser fundamentals",
                "description": "Learn semantic HTML, responsive CSS, JavaScript basics, and how the browser actually renders a page.",
                "skill": "Frontend foundations",
                "resource": "MDN Web Docs, freeCodeCamp responsive web projects",
                "duration": "6 weeks",
                "outcome": "You can build polished responsive pages without copying templates blindly.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "Build React apps with APIs",
                "description": "Move into component design, state, forms, async data, and collaboration with backend APIs.",
                "skill": "Application architecture",
                "resource": "React docs, project-based tutorials, REST API practice",
                "duration": "10 weeks",
                "outcome": "You can build interactive apps with reusable components and real data.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "Add backend, auth, and deployment",
                "description": "Learn databases, service architecture, deployment, and the polish needed for production apps.",
                "skill": "Full-stack delivery",
                "resource": "FastAPI or Node projects, Vercel/Render deployments",
                "duration": "12 weeks",
                "outcome": "You can ship portfolio projects that feel close to startup work.",
            },
        ],
        "insights": [
            {
                "quote": "Programs must be written for people to read.",
                "author": "Harold Abelson",
                "source": "Structure and Interpretation of Computer Programs",
                "context": "Readable code is a real competitive advantage on collaborative product teams.",
            },
            {
                "quote": "Simplicity is prerequisite for reliability.",
                "author": "Edsger W. Dijkstra",
                "source": "EWD report",
                "context": "Strong web products are often the result of small clear systems, not clever complexity.",
            },
        ],
    },
    {
        "slug": "cybersecurity-analyst",
        "title": "Cybersecurity Analyst",
        "summary": "Protect systems, investigate threats, and reduce security risk across networks and applications.",
        "difficulty_level": "High",
        "time_required": "12-24 months",
        "outlook": "Ideal for students who enjoy systems thinking, investigation, and methodical practice.",
        "fit_reason": "Security careers need patience. You have to understand how systems work before you can defend them well.",
        "required_subjects": "Maths, Computer Science, Networking, Logical reasoning",
        "keyword_profile": "security,cyber,network,linux,incident,hacking,defense",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Understand systems and networking",
                "description": "Learn operating systems, networking basics, command line workflows, and how common attacks happen.",
                "skill": "Security fundamentals",
                "resource": "TryHackMe beginner paths, networking labs, Linux practice",
                "duration": "8 weeks",
                "outcome": "You can explain core security concepts instead of memorizing terms.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "Practice detection and hardening",
                "description": "Work through vulnerability scanning, log analysis, web security basics, and defensive configuration.",
                "skill": "Defensive operations",
                "resource": "OWASP labs, Security Blue Team labs, home lab exercises",
                "duration": "10 weeks",
                "outcome": "You can identify weak points and document concrete improvements.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "Choose a security specialization",
                "description": "Explore SOC workflows, cloud security, penetration testing, or digital forensics with focused projects.",
                "skill": "Role specialization",
                "resource": "Blue/Red team labs, certification prep, portfolio writeups",
                "duration": "14 weeks",
                "outcome": "You have a clearer path into a specific entry-level security role.",
            },
        ],
        "insights": [
            {
                "quote": "Security is a process, not a product.",
                "author": "Bruce Schneier",
                "source": "Crypto-Gram",
                "context": "This career is realistic only if you like continuous learning and disciplined habits, not one-time fixes.",
            },
            {
                "quote": "Only amateurs attack machines; professionals target people.",
                "author": "Bruce Schneier",
                "source": "Security quote",
                "context": "Security work is technical, but human behavior is often the real risk surface.",
            },
        ],
    },
    {
        "slug": "healthcare-professional",
        "title": "Healthcare Professional",
        "summary": "Pursue medicine, nursing, pharmacy, or allied health through disciplined science study and service-minded work.",
        "difficulty_level": "High",
        "time_required": "36-72 months",
        "outlook": "A fit for students with strong biology interest, scientific discipline, and willingness for long preparation cycles.",
        "fit_reason": "This path is rewarding but demanding. It requires consistency over years, not short bursts of motivation.",
        "required_subjects": "Biology, Chemistry, Physics, Communication",
        "keyword_profile": "medical,medicine,doctor,healthcare,biology,neet,patient,clinical",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Build science depth and study discipline",
                "description": "Strengthen biology, chemistry, and timed revision habits before aiming at competitive exams or long-form coursework.",
                "skill": "Science mastery",
                "resource": "NCERT-focused revision, structured coaching, topic tests",
                "duration": "10 weeks",
                "outcome": "Your foundations become stable enough for serious entrance preparation.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "Train for exam pressure and recall",
                "description": "Use mock papers, error logs, spaced revision, and topic blocks to improve accuracy under time pressure.",
                "skill": "Exam readiness",
                "resource": "Mock test series, revision trackers, doubt review",
                "duration": "16 weeks",
                "outcome": "You can sustain preparation with measurable accuracy gains.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "Explore realistic healthcare branches",
                "description": "Map the differences between MBBS, nursing, pharmacy, physiotherapy, and allied health pathways with admission research.",
                "skill": "Career navigation",
                "resource": "College research, counselor sessions, alumni conversations",
                "duration": "6 weeks",
                "outcome": "You choose a branch with clearer expectations about cost, time, and workload.",
            },
        ],
        "insights": [
            {
                "quote": "Wherever the art of Medicine is loved, there is also a love of Humanity.",
                "author": "Hippocrates",
                "source": "Attributed medical quote",
                "context": "Healthcare is not only academic performance. Service, ethics, and emotional stamina matter too.",
            },
            {
                "quote": "Let food be thy medicine and medicine be thy food.",
                "author": "Hippocrates",
                "source": "Attributed medical quote",
                "context": "Medicine asks for disciplined fundamentals. Strong basics matter more than cramming inspiration.",
            },
        ],
    },
    {
        "slug": "chartered-accountant",
        "title": "Chartered Accountant (CA)",
        "summary": "Manage finance, audit, taxation, and corporate governance for organizations globally.",
        "difficulty_level": "Very High",
        "time_required": "4-5 years",
        "outlook": "Ideal for students with strong numerical skills, patience, and business acumen.",
        "fit_reason": "High demand in finance. Requires clearing highly competitive ICAI exams and completing rigorous articleship.",
        "required_subjects": "Commerce, Accounts, Maths, Economics",
        "keyword_profile": "finance,accounts,audit,taxation,ca,cma,business,economics,commerce",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Clear CA Foundation",
                "description": "Register with ICAI and pass the CA Foundation exam (Principles of Accounting, Business Laws, Maths).",
                "skill": "Accounting Fundamentals",
                "resource": "ICAI Study Material, online coaching for CA Foundation",
                "duration": "6 months",
                "outcome": "You have a solid grasp of basic accounting and business laws.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "CA Intermediate & Articleship",
                "description": "Clear the CA Intermediate groups and secure an articleship under a practicing CA for 3 years.",
                "skill": "Advanced Taxation & Auditing",
                "resource": "ICAI Modules, Mock test papers, Practical training",
                "duration": "3 years",
                "outcome": "Practical exposure to real-world auditing, taxation, and compliance.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "CA Final Exam",
                "description": "Clear the rigorous CA Final exams while completing your articleship.",
                "skill": "Corporate Financial Reporting",
                "resource": "Intensive revision test papers (RTPs), CA Final coaching",
                "duration": "1 year",
                "outcome": "You become a certified Chartered Accountant.",
            },
        ],
        "insights": [
            {
                "quote": "Accounting is the language of business.",
                "author": "Warren Buffett",
                "source": "Investment Principles",
                "context": "Mastering accounting gives you the foundation to understand and advise any business globally.",
            },
            {
                "quote": "Success in CA is 99% perspiration and 1% inspiration.",
                "author": "Anonymous CA",
                "source": "ICAI Community",
                "context": "The very low pass rates mean that disciplined study habits matter far more than raw intelligence.",
            },
        ],
    },
    {
        "slug": "corporate-lawyer",
        "title": "Corporate Lawyer",
        "summary": "Navigate legal frameworks, corporate mergers, intellectual property, and litigation.",
        "difficulty_level": "High",
        "time_required": "5 years",
        "outlook": "Great for students with excellent reading, analytical, and communication skills.",
        "fit_reason": "A 5-year integrated BA LLB through top National Law Universities (NLUs) provides high entry salaries.",
        "required_subjects": "English, History, Political Science, Logical Reasoning",
        "keyword_profile": "law,legal,lawyer,corporate,clat,litigation,judiciary,advocate,arts",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Crack CLAT or Law Entrances",
                "description": "Prepare for the Common Law Admission Test (CLAT) focusing on reading comprehension, logical reasoning, and current affairs.",
                "skill": "Logical Reasoning & Reading",
                "resource": "CLAT past papers, daily newspaper reading (The Hindu)",
                "duration": "1 year",
                "outcome": "Secure admission into a top National Law University (NLU) or reputed law school.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "Law School & Internships",
                "description": "Study constitutional, criminal, and corporate law. Intern with NGOs, trial courts, and law firms.",
                "skill": "Legal Drafting & Research",
                "resource": "SCC Online, Moot Court competitions",
                "duration": "3 years",
                "outcome": "You can draft legal notices and understand judicial precedents.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "Specialization & Placement",
                "description": "Focus on corporate law, intellectual property, or litigation. Secure pre-placement offers (PPOs) in top firms.",
                "skill": "Corporate Negotiation",
                "resource": "Tier-1 Law Firm internships",
                "duration": "1 year",
                "outcome": "You graduate as an advocate ready for corporate or litigation roles.",
            },
        ],
        "insights": [
            {
                "quote": "The leading rule for the lawyer, as for the man of every other calling, is diligence.",
                "author": "Abraham Lincoln",
                "source": "Notes for a Law Lecture",
                "context": "Legal practice requires extensive reading, preparation, and attention to the smallest details.",
            },
            {
                "quote": "A lawyer’s time and advice are his stock in trade.",
                "author": "Abraham Lincoln",
                "source": "Legal quotes",
                "context": "Your ability to communicate complex legal realities clearly is what clients will pay for.",
            },
        ],
    },
    {
        "slug": "business-manager",
        "title": "Business Manager (MBA)",
        "summary": "Lead operations, marketing, or strategy for enterprises by combining analytical and people skills.",
        "difficulty_level": "Medium to High",
        "time_required": "2 years (Post Graduation)",
        "outlook": "Perfect for students with leadership qualities and cross-functional interests.",
        "fit_reason": "High-paying roles await those who graduate from top B-Schools (IIMs). Requires cracking the CAT exam.",
        "required_subjects": "Maths, English, Business Studies, Economics",
        "keyword_profile": "business,management,mba,cat,marketing,operations,strategy,finance,manager",
        "roadmap": [
            {
                "phase": "Beginner",
                "step_order": 1,
                "title": "Build a Strong Undergraduate Profile",
                "description": "Maintain high grades in your B.Com/BBA/B.Tech, join leadership roles in college clubs, and prepare for CAT.",
                "skill": "Quantitative Aptitude & Leadership",
                "resource": "Arun Sharma CAT books, college leadership roles",
                "duration": "2 years",
                "outcome": "You are ready to compete in the CAT/XAT exams with a solid profile.",
            },
            {
                "phase": "Intermediate",
                "step_order": 2,
                "title": "Crack CAT and B-School Interviews",
                "description": "Score 95+ percentile in CAT and clear the grueling Group Discussion / Personal Interview (GD/PI) rounds.",
                "skill": "Verbal Ability & Interviewing",
                "resource": "CAT mock tests, PI coaching",
                "duration": "6 months",
                "outcome": "Admission into a top-tier Indian Institute of Management (IIM) or equivalent.",
            },
            {
                "phase": "Advanced",
                "step_order": 3,
                "title": "MBA and Corporate Placements",
                "description": "Specialize in Marketing, Finance, or Operations. Secure a top summer internship leading to a PPO.",
                "skill": "Strategic Management",
                "resource": "Case studies (HBR), corporate internships",
                "duration": "2 years",
                "outcome": "You graduate ready for mid-to-senior management roles with high compensation.",
            },
        ],
        "insights": [
            {
                "quote": "Management is doing things right; leadership is doing the right things.",
                "author": "Peter Drucker",
                "source": "Essential Drucker",
                "context": "MBA programs teach management, but the industry rewards those who show genuine leadership.",
            },
            {
                "quote": "The best way to predict the future is to create it.",
                "author": "Peter Drucker",
                "source": "Business quotes",
                "context": "Business strategy isn't just analyzing data; it's about making bold bets on market direction.",
            },
        ],
    },
]

def seed_database(db: Session) -> None:
    if db.query(Admin).filter(Admin.email == "Shreekrishna@2003").first() is None:
        default_admin = Admin(
            email="Shreekrishna@2003",
            password_hash=pwd_context.hash("Radhakrishna@2003")
        )
        db.add(default_admin)
        db.flush()

    if db.query(CareerPath).count() > 0:
        db.commit()
        return

    for career in CAREER_CATALOG:
        career_path = CareerPath(
            slug=career["slug"],
            title=career["title"],
            summary=career["summary"],
            difficulty_level=career["difficulty_level"],
            time_required=career["time_required"],
            outlook=career["outlook"],
            fit_reason=career["fit_reason"],
            required_subjects=career["required_subjects"],
            keyword_profile=career["keyword_profile"],
        )
        db.add(career_path)
        db.flush()

        for step in career["roadmap"]:
            db.add(
                RoadmapStep(
                    career_path_id=career_path.id,
                    phase=step["phase"],
                    step_order=step["step_order"],
                    title=step["title"],
                    description=step["description"],
                    skill=step["skill"],
                    resource=step["resource"],
                    duration=step["duration"],
                    outcome=step["outcome"],
                )
            )

        for insight in career["insights"]:
            db.add(
                CareerInsight(
                    career_path_id=career_path.id,
                    quote=insight["quote"],
                    author=insight["author"],
                    source=insight["source"],
                    context=insight["context"],
                )
            )

    db.commit()
