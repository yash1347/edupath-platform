import { useState } from "react";
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";

const INITIAL_LOGIN = {
  name: "",
  email: "",
  phone: "",
  state: "",
};

export default function LoginPage({ onLogin }) {
  const [form, setForm] = useState(INITIAL_LOGIN);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleGoogleSuccess = (credentialResponse) => {
    try {
      const decoded = jwtDecode(credentialResponse.credential);
      setForm((current) => ({
        ...current,
        name: decoded.name || "",
        email: decoded.email || "",
      }));
      setError("");
    } catch (err) {
      setError("Failed to decode Google profile. Please fill details manually.");
    }
  };

  const handleGoogleError = () => {
    setError("Google sign-in failed or was cancelled.");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!form.name || !form.email || !form.phone || !form.state) {
      setError("Please fill in all fields before continuing.");
      return;
    }

    setError("");
    onLogin(form);
  };

  return (
    <main className="page-shell">
      <section className="panel auth-panel">
        <div className="panel-header">
          <p className="eyebrow">Welcome to EDUPATH</p>
          <h2>Sign in and build a personalised roadmap for your next stage.</h2>
          <p className="muted">
            Use your Google email, phone number, and state. After login, select your current level and answer interest questions to receive a tailored roadmap.
          </p>
        </div>

        <div className="auth-actions" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={handleGoogleError}
            useOneTap
            shape="pill"
            theme="filled_black"
          />
          <span className="muted">Or fill in your details below to continue.</span>
        </div>

        <form className="form-shell" onSubmit={handleSubmit}>
          <div className="form-grid">
            <label className="field">
              <span>Name</span>
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="Aarav Sharma"
                required
              />
            </label>

            <label className="field">
              <span>Email</span>
              <input
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="student@gmail.com"
                required
              />
            </label>

            <label className="field">
              <span>Phone</span>
              <input
                name="phone"
                type="tel"
                value={form.phone}
                onChange={handleChange}
                placeholder="9876543210"
                required
              />
            </label>

            <label className="field">
              <span>State</span>
              <input
                name="state"
                value={form.state}
                onChange={handleChange}
                placeholder="Maharashtra"
                required
              />
            </label>
          </div>

          <div className="form-footer">
            {error ? (
              <p className="inline-error">{error}</p>
            ) : (
              <span className="muted">Your information helps personalise the next page.</span>
            )}
            <button className="primary-button" type="submit">
              Continue to profile questions
            </button>
          </div>
        </form>
      </section>
    </main>
  );
}
