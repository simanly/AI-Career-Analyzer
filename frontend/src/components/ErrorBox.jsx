const MESSAGES = {
  FILE_TOO_LARGE: "The file is too large. Maximum size is 5 MB.",
  UNSUPPORTED_FILE_TYPE: "Only PDF and DOCX files are accepted.",
  PARSE_FAILED: "Could not read text from the file.",
  NETWORK_ERROR: "Could not connect to the server.",
};

export default function ErrorBox({ code, message }) {
  if (!message && !code) return null;
  return (
    <div className="error-box" role="alert">
      {MESSAGES[code] || message || "Something went wrong."}
    </div>
  );
}