import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Results from "./pages/Results";

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload onResult={setResult} />} />
        <Route path="/results" element={<Results result={result} />} />
      </Routes>
    </BrowserRouter>
  );
}