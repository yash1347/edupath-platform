import { useEffect, useState } from "react";

const SUBJECTS = ["Maths", "Physics", "Chemistry", "Biology"];

export default function ProgressPanel({ progress = {}, onSave, savingSubject }) {
  const [drafts, setDrafts] = useState({});

  useEffect(() => {
    setDrafts(progress);
  }, [progress]);

  return (
    <section className="panel">
      <div className="panel-header">
        <p className="eyebrow">Progress Tracking</p>
        <h2>Record subject-wise momentum</h2>
        <p className="muted">
          Updating progress helps EduPath rebalance your weekly plan toward weak or unfinished areas.
        </p>
      </div>

      <div className="progress-grid">
        {SUBJECTS.map((subject) => {
          const value = drafts[subject] || 0;
          return (
            <article className="subpanel" key={subject}>
              <div className="stack-row">
                <h3>{subject}</h3>
                <span>{value}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={value}
                onChange={(event) =>
                  setDrafts((current) => ({
                    ...current,
                    [subject]: Number(event.target.value),
                  }))
                }
                disabled={savingSubject === subject}
              />
              <div className="stack-row">
                <p className="muted">
                  {savingSubject === subject ? "Saving progress..." : "Adjust and save your current mastery."}
                </p>
                <button
                  className="ghost-button"
                  type="button"
                  onClick={() => onSave(subject, value)}
                  disabled={savingSubject === subject}
                >
                  Save
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
