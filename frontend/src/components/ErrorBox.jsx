const MESSAGES = {
  FILE_TOO_LARGE: "Fayl çox böyükdür. Maksimum ölçü 5 MB-dır.",
  UNSUPPORTED_FILE_TYPE: "Yalnız PDF və DOCX faylları qəbul olunur.",
  PARSE_FAILED: "Fayldan mətn oxumaq mümkün olmadı.",
  NETWORK_ERROR: "Serverə qoşulmaq mümkün olmadı.",
};

export default function ErrorBox({ code, message }) {
  if (!message && !code) return null;
  return (
    <div className="error-box" role="alert">
      {MESSAGES[code] || message || "Xəta baş verdi."}
    </div>
  );
}