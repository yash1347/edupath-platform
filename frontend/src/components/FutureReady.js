export default function FutureReady({ items = [] }) {
  if (!items.length) return null;

  return (
    <section className="panel">
      <div className="panel-header">
        <p className="eyebrow">Future Ready</p>
        <h2>What EduPath AI can expand into next</h2>
      </div>

      <div className="future-grid">
        {items.map((item) => (
          <article className="future-card" key={item}>
            <h3>{item}</h3>
            <p className="muted">
              Planned as product extensions so the platform grows from roadmap generation into ongoing guidance.
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
