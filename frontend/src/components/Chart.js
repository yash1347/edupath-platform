import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const BAND_COLORS = {
  Strong: "#0c8b6b",
  Average: "#d7a034",
  Weak: "#d65d42",
};

export default function Chart({ data }) {
  if (!data) return null;

  const marksBreakdown = Array.isArray(data.marks_breakdown) ? data.marks_breakdown : [];
  const strongSubjects = Array.isArray(data.strong_subjects) ? data.strong_subjects : [];
  const weakSubjects = Array.isArray(data.weak_subjects) ? data.weak_subjects : [];
  const confidenceScore = Number.isFinite(data.confidence_score) ? data.confidence_score : 0;

  const strengthData = marksBreakdown.map((item) => ({
    subject: item.subject,
    marks: item.marks,
    fill: BAND_COLORS[item.band] || "#264653",
  }));

  const distribution = [
    { name: "Strong", value: strongSubjects.length, fill: BAND_COLORS.Strong },
    { name: "Weak", value: weakSubjects.length, fill: BAND_COLORS.Weak },
    {
      name: "Average",
      value: Math.max(0, marksBreakdown.length - strongSubjects.length - weakSubjects.length),
      fill: BAND_COLORS.Average,
    },
  ];

  return (
    <section className="panel charts-panel">
      <div className="panel-header">
        <p className="eyebrow">Data Visualization</p>
        <h2>See your academic signals at a glance</h2>
      </div>

      <div className="charts-grid">
        <article className="chart-card">
          <h3>Strong vs weak subjects</h3>
          <div className="chart-shell">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={strengthData}>
                <CartesianGrid strokeDasharray="4 4" stroke="rgba(27, 44, 55, 0.1)" />
                <XAxis dataKey="subject" stroke="#49606d" />
                <YAxis domain={[0, 100]} stroke="#49606d" />
                <Tooltip />
                <Bar dataKey="marks" radius={[12, 12, 0, 0]}>
                  {strengthData.map((entry) => (
                    <Cell key={entry.subject} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="chart-card">
          <h3>Confidence level</h3>
          <div className="chart-shell">
            <ResponsiveContainer width="100%" height={280}>
              <RadialBarChart
                cx="50%"
                cy="50%"
                innerRadius="55%"
                outerRadius="95%"
                barSize={20}
                data={[{ value: confidenceScore, fill: "#176087" }]}
                startAngle={90}
                endAngle={-270}
              >
                <RadialBar minAngle={15} dataKey="value" cornerRadius={16} background />
                <text x="50%" y="48%" textAnchor="middle" className="chart-center-value">
                  {confidenceScore}%
                </text>
                <text x="50%" y="58%" textAnchor="middle" className="chart-center-label">
                  certainty
                </text>
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="chart-card">
          <h3>Performance distribution</h3>
          <div className="chart-shell">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={distribution} dataKey="value" nameKey="name" innerRadius={70} outerRadius={100}>
                  {distribution.map((entry) => (
                    <Cell key={entry.name} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </article>
      </div>
    </section>
  );
}
