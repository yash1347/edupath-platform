import { useEffect, useState } from "react";

import Chart from "../components/Chart";
import Form from "../components/Form";
import FutureReady from "../components/FutureReady";
import LoginPage from "../components/LoginPage";
import Planner from "../components/Planner";
import ProgressPanel from "../components/ProgressPanel";
import Result from "../components/Result";
import Roadmap from "../components/Roadmap";
import {
  analyzeStudent,
  fetchBootstrap,
  refreshStudyPlan,
  saveSubjectProgress,
  toggleRoadmapStep,
} from "../api";

function Hero({ analysis }) {
  const recommendedCareerTitle = analysis?.recommended_career?.title || "Waiting for analysis";
  const confidenceLabel = analysis?.confidence_score != null ? `${analysis.confidence_score}%` : "--";
  const completedSteps = analysis?.completion_summary?.completed_steps ?? 0;
  const totalSteps = analysis?.completion_summary?.total_steps ?? 0;

  return (
    <section className="hero">
      <div className="hero-copy">
        <p className="eyebrow">EDUPATH</p>
        <h1>Career clarity for students who are unsure what comes next.</h1>
        <p className="hero-text">
          Analyze marks, interest, skills, and progress to generate a realistic career direction, roadmap,
          and adaptive study planner.
        </p>
      </div>

      <div className="hero-stats">
        <article className="stat-card">
          <span>Career Match</span>
          <strong>{recommendedCareerTitle}</strong>
        </article>
        <article className="stat-card">
          <span>Confidence</span>
          <strong>{confidenceLabel}</strong>
        </article>
        <article className="stat-card">
          <span>Roadmap</span>
          <strong>
            {analysis ? `${completedSteps}/${totalSteps} done` : "No roadmap yet"}
          </strong>
        </article>
      </div>
    </section>
  );
}

export default function Home() {
  const [bootstrap, setBootstrap] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [userSession, setUserSession] = useState(null);
  const [profile, setProfile] = useState({ name: "", email: "", phone: "", state: "" });
  const [loading, setLoading] = useState(false);
  const [plannerLoading, setPlannerLoading] = useState(false);
  const [busyStepId, setBusyStepId] = useState(null);
  const [savingSubject, setSavingSubject] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    Promise.resolve(typeof fetchBootstrap === "function" ? fetchBootstrap() : null)
      .then(setBootstrap)
      .catch(() => {
        setError("Backend bootstrap data could not be loaded. Start the API server and try again.");
      });
  }, []);

  const handleLogin = (account) => {
    setUserSession(account);
    setProfile(account);
    setError("");
    setNotice("Welcome back! Complete the next form to generate your roadmap.");
  };

  const handleAnalyze = async (payload) => {
    setLoading(true);
    setError("");
    setNotice("");

    try {
      const response = await analyzeStudent(payload);
      setAnalysis(response);
      localStorage.setItem("studentUserId", response.user_id);
      setNotice("Live analysis created and persisted successfully.");
    } catch (requestError) {
      const detail = requestError?.response?.data?.detail;
      const errorMessage = Array.isArray(detail)
        ? detail.map((err) => `${err.loc?.slice(-1)}: ${err.msg}`).join(", ")
        : detail || "Analysis failed. Please verify the backend and database setup.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStep = async (stepId) => {
    if (!analysis) return;

    setBusyStepId(stepId);
    setError("");
    try {
      await toggleRoadmapStep(stepId, analysis.user_id);
      const refreshed = await refreshStudyPlan(analysis.user_id);
      setAnalysis(refreshed);
      setNotice("Roadmap progress updated and study plan refreshed.");
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to update roadmap progress.");
    } finally {
      setBusyStepId(null);
    }
  };

  const handleSaveSubjectProgress = async (subjectName, completionPercentage) => {
    if (!analysis) return;

    setSavingSubject(subjectName);
    setError("");
    try {
      await saveSubjectProgress({
        user_id: analysis.user_id,
        subject_name: subjectName,
        completion_percentage: completionPercentage,
      });
      setAnalysis((current) => ({
        ...current,
        subject_progress: {
          ...current.subject_progress,
          [subjectName]: completionPercentage,
        },
      }));
      setNotice(`Saved ${subjectName} progress at ${completionPercentage}%.`);
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to save subject progress.");
    } finally {
      setSavingSubject("");
    }
  };

  const handleRefreshPlan = async () => {
    if (!analysis) return;

    setPlannerLoading(true);
    setError("");
    try {
      const refreshed = await refreshStudyPlan(analysis.user_id);
      setAnalysis(refreshed);
      setNotice("Adaptive study plan refreshed using your latest progress.");
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to refresh the study plan.");
    } finally {
      setPlannerLoading(false);
    }
  };

  if (!userSession) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <main className="page-shell">
      <Hero analysis={analysis} />

      {error ? <div className="message-banner error-banner">{error}</div> : null}
      {notice ? <div className="message-banner success-banner">{notice}</div> : null}

      <section className="panel">
        <div className="panel-header">
          <p className="eyebrow">Welcome back</p>
          <h2>{`Hello, ${userSession.name}!`}</h2>
          <p className="muted">
            Choose your current education stage and answer questions about your interests, dream career, and recent marks.
          </p>
        </div>
      </section>

      <Form
        onSubmit={handleAnalyze}
        loading={loading}
        educationLevels={bootstrap?.education_levels || []}
        initialData={profile}
      />

      {analysis ? (
        <>
          <Chart data={analysis} />
          <Result data={analysis} />
          <Roadmap
            roadmap={analysis.roadmap}
            summary={analysis.completion_summary}
            onToggleStep={handleToggleStep}
            busyStepId={busyStepId}
          />
          <ProgressPanel
            progress={analysis.subject_progress}
            onSave={handleSaveSubjectProgress}
            savingSubject={savingSubject}
          />
          <Planner
            studyPlan={analysis.study_plan}
            onRefresh={handleRefreshPlan}
            loading={plannerLoading}
          />
          <FutureReady items={analysis.future_ready_features} />
        </>
      ) : null}
    </main>
  );
}
