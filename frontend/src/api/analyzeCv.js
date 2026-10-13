import { mockResult } from "../mock/mockResult";

const API_URL = import.meta.env.VITE_API_URL; // e.g. https://your-backend.onrender.com
const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true" || !API_URL;

function normalize(data) {
  return {
    skills: data?.skills ?? [],
    careers: data?.careers ?? [],
    skill_gap: data?.skill_gap ?? [],
    roadmap: data?.roadmap ?? [],
  };
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

  if (!res.ok) {
    const err = new Error(data?.error || "An unknown error occurred.");
    err.code = data?.code || "UNKNOWN_ERROR";
    throw err;
  }

  return normalize(data);
}