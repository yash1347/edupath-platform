import React, { useEffect, useState } from 'react';
import { fetchOpportunities, fetchGovtJobs } from '../api';
import { Compass, Clock, BookOpen, Target, CheckCircle2 } from 'lucide-react';

export default function Opportunities() {
  const [careers, setCareers] = useState([]);
  const [govtJobs, setGovtJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchOpportunities(), fetchGovtJobs()])
      .then(([careersRes, jobsRes]) => {
        setCareers(careersRes);
        setGovtJobs(jobsRes);
        setLoading(false);
      })
      .catch((e) => {
        console.error(e);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="page-shell">
        <h1 style={{ fontSize: '2.5rem', marginBottom: '8px' }}>Explorer</h1>
        <p className="muted">Loading global opportunities...</p>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '2.8rem', margin: '0 0 12px 0' }}>Opportunities Explorer</h1>
        <p className="muted" style={{ fontSize: '1.1rem', maxWidth: '600px' }}>
          Discover the wide world of careers stored in our database. See requirements, outlooks, time commitments, and estimated starting salary for each path.
        </p>
      </header>

      <div className="charts-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))' }}>
        {careers.map((career) => (
          <div key={career.slug} className="panel" style={{ display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ fontSize: '1.4rem', margin: '0 0 8px 0', color: 'var(--primary-deep)' }}>{career.title}</h3>
            <p className="muted" style={{ margin: '0 0 20px 0', lineHeight: 1.5 }}>{career.summary}</p>

            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '16px' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.95rem' }}>
                <CheckCircle2 size={16} /> Salary: {career.estimated_salary}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.95rem' }}>
                <Clock size={16} /> Timeline: {career.time_required}
              </span>
            </div>

            <div className="step-meta" style={{ marginBottom: '20px' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Target size={16} /> Difficulty: {career.difficulty_level}
              </span>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '8px', color: 'var(--muted)' }}>Required Subjects</div>
              <div className="tag-row">
                {career.required_subjects.map((sub, i) => (
                  <span key={i} className="tag">{sub}</span>
                ))}
              </div>
            </div>

            <div style={{ padding: '16px', background: 'rgba(23, 96, 135, 0.05)', borderRadius: '16px', marginTop: 'auto' }}>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start' }}>
                <Compass size={20} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <p style={{ margin: 0, fontSize: '0.95rem', lineHeight: 1.5, color: 'var(--text)' }}>
                  {career.outlook}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <section style={{ marginTop: '40px' }}>
        <header style={{ marginBottom: '24px' }}>
          <h2 style={{ fontSize: '2.2rem', margin: '0 0 10px 0' }}>Government Exam & Job Paths</h2>
          <p className="muted" style={{ fontSize: '1.05rem', maxWidth: '640px' }}>
            Review entry qualifications, exam bodies, selection steps, syllabus guidance, and estimated starting salary for government recruitment opportunities.
          </p>
        </header>

        <div className="charts-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))' }}>
          {govtJobs.map((job) => (
            <div key={job.id} className="panel" style={{ display: 'flex', flexDirection: 'column' }}>
              <h3 style={{ fontSize: '1.3rem', margin: '0 0 8px 0', color: 'var(--primary-deep)' }}>{job.title}</h3>
              <p className="muted" style={{ margin: '0 0 14px 0', lineHeight: 1.5 }}>{job.qualification} • {job.exam_body}</p>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.95rem' }}>
                  <BookOpen size={16} /> Qualification: {job.qualification}
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.95rem' }}>
                  <CheckCircle2 size={16} /> Salary: {job.estimated_salary}
                </span>
              </div>

              <div style={{ marginBottom: '16px' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '8px', color: 'var(--muted)' }}>Selection Process</div>
                <ul style={{ margin: 0, paddingLeft: '18px', color: 'var(--text)', lineHeight: 1.6 }}>
                  {job.selection_process.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ul>
              </div>

              <div style={{ padding: '16px', background: 'rgba(23, 96, 135, 0.05)', borderRadius: '16px' }}>
                <p style={{ margin: 0, fontSize: '0.95rem', lineHeight: 1.6, color: 'var(--text)' }}>
                  {job.syllabus_summary}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
