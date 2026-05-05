import { useEffect, useMemo, useState } from "react";

const INITIAL_FORM = {
  name: "",
  email: "",
  phone: "",
  state: "",
  education_level: "",
  stream: "",
  dream: "",
  career_choice: "",
  interests: "",
  skills: "",
  maths: "",
  physics: "",
  chemistry: "",
  biology: "",
};

const INTEREST_OPTIONS = [
  "Coding and Software",
  "Science and Research",
  "Healthcare and Medicine",
  "Business and Management",
  "Design and Creativity",
  "Finance and Accounting",
  "Law and Humanities",
  "Engineering and Mechanics",
  "Marketing and Content",
  "Data and Analytics"
];

const SKILL_OPTIONS = [
  "Problem Solving",
  "Communication",
  "Logical Reasoning",
  "Leadership",
  "Analytical Thinking",
  "Creativity",
  "Technical Troubleshooting",
  "Public Speaking",
  "Research and Writing",
  "Project Management"
];

const STREAM_OPTIONS = ["PCM", "PCB", "PCMB", "Commerce", "Arts"];

const EDUCATION_LEVEL_MAP = {
  "After 10th": "10th",
  "After 12th": "12th",
  UG: "Graduation",
  PG: "Postgraduate",
};

const SUBJECT_LABELS = {
  "10th": [
    { key: "maths", label: "Maths / Numeracy" },
    { key: "physics", label: "Science / Physics" },
    { key: "chemistry", label: "English / Language" },
    { key: "biology", label: "Social Science / General" },
  ],
  "12th": [
    { key: "maths", label: "Maths" },
    { key: "physics", label: "Physics" },
    { key: "chemistry", label: "Chemistry" },
    { key: "biology", label: "Biology" },
  ],
  Graduation: [
    { key: "maths", label: "Core Subject 1" },
    { key: "physics", label: "Core Subject 2" },
    { key: "chemistry", label: "Elective or Lab" },
    { key: "biology", label: "General or Optional" },
  ],
  Postgraduate: [
    { key: "maths", label: "Major Subject" },
    { key: "physics", label: "Specialization" },
    { key: "chemistry", label: "Research / Project" },
    { key: "biology", label: "Presentation / Soft skills" },
  ],
};

const DEFAULT_SUBJECTS = SUBJECT_LABELS["12th"];

function normalizeEducationLevel(level) {
  return EDUCATION_LEVEL_MAP[level] || level;
}

