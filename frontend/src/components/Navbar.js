import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Briefcase, MessageSquare, Shield, Home } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();

  const links = [
    { name: 'Dashboard', path: '/', icon: <Home size={18} /> },
    { name: 'Opportunities', path: '/opportunities', icon: <Briefcase size={18} /> },
    { name: 'AI Chat', path: '/chat', icon: <MessageSquare size={18} /> },
    { name: 'Admin', path: '/admin', icon: <Shield size={18} /> },
  ];

  return (
    <nav className="nav-shell">
      <div className="nav-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary-deep)', letterSpacing: '-0.02em' }}>EduPath AI</span>
          <span className="eyebrow" style={{ margin: 0, padding: '4px 8px', fontSize: '0.65rem' }}>BETA</span>
        </div>
        <div className="nav-links">
          {links.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              className={`nav-link ${location.pathname === link.path ? 'active' : ''}`}
            >
              {link.icon}
              {link.name}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
