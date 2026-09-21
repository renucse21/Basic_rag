import { useRef, useState } from "react";
import Loading from "./Loading";

export default function FileUpload({ document, onUpload }) {
  const input = useRef(); const [progress, setProgress] = useState(0); const [status, setStatus] = useState("");
  const submit = async (e) => {
    const file = e.target.files?.[0]; if (!file) return;
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) { setStatus("Please select a PDF file."); return; }
    setProgress(1); setStatus("Uploading and indexing...");
    try { await onUpload(file, setProgress); setStatus("Upload complete."); } catch { setStatus("Upload failed."); } finally { setProgress(0); input.current.value = ""; }
  };
  return <section className="upload panel"><div><h2>Upload document</h2><p>PDF files only</p></div><input id="pdf-file" ref={input} type="file" accept=".pdf,application/pdf" onChange={submit} /><label className="button" htmlFor="pdf-file">Choose PDF</label>{progress > 0 && <><Loading /> <progress value={progress} max="100" /></>}{status && <span className="status">{status}</span>}{document && <div className="document"><strong>{document.filename}</strong><span>{document.chunks} chunks indexed</span></div>}</section>;
}
