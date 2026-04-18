function BadgeList({ title, items = [], tone = "default" }) {
  return (
    <div className="subpanel">
      <h3>{title}</h3>
      <div className="tag-row">
        {items.length ? (
          items.map((item) => (
            <span className={`tag ${tone}`} key={item}>
              {item}
            </span>
          ))
        ) : (
          <span className="tag muted-tag">None recorded</span>
        )}
      </div>
    </div>
  );
}

export default function Result({ data }) {
  if (!data) return null;

  const recommendedCareer = data.recommended_career || {};
  const requiredSubjects = Array.isArray(recommendedCareer.required_subjects)
    ? recommendedCareer.required_subjects
    : [];
  const careerMatches = Array.isArray(data.career_matches) ? data.career_matches : [];
  const insights = Array.isArray(data.insights) ? data.insights : [];

  return (
    <section className="panel result-panel">
      <div className="result-hero">
        <div className="hero-copy-block">
          <p className="eyebrow">Recommended Career</p>
          <h2>{recommendedCareer.title}</h2>
          <p className="lead-text">{recommendedCareer.summary}</p>
          <p className="muted">{data.message}</p>
        </div>

        <div className="confidence-card">
          <span>Confidence</span>
          <strong>{data.confidence_score}%</strong>
          <small>{recommendedCareer.difficulty_level} difficulty</small>
        </div>
      </div>

      <div className="result-grid">
        <div className="subpanel">
          <h3>Reality check</h3>
          <p><strong>Time required:</strong> {recommendedCareer.time_required}</p>
          <p><strong>Difficulty:</strong> {recommendedCareer.difficulty_level}</p>
          <p className="muted">{recommendedCareer.outlook}</p>
        </div>

        <div className="subpanel">
          <h3>Why this path fits</h3>
          <p>{recommendedCareer.fit_reason}</p>
          <div className="tag-row top-gap">
            {requiredSubjects.map((subject) => (
              <span className="tag" key={subject}>
                {subject}
              </span>
            ))}
          </div>
        </div>

        <BadgeList title="Strong subjects" items={data.strong_subjects} tone="good" />
        <BadgeList title="Weak subjects" items={data.weak_subjects} tone="warning" />
      </div>

      <div className="split-grid">
        <article className="subpanel">
          <h3>Top career matches</h3>
          <div className="stack-list">
            {careerMatches.map((match) => (
              <div className="stack-item" key={match.career_slug}>
                <div className="stack-row">
                  <strong>{match.title}</strong>
                  <span>{match.score}</span>
                </div>
                <p className="muted">{match.rationale}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="subpanel">
          <h3>Career insights</h3>
          <div className="stack-list">
            {insights.map((insight) => (
              <blockquote className="quote-card" key={`${insight.author}-${insight.quote}`}>
                <p>"{insight.quote}"</p>
                <footer>
                  {insight.author} | {insight.source}
                </footer>
                <small>{insight.context}</small>
              </blockquote>
            ))}
          </div>
        </article>
      </div>
    </section>
  );
}
