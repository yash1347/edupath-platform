import React, { useState, useEffect } from 'react';
import { ShieldAlert, Users, TrendingUp } from 'lucide-react';
import { adminLogin, fetchAdminUsers } from '../api';

export default function AdminPanel() {
  const [token, setToken] = useState(localStorage.getItem('adminToken') || null);
  const [email, setEmail] = useState('admin@edupath.com');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (token) {
      loadUsers();
    }
  }, [token]);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await fetchAdminUsers(token);
      setUsers(data);
    } catch (e) {
      if (e.response?.status === 401) {
        handleLogout();
      } else {
        setError('Failed to load users');
      }
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
          <p className="muted">Manage and monitor student success rates across the platform.</p>
        </div>
        <button onClick={handleLogout} className="ghost-button">Sign Out</button>
      </div>

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
              <th>Student Name</th>
              <th>Education</th>
              <th>Recommended Path</th>
              <th>Progress</th>
              <th>Success Likelihood</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="6" style={{ textAlign: 'center', padding: '32px' }}>Loading...</td></tr>
            ) : users.length === 0 ? (
              <tr><td colSpan="6" style={{ textAlign: 'center', padding: '32px' }}>No students recorded yet.</td></tr>
            ) : (
              users.map(u => (
                <tr key={u.id}>
                  <td style={{ color: 'var(--muted)', fontWeight: 600 }}>#{u.id}</td>
                  <td style={{ fontWeight: 600 }}>
                    <div>{u.name}</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--muted)', fontWeight: 400 }}>{u.email}</div>
                  </td>
                  <td>{u.education_level}</td>
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
    </div>
  );
}
