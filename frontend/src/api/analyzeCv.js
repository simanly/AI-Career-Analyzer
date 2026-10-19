import { mockResult } from "../mock/mockResult";

const API_URL = import.meta.env.VITE_API_URL;
const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true" || !API_URL;

const toArray = (v) => (Array.isArray(v) ? v : []);
const lower = (v, fallback) => String(v ?? fallback).toLowerCase();

function normalizeScore(s) {
  const n = Number(s) || 0;
  return n > 1 ? n / 100 : n;
}

function normalize(data) {
  const skills = toArray(data?.skills).map((s) =>
    typeof s === "string" ? s : s?.name ?? s?.skill ?? ""
  );

  const careers = toArray(data?.careers).map((c) => ({
    id: c.career_id ?? c.id,
    name: c.career_name ?? c.name,
    score: normalizeScore(c.score),
    matched_skills: toArray(c.matched_skills),
    missing_skills: toArray(c.missing_skills),
  }));

  const skill_gap = toArray(data?.skill_gap).map((g) => ({
    id: g.career_id ?? g.id,
    career: g.career_name ?? g.name,
    gap_count: g.gap_count ?? toArray(g.missing_skills).length,
    missing_skills: toArray(g.missing_skills),
    priority: lower(g.priority, "medium"),
  }));

  const roadmap = toArray(data?.roadmap).map((r) => ({
    id: r.career_id ?? r.id,
    career: r.career_name ?? r.name,
    steps: toArray(r.steps),
  }));

  const prediction = toArray(data?.ml_prediction?.top_predictions).map((p) => ({
    category: String(p.category ?? ""),
    probability: normalizeScore(p.probability),
  }));

  // backend-in "text" sahəsi (CV mətni) burada atılır
  return { skills, careers, skill_gap, roadmap, prediction };
}

export async function analyzeCv(file) {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 1500));
    return normalize(mockResult);
  }

  const formData = new FormData();
  formData.append("file", file);

  let res;
  try {
    res = await fetch(`${API_URL}/analyze-cv`, { method: "POST", body: formData });
  } catch {
    const err = new Error("Could not connect to the server.");
    err.code = "NETWORK_ERROR";
    throw err;
  }

  const data = await res.json().catch(() => null);

  // JSON cavabı olmayan 5xx: backend işləmir, başlamaqdadır (Render) və ya proxy qoşula bilmir.
  if (!res.ok && !data) {
    const err = new Error(
      "The analysis server is not responding. Make sure the backend is running " +
        "(cd backend && uvicorn main:app --port 8000), or try again in a minute if it is waking up."
    );
    err.code = "SERVER_UNAVAILABLE";
    throw err;
  }

  if (!res.ok) {
    const detail = typeof data?.detail === "string" ? data.detail : null;
    const err = new Error(data?.error || detail || "The server could not process this file.");
    err.code = data?.code || "UNKNOWN_ERROR";
    throw err;
  }

  return normalize(data);
}