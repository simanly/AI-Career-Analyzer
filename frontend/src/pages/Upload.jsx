import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeCv } from "../api/analyzeCv";
import ErrorBox from "../components/ErrorBox";

const MAX_SIZE = 5 * 1024 * 1024; // 5 MB
const ALLOWED_EXT = ["pdf", "docx"];

function validate(file) {
  const ext = file.name.split(".").pop().toLowerCase();
  if (!ALLOWED_EXT.includes(ext)) return { code: "UNSUPPORTED_FILE_TYPE" };
  if (file.size > MAX_SIZE) return { code: "FILE_TOO_LARGE" };
  return null;
}

export default function Upload({ onResult }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);
  const navigate = useNavigate();

  const pickFile = (f) => {
    if (!f) return;
    const problem = validate(f);
    if (problem) {
      setFile(null);
      setError(problem);
      return;
    }
    setError(null);
    setFile(f);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    pickFile(e.dataTransfer.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeCv(file);
      onResult(result);
      navigate("/results");
    } catch (err) {
      setError({ code: err.code, message: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h2>CV-ni yüklə</h2>

      <div
        className={`dropzone ${dragging ? "dragging" : ""}`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          hidden
          onChange={(e) => pickFile(e.target.files[0])}
        />
        {file ? (
          <p><strong>{file.name}</strong> ({(file.size / 1024 / 1024).toFixed(2)} MB)</p>
        ) : (
          <p>Faylı bura sürüklə və ya seçmək üçün kliklə<br /><small>PDF və ya DOCX, maksimum 5 MB</small></p>
        )}
      </div>

      <ErrorBox code={error?.code} message={error?.message} />

      <button className="btn" onClick={handleAnalyze} disabled={!file || loading}>
        {loading ? "Analiz edilir..." : "Analyze"}
      </button>
    </div>
  );
}