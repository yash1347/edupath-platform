export default function Roadmap({ roadmap, summary, onToggleStep, busyStepId }) {
  if (!roadmap?.length) return null;

  return (
    <section className="panel">
      <div className="panel-header">
        <p className="eyebrow">Career Roadmap</p>
        <h2>Phase-based path from beginner to advanced</h2>
        <p className="muted">
          {summary.completed_steps} of {summary.total_steps} roadmap steps completed.
        </p>
      </div>

      <div className="roadmap-grid">
        {roadmap.map((phase) => (
          <article className="roadmap-phase" key={phase.phase}>
            <div className="phase-head">
              <span className="phase-pill">{phase.phase}</span>
            </div>

            {phase.steps.map((step) => (
              <div className={`roadmap-step ${step.completed ? "is-complete" : ""}`} key={step.id}>
                <p className="step-number">Step {step.step_order}</p>
                <h3>{step.title}</h3>
                <p>{step.description}</p>
                <div className="step-meta">
                  <span><strong>Skill:</strong> {step.skill}</span>
                  <span><strong>Resource:</strong> {step.resource}</span>
                  <span><strong>Duration:</strong> {step.duration}</span>
                  <span><strong>Outcome:</strong> {step.outcome}</span>
                </div>
                <button
                  className={`ghost-button ${step.completed ? "success" : ""}`}
                  type="button"
                  onClick={() => onToggleStep(step.id)}
                  disabled={busyStepId === step.id}
                >
                  {busyStepId === step.id
                    ? "Saving..."
                    : step.completed
                      ? "Completed"
                      : "Mark Complete"}
                </button>
              </div>
            ))}
          </article>
        ))}
      </div>
    </section>
  );
}
