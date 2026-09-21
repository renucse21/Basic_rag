import { useState } from "react";
import Loading from "./Loading";
import Message from "./Message";

export default function ChatBox({ disabled, messages, onAsk, onClear }) {
  const [question, setQuestion] = useState(""); const [busy, setBusy] = useState(false);
  const submit = async (e) => { e.preventDefault(); if (!question.trim() || busy || disabled) return; const value = question.trim(); setQuestion(""); setBusy(true); await onAsk(value); setBusy(false); };
  return <section className="chat panel"><div className="chat-title"><h2>Chat</h2><button className="clear" onClick={onClear} disabled={!messages.length}>Clear chat</button></div><div className="history">{!messages.length && <p className="empty">Upload a document to start chatting.</p>}{messages.map((message, i) => <Message key={i} {...message} />)}{busy && <Loading />}</div><form onSubmit={submit}><input disabled={disabled || busy} value={question} onChange={(e) => setQuestion(e.target.value)} placeholder={disabled ? "Upload a PDF first..." : "Ask a question (Enter to send)"} /><button disabled={disabled || busy || !question.trim()}>Send</button></form></section>;
}
