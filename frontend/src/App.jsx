import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Results from "./pages/Results";
import Roadmap from "./pages/Roadmap";
import NotFound from "./pages/NotFound";

const KEY = "analysis_result";

function loadSaved() {
  try {
    return JSON.parse(sessionStorage.getItem(KEY));
  } catch {
    return null;
  }
}

export default function App() {
  const [result, setResult] = useState(loadSaved);

  useEffect(() => {
    try {
      if (result) sessionStorage.setItem(KEY, JSON.stringify(result));
      else sessionStorage.removeItem(KEY);
    } catch {
      /* saxlamaq mümkün olmasa, problem deyil */
    }
  }, [result]);

  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload onResult={setResult} />} />
        <Route path="/results" element={<Results result={result} />} />
        <Route path="/roadmap" element={<Roadmap result={result} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}