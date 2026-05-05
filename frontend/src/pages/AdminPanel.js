import React, { useState, useEffect } from 'react';
import { ShieldAlert, Users, TrendingUp, Map, Edit2, Save, X } from 'lucide-react';
import { adminLogin, fetchAdminUsers, fetchAdminCareers, updateRoadmapStep } from '../api';

export default function AdminPanel() {
  const [token, setToken] = useState(localStorage.getItem('adminToken') || null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  const [activeTab, setActiveTab] = useState('students');
  const [users, setUsers] = useState([]);
  const [careers, setCareers] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const [editingStep, setEditingStep] = useState(null);
  const [editForm, setEditForm] = useState({});

  useEffect(() => {
    if (token) {
      if (activeTab === 'students') loadUsers();
      if (activeTab === 'roadmaps') loadCareers();
    }
  }, [token, activeTab]);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await fetchAdminUsers(token);
      setUsers(data);
    } catch (e) {
      if (e.response?.status === 401) handleLogout();
      else setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const loadCareers = async () => {
    setLoading(true);
    try {
      const data = await fetchAdminCareers(token);
      setCareers(data);
    } catch (e) {
      if (e.response?.status === 401) handleLogout();
      else setError('Failed to load careers');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await adminLogin({ email, password });
      setToken(res.access_token);
      localStorage.setItem('adminToken', res.access_token);
    } catch (e) {
      setError('Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('adminToken');
    setUsers([]);
    setCareers([]);
  };
  
  const startEditing = (step) => {
    setEditingStep(step.id);
    setEditForm({
      title: step.title,
      description: step.description,
      resource: step.resource,
      duration: step.duration
    });
  };
  
  const saveStep = async (stepId) => {
    try {
      await updateRoadmapStep(token, stepId, editForm);
      setEditingStep(null);
      loadCareers(); // refresh
    } catch (e) {
      alert("Failed to save step");
    }
  };

  if (!token) {
    return (
      <div className="page-shell" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
        <div className="panel" style={{ maxWidth: '400px', width: '100%', padding: '40px' }}>
          <div style={{ textAlign: 'center', marginBottom: '30px' }}>
            <div style={{ display: 'inline-flex', padding: '16px', background: 'rgba(214, 93, 66, 0.1)', borderRadius: '50%', marginBottom: '16px' }}>
              <ShieldAlert size={32} color="var(--warning)" />
            </div>
            <h2 style={{ margin: 0 }}>Admin Portal</h2>
            <p className="muted" style={{ margin: '8px 0 0 0' }}>Restricted access only</p>
          </div>
          
          {error && <div className="message-banner error-banner">{error}</div>}
          
          <form onSubmit={handleLogin} className="form-shell" style={{ gap: '16px' }}>
            <div className="field">
              <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
            </div>
            <div className="field">
              <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
            </div>
            <button type="submit" className="primary-button" disabled={loading} style={{ marginTop: '8px' }}>
              {loading ? 'Authenticating...' : 'Secure Login'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <div className="result-hero" style={{ marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', margin: '0 0 8px 0' }}>Admin Dashboard</h1>
          <p className="muted">Manage and monitor student success rates and roadmap data across the platform.</p>
        </div>
        <button onClick={handleLogout} className="ghost-button">Sign Out</button>
      </div>

      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
        <button 
          className={activeTab === 'students' ? 'primary-button' : 'ghost-button'}
          onClick={() => setActiveTab('students')}
        >
          <Users size={16} style={{ marginRight: '8px' }}/> Students
        </button>
        <button 
          className={activeTab === 'roadmaps' ? 'primary-button' : 'ghost-button'}
          onClick={() => setActiveTab('roadmaps')}
        >
          <Map size={16} style={{ marginRight: '8px' }}/> Manage Roadmaps
        </button>
      </div>

      {activeTab === 'students' && (
        <>
          <div className="hero-stats" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', marginBottom: '32px' }}>
            <div className="stat-card">
              <span><Users size={16} style={{ display: 'inline', marginRight: '8px' }}/> Total Students</span>
              <strong>{users.length}</strong>
            </div>
            <div className="stat-card">
              <span><TrendingUp size={16} style={{ display: 'inline', marginRight: '8px' }}/> Avg Success Rate</span>
              <strong>
                {users.length ? Math.round(users.reduce((acc, u) => acc + (u.success_probability || 0), 0) / users.length) : 0}%
              </strong>
            </div>
          </div>

          <div className="panel" style={{ padding: '0', overflowX: 'auto' }}>
            <table className="admin-table">
              <thead style={{ background: 'rgba(22, 48, 60, 0.03)' }}>
                <tr>
                  <th>ID</th>
                  <th>Student Info</th>
                  <th>Education</th>
                  <th>Interests</th>
                  <th>Recommended Path</th>
                  <th>Progress</th>
                  <th>Success Likelihood</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan="7" style={{ textAlign: 'center', padding: '32px' }}>Loading...</td></tr>
                ) : users.length === 0 ? (
                  <tr><td colSpan="7" style={{ textAlign: 'center', padding: '32px' }}>No students recorded yet.</td></tr>
                ) : (
                  users.map(u => (
                    <tr key={u.id}>
                      <td style={{ color: 'var(--muted)', fontWeight: 600 }}>#{u.id}</td>
                      <td style={{ fontWeight: 600 }}>
                        <div>{u.name}</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--muted)', fontWeight: 400 }}>{u.email}</div>
                        {(u.phone || u.state) && (
                          <div style={{ fontSize: '0.75rem', color: 'var(--muted)', marginTop: '4px' }}>
                            {u.phone} {u.phone && u.state ? '•' : ''} {u.state}
                          </div>
                        )}
                      </td>
                      <td>{u.education_level}</td>
                      <td>
                        <div style={{ fontSize: '0.85rem', color: 'var(--muted)', maxWidth: '150px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={u.interests}>
                          {u.interests || '-'}
                        </div>
                      </td>
                      <td>
                        {u.recommended_path ? (
                          <span className="tag" style={{ fontSize: '0.8rem', padding: '4px 8px' }}>{u.recommended_path}</span>
                        ) : '-'}
                      </td>
                      <td>
                        <div style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>
                          {u.completed_steps} / {u.total_steps} steps
                        </div>
                      </td>
                      <td>
                        {u.success_probability ? (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <div style={{ width: '60px', height: '6px', background: 'var(--line)', borderRadius: '3px', overflow: 'hidden' }}>
                              <div style={{ 
                                height: '100%', 
                                width: `${u.success_probability}%`, 
                                background: u.success_probability > 70 ? 'var(--success)' : u.success_probability > 40 ? 'var(--warning)' : 'var(--muted)' 
                              }} />
                            </div>
                            <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>{Math.round(u.success_probability)}%</span>
                          </div>
                        ) : '-'}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </>
      )}

      {activeTab === 'roadmaps' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {loading ? (
            <p>Loading careers...</p>
          ) : careers.map(career => (
            <div key={career.id} className="panel" style={{ padding: '24px' }}>
              <h3 style={{ margin: '0 0 16px 0' }}>{career.title}</h3>
              {career.roadmap.map(phaseGroup => (
                <div key={phaseGroup.phase} style={{ marginBottom: '24px' }}>
                  <h4 style={{ borderBottom: '1px solid var(--line)', paddingBottom: '8px', marginBottom: '16px' }}>{phaseGroup.phase} Phase</h4>
                  <div style={{ display: 'grid', gap: '16px' }}>
                    {phaseGroup.steps.map(step => (
                      <div key={step.id} style={{ background: 'var(--bg-secondary)', padding: '16px', borderRadius: '8px', border: '1px solid var(--line)' }}>
                        {editingStep === step.id ? (
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            <input 
                              value={editForm.title} 
                              onChange={e => setEditForm({...editForm, title: e.target.value})} 
                              placeholder="Title" 
                              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--line)' }}
                            />
                            <textarea 
                              value={editForm.description} 
                              onChange={e => setEditForm({...editForm, description: e.target.value})} 
                              placeholder="Description" 
                              rows={2}
                              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--line)' }}
                            />
                            <input 
                              value={editForm.resource} 
                              onChange={e => setEditForm({...editForm, resource: e.target.value})} 
                              placeholder="Resource" 
                              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--line)' }}
                            />
                            <input 
                              value={editForm.duration} 
                              onChange={e => setEditForm({...editForm, duration: e.target.value})} 
                              placeholder="Duration" 
                              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--line)' }}
                            />
                            <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                              <button className="primary-button" onClick={() => saveStep(step.id)} style={{ padding: '6px 12px', fontSize: '0.9rem' }}><Save size={14} style={{marginRight:'4px'}}/> Save</button>
                              <button className="ghost-button" onClick={() => setEditingStep(null)} style={{ padding: '6px 12px', fontSize: '0.9rem' }}><X size={14} style={{marginRight:'4px'}}/> Cancel</button>
                            </div>
                          </div>
                        ) : (
                          <>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                              <div>
                                <h5 style={{ margin: '0 0 4px 0', fontSize: '1rem' }}>Step {step.step_order}: {step.title}</h5>
                                <p style={{ margin: '0 0 8px 0', fontSize: '0.9rem', color: 'var(--muted)' }}>{step.description}</p>
                              </div>
                              <button className="ghost-button" onClick={() => startEditing(step)} style={{ padding: '4px 8px' }}>
                                <Edit2 size={16} />
                              </button>
                            </div>
                            <div style={{ display: 'flex', gap: '16px', fontSize: '0.85rem' }}>
                              <span style={{ background: 'rgba(0,0,0,0.05)', padding: '2px 8px', borderRadius: '4px' }}>⏱️ {step.duration}</span>
                              <span style={{ background: 'rgba(0,0,0,0.05)', padding: '2px 8px', borderRadius: '4px' }}>📚 {step.resource}</span>
                            </div>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
