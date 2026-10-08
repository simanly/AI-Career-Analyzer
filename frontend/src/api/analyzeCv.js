import { mockResult } from "../mock/mockResult";

const USE_MOCK = true; // backend hazır olanda false et
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function analyzeCv(file) {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 1500));
    return mockResult;
  }

  const formData = new FormData();
  formData.append("file", file);

  let res;
  try {
    res = await fetch(`${API_URL}/analyze-cv`, { method: "POST", body: formData });
  } catch {
    const err = new Error("Serverə qoşulmaq mümkün olmadı.");
    err.code = "NETWORK_ERROR";
    throw err;
  }

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    const err = new Error(data?.error || "Naməlum xəta baş verdi.");
    err.code = data?.code || "UNKNOWN_ERROR";
    throw err;
  }

  return data;
}