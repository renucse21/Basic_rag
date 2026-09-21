import { useState } from "react";
import axios from "axios";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";
import "./App.css";

export default function App() {
  const [document, setDocument] = useState(null);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");
  const upload = async (file, onProgress) => {
    setError("");
    const body = new FormData(); body.append("file", file);
    try {
      const { data } = await axios.post("/api/upload", body, { onUploadProgress: (e) => onProgress(Math.round((e.loaded * 100) / e.total)) });
      setDocument(data);
    } catch (e) { setError(e.response?.data?.detail || "Upload failed."); throw e; }
  };
  const ask = async (question) => {
    setError("");
    setMessages((old) => [...old, { role: "user", content: question }]);
    try {
      const { data } = await axios.post("/api/chat", { document_id: document.document_id, question });
      setMessages((old) => [...old, { role: "assistant", content: data.answer, sources: data.sources }]);
    } catch (e) { setError(e.response?.data?.detail || "Unable to answer."); }
  };
  return <main className="app"><header><h1>PDF RAG Assistant</h1><p>Upload a PDF and ask questions about its contents.</p></header>
    <FileUpload document={document} onUpload={upload} />
    {error && <div className="error" role="alert">{error}</div>}
    <ChatBox disabled={!document} messages={messages} onAsk={ask} onClear={() => setMessages([])} /></main>;
}