export default function Form({ onSubmit, loading, educationLevels = [], initialData = {} }) {
  const [form, setForm] = useState(() => ({ ...INITIAL_FORM, ...initialData }));
  const [error, setError] = useState("");

  useEffect(() => {
    setForm({ ...INITIAL_FORM, ...initialData });
  }, [initialData]);

  const educationOptions = useMemo(
    () =>
      (educationLevels.length ? educationLevels : ["10th", "12th", "Graduation", "Postgraduate"]).map(
        normalizeEducationLevel
      ),
    [educationLevels]
  );

  const normalizedEducationLevel = normalizeEducationLevel(form.education_level);
  let currentSubjectFields = SUBJECT_LABELS[normalizedEducationLevel] || DEFAULT_SUBJECTS;

  if (normalizedEducationLevel === "12th" && form.stream) {
    if (form.stream === "PCM") {
      currentSubjectFields = currentSubjectFields.filter((f) => f.key !== "biology");
    } else if (form.stream === "PCB") {
      currentSubjectFields = currentSubjectFields.filter((f) => f.key !== "maths");
    } else if (form.stream === "Commerce" || form.stream === "Arts") {
      currentSubjectFields = []; // Hide all science subjects for Commerce/Arts
    }
  }

  const stagePrompt = {
    "10th": "What subjects interest you most today? What is your dream career?",
    "12th": "Which stream are you choosing? What are your strongest subjects?",
    Graduation: "What do you want to specialise in? What is your long-term goal?",
    Postgraduate: "What are your postgraduate ambitions and preferred research or job path?",
  }[normalizedEducationLevel] || "Tell us about your interests, marks, and dream career.";

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const activeSubjects = currentSubjectFields.map((f) => f.key);
    const activeScores = activeSubjects.map((subject) => Number(form[subject]));

    if (activeScores.some((score) => Number.isNaN(score) || score < 0 || score > 100)) {
      setError("Marks should be between 0 and 100.");
      return;
    }

    if (!form.education_level) {
      setError("Please choose your current education stage.");
      return;
    }

    setError("");
    onSubmit({
      ...form,
      education_level: normalizedEducationLevel,
      maths: activeSubjects.includes("maths") ? (Number(form.maths) || 0) : 0,
      physics: activeSubjects.includes("physics") ? (Number(form.physics) || 0) : 0,
      chemistry: activeSubjects.includes("chemistry") ? (Number(form.chemistry) || 0) : 0,
      biology: activeSubjects.includes("biology") ? (Number(form.biology) || 0) : 0,
    });
  };

  return (
    <section className="panel form-panel">
      <div className="panel-header">
        <p className="eyebrow">Student Intake</p>
        <h2>Answer a few questions and get a personalised roadmap.</h2>
        <p className="muted">EDUPATH will use your stage, marks, interests, and dreams to recommend your strongest path.</p>
      </div>

      <form className="form-shell" onSubmit={handleSubmit}>
        <div className="form-grid">
          <label className="field">
            <span>Name</span>
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Aarav Sharma"
              required
            />
          </label>

          <label className="field">
            <span>Email</span>
            <input
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              placeholder="student@example.com"
              required
            />
          </label>

          <label className="field">
            <span>Phone</span>
            <input
              name="phone"
              type="tel"
              value={form.phone}
              onChange={handleChange}
              placeholder="9876543210"
              required
            />
          </label>

          <label className="field">
            <span>State</span>
            <input
              name="state"
              value={form.state}
              onChange={handleChange}
              placeholder="Maharashtra"
              required
            />
          </label>

          <label className="field field-wide">
            <span>Education level</span>
            <select
              name="education_level"
              value={form.education_level}
              onChange={handleChange}
              required
            >
              <option value="">Select your stage</option>
              {educationOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          {normalizedEducationLevel === "12th" && (
            <label className="field field-wide">
              <span>Stream</span>
              <select
                name="stream"
                value={form.stream}
                onChange={handleChange}
                required
              >
                <option value="">Select your stream</option>
                {STREAM_OPTIONS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>
          )}

          <label className="field field-wide">
            <span>Why this stage?</span>
            <textarea
              name="career_choice"
              rows="3"
              value={form.career_choice}
              onChange={handleChange}
              placeholder="Why did you choose 10th / 12th / UG / PG?"
              required
            />
          </label>

          <label className="field field-wide">
            <span>Dream career</span>
            <textarea
              name="dream"
              rows="3"
              value={form.dream}
              onChange={handleChange}
              placeholder="What is your dream job or field?"
              required
            />
          </label>

          {currentSubjectFields.map((subject) => (
            <label className="field" key={subject.key}>
              <span>{subject.label}</span>
              <input
                min="0"
                max="100"
                name={subject.key}
                type="number"
                value={form[subject.key]}
                onChange={handleChange}
                placeholder="0-100"
                required
              />
            </label>
          ))}

          <label className="field field-wide">
            <span>What are you interested in?</span>
            <select
              name="interests"
              value={form.interests}
              onChange={handleChange}
              required
            >
              <option value="">Select your primary interest</option>
              {INTEREST_OPTIONS.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </label>

          <label className="field field-wide">
            <span>What are your strong skills?</span>
            <select
              name="skills"
              value={form.skills}
              onChange={handleChange}
              required
            >
              <option value="">Select your primary skill</option>
              {SKILL_OPTIONS.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </label>

          <div className="field field-wide">
            <span>Stage prompt</span>
            <p className="muted">{stagePrompt}</p>
          </div>
        </div>

        <div className="form-footer">
          {error ? (
            <p className="inline-error">{error}</p>
          ) : (
            <span className="muted">This input helps us identify strong and weak subjects and build a better roadmap.</span>
          )}
          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Analyzing Profile..." : "Generate Career Roadmap"}
          </button>
        </div>
      </form>
    </section>
  );
}
