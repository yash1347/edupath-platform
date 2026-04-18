import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL?.trim() || "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

export async function fetchBootstrap() {
  const response = await client.get("/api/v1/bootstrap");
  return response.data;
}

export async function analyzeStudent(payload) {
  const response = await client.post("/api/v1/analysis", payload);
  return response.data;
}

export async function toggleRoadmapStep(stepId, userId) {
  const response = await client.post(`/api/v1/roadmap-steps/${stepId}/complete`, {
    user_id: userId,
  });
  return response.data;
}

export async function saveSubjectProgress(payload) {
  const response = await client.post("/api/v1/subject-progress", payload);
  return response.data;
}

export async function refreshStudyPlan(userId) {
  const response = await client.post("/api/v1/study-plan/refresh", {
    user_id: userId,
  });
  return response.data;
}

export async function fetchOpportunities() {
  const response = await client.get("/api/v1/opportunities");
  return response.data;
}

export async function adminLogin(payload) {
  const response = await client.post("/api/v1/admin/login", payload);
  return response.data;
}

export async function fetchAdminUsers(token) {
  const response = await client.get("/api/v1/admin/users", {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
}

export default client;
