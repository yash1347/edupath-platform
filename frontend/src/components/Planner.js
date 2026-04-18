function groupEntries(entries) {
  return entries.reduce((accumulator, entry) => {
    if (!accumulator[entry.day_name]) {
      accumulator[entry.day_name] = [];
    }
    accumulator[entry.day_name].push(entry);
    return accumulator;
  }, {});
}

export default function Planner({ studyPlan, onRefresh, loading }) {
  if (!studyPlan) return null;

  const grouped = groupEntries(studyPlan.entries);

  return (
    <section className="panel">
      <div className="panel-header planner-header">
        <div>
          <p className="eyebrow">Smart Study Planner</p>
          <h2>{studyPlan.title}</h2>
          <p className="muted">{studyPlan.adaptive_summary}</p>
        </div>

        <div className="planner-actions">
          <div className="stat-chip">
            <span>Weekly hours</span>
            <strong>{studyPlan.weekly_hours}</strong>
          </div>
          <button className="primary-button" type="button" onClick={onRefresh} disabled={loading}>
            {loading ? "Refreshing..." : "Refresh Adaptive Plan"}
          </button>
        </div>
      </div>

      <div className="planner-grid">
        {Object.entries(grouped).map(([dayName, entries]) => (
          <article className="planner-day" key={dayName}>
            <h3>{dayName}</h3>
            <div className="stack-list">
              {entries.map((entry, index) => (
                <div className={`planner-session ${entry.is_break ? "break-session" : ""}`} key={`${dayName}-${index}`}>
                  <div className="stack-row">
                    <strong>{entry.subject_name}</strong>
                    <span>{entry.duration_hours}h</span>
                  </div>
                  <p>{entry.session_type}</p>
                  <small>{entry.objective}</small>
                </div>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
