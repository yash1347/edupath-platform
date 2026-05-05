import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User as UserIcon } from 'lucide-react';
import client from '../api';

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { id: 1, type: 'bot', text: 'Hello! I am your EDUPATH Mentor. Ask me any questions about learning paths, career outlooks, or study motivation!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  // Pulling studentUserId from local storage if available, defaulting to mock ID 1 for MVP
  const userId = localStorage.getItem('studentUserId') || 1;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { id: Date.now(), type: 'user', text: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      const res = await client.post('/api/v1/chat', {
        user_id: userId,
        message: userMessage
      });
      setMessages(prev => [...prev, { id: Date.now(), type: 'bot', text: res.data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { id: Date.now(), type: 'bot', text: 'Oops! I am having trouble connecting to the network right now.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2.5rem', margin: '0 0 8px 0' }}>AI Career Consultation</h1>
        <p className="muted">Get personalized advice injected with your dashboard history.</p>
      </header>

      <div className="chat-panel">
        <div className="chat-history">
          {messages.map(m => (
            <div key={m.id} className={`chat-message ${m.type}`} style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
              {m.type === 'bot' && <div style={{ background: '#fff', padding: '6px', borderRadius: '50%' }}><Bot size={20} color="var(--primary)" /></div>}
              {m.type === 'user' && <div style={{ background: 'rgba(255,255,255,0.2)', padding: '6px', borderRadius: '50%' }}><UserIcon size={20} color="#fff" /></div>}
              <div style={{ lineHeight: 1.5, marginTop: '4px', whiteSpace: 'pre-wrap' }}>
                {m.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="chat-message bot" style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <div style={{ background: '#fff', padding: '6px', borderRadius: '50%' }}><Bot size={20} color="var(--primary)" /></div>
              <span>Typing...</span>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
        <form className="chat-input-area" onSubmit={handleSend}>
          <input 
            type="text" 
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask about how to schedule your math revision..."
            style={{ flex: 1, padding: '14px', borderRadius: '18px', border: '1px solid var(--line)', background: 'var(--panel-strong)' }}
          />
          <button type="submit" disabled={!input.trim() || loading} className="primary-button" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Send size={18} /> Send
          </button>
        </form>
      </div>
    </div>
  );
}
