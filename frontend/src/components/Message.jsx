export default function Message({ role, content, sources = [] }) {
  return <article className={`message ${role}`}><b>{role === "user" ? "You" : "Assistant"}</b><p>{content}</p>{sources.length > 0 && <div className="sources"><strong>Sources:</strong>{sources.map((source) => <span key={`${source.filename}-${source.page}`}>{source.filename}{source.page ? `, page ${source.page}` : ""}</span>)}</div>}</article>;
}
