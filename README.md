# PDF RAG Assistant

PDF RAG Assistant is a local Retrieval-Augmented Generation application. It lets a user upload a PDF, index its text, and ask questions about that document through a React web interface.

The application uses:

- **Frontend:** React, Vite, JavaScript, Axios
- **Backend:** Python, FastAPI, LangChain
- **PDF extraction:** PyMuPDF
- **Text splitting:** LangChain `RecursiveCharacterTextSplitter`
- **Embeddings:** Ollama with `nomic-embed-text`
- **Chat model:** Ollama with `llama3.2`
- **Vector database:** ChromaDB

The application runs locally and does not require an OpenAI API key.

## How the application works

1. The user selects a PDF in the React interface.
2. The frontend sends the file to `POST /api/upload`.
3. FastAPI validates the file and temporarily saves it.
4. PyMuPDF extracts text page by page.
5. Empty pages are skipped. Each extracted page keeps its page number.
6. LangChain splits page text into overlapping chunks.
7. Ollama generates an embedding for every chunk.
8. ChromaDB stores the chunks, embeddings, document ID, filename, and page number.
9. The user enters a question.
10. The frontend sends the question and selected `document_id` to `POST /api/chat`.
11. The question is embedded with Ollama.
12. ChromaDB retrieves the most relevant chunks belonging only to that document.
13. The retrieved chunks are provided to the Ollama chat model.
14. The model is instructed to answer only from the retrieved context.
15. The frontend displays the answer and deduplicated source pages.

If the answer is not present in the retrieved PDF context, the assistant responds:

> I could not find the answer in the uploaded document.

## Project structure

```text
rag_projec/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application and startup
│   │   ├── config.py               # Environment-based settings
│   │   ├── schemas.py              # Request and response models
│   │   ├── rag/
│   │   │   ├── document_loader.py  # PDF text extraction
│   │   │   ├── text_splitter.py    # Chunking
│   │   │   ├── embeddings.py       # Ollama embeddings
│   │   │   ├── vector_store.py     # ChromaDB indexing and search
│   │   │   └── qa_chain.py         # Retrieval and Ollama answer generation
│   │   └── routes/
│   │       ├── upload.py            # POST /api/upload
│   │       └── chat.py              # POST /api/chat
│   ├── data/
│   │   ├── uploads/                 # Temporary upload location
│   │   └── chroma/                  # Persistent ChromaDB data
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   ├── ChatBox.jsx
│   │   │   ├── Message.jsx
│   │   │   └── Loading.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
├── .env
├── .env.example
└── README.md
```

## Prerequisites

Install the following software:

- Python 3.10 or newer
- Node.js 18 or newer
- Ollama

Verify the installations in PowerShell:

```powershell
python --version
node --version
npm --version
ollama --version
```

## Ollama setup

Start Ollama. On Windows, opening the Ollama application normally starts the local service. The default service URL is:

```text
http://localhost:11434
```

Pull the models used by this project:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

Confirm that both models are installed:

```powershell
ollama list
```

You should see `llama3.2` and `nomic-embed-text` in the output.

## Configuration

The project reads configuration from the root `.env` file. If `.env` does not exist, copy the example:

```powershell
Copy-Item .env.example .env
```

The default configuration is:

```dotenv
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2
EMBEDDING_MODEL=nomic-embed-text
LLM_TEMPERATURE=0.2
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K=4
MAX_UPLOAD_SIZE_MB=20
CHROMA_PERSIST_DIRECTORY=./data/chroma
UPLOAD_DIRECTORY=./data/uploads
CORS_ORIGINS=http://localhost:5173
```

Configuration values:

| Variable | Purpose |
|---|---|
| `OLLAMA_BASE_URL` | URL of the local Ollama service |
| `LLM_MODEL` | Ollama model used to generate answers |
| `EMBEDDING_MODEL` | Ollama model used to create embeddings |
| `LLM_TEMPERATURE` | Response randomness; lower values are more deterministic |
| `CHUNK_SIZE` | Maximum size of each text chunk |
| `CHUNK_OVERLAP` | Number of overlapping characters between chunks |
| `TOP_K` | Number of relevant chunks retrieved for a question |
| `MAX_UPLOAD_SIZE_MB` | Maximum accepted PDF size |
| `CHROMA_PERSIST_DIRECTORY` | Directory where ChromaDB stores vectors |
| `UPLOAD_DIRECTORY` | Temporary upload directory |
| `CORS_ORIGINS` | Frontend origins allowed by FastAPI |

Do not add an OpenAI key to this project. The current implementation uses Ollama.

## Install backend dependencies

From the project root:

```powershell
cd C:\Users\dubba\Downloads\rag_projec
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

If PowerShell blocks environment activation, run the backend with the virtual-environment interpreter directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

## Run the backend

Open a PowerShell terminal and run:

```powershell
cd C:\Users\dubba\Downloads\rag_projec\backend
C:\Users\dubba\Downloads\rag_projec\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend is available at:

```text
http://127.0.0.1:8000
```

Check that it is running:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/health
```

Expected response:

```json
{"status":"ok"}
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Run the frontend

Open a second PowerShell terminal:

```powershell
cd C:\Users\dubba\Downloads\rag_projec\frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally:

```text
http://localhost:5173
```

The Vite development proxy forwards `/api` requests to the FastAPI backend.

## Using the application

1. Open `http://localhost:5173`.
2. Choose a PDF file.
3. Click **Upload PDF**.
4. Wait for indexing to finish.
5. Confirm that the filename and chunk count are displayed.
6. Enter a question about the uploaded document.
7. Click **Send** or press Enter.
8. Read the answer and the source pages shown below it.
9. Use **Clear chat** to remove the current conversation history.

Only PDF files are accepted. The backend also rejects empty files, files above the configured size limit, and PDFs with no extractable text.

## API reference

### Health check

```http
GET /api/health
```

Response:

```json
{"status":"ok"}
```

### Upload and index a PDF

```http
POST /api/upload
Content-Type: multipart/form-data
```

The multipart field must be named `file`.

Example response:

```json
{
  "success": true,
  "message": "PDF indexed successfully.",
  "document_id": "a1b2c3...",
  "filename": "example.pdf",
  "chunks": 12
}
```

Save the returned `document_id`. It identifies the uploaded document and is required for chat requests.

### Ask a question

```http
POST /api/chat
Content-Type: application/json
```

Request:

```json
{
  "document_id": "a1b2c3...",
  "question": "What is the main topic of this document?"
}
```

Response:

```json
{
  "answer": "The document is about ...",
  "sources": [
    {
      "filename": "example.pdf",
      "page": 2
    }
  ]
}
```

Retrieval is filtered by `document_id`, so chunks from other uploaded PDFs are not used.

## Troubleshooting

### `model "nomic-embed-text" not found`

Pull the embedding model:

```powershell
ollama pull nomic-embed-text
```

### `model "llama3.2" not found`

Pull the chat model:

```powershell
ollama pull llama3.2
```

### Ollama connection refused

Make sure Ollama is running and check the service:

```powershell
Invoke-WebRequest http://localhost:11434/api/tags
```

If the request fails, start the Ollama desktop application and restart the backend.

### `Address already in use` on port 8000

Another backend process is already using the port. Either reuse that running backend or stop the process before starting another one:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen
```

Do not start multiple backend processes on the same port.

### Upload reports no extractable text

The PDF may be scanned images rather than text-based pages. This application currently extracts text with PyMuPDF and does not perform OCR. Use a text-based PDF or add an OCR preprocessing step.

### Frontend cannot reach the backend

Check all of the following:

- The backend is running on port `8000`.
- The frontend is running on port `5173`.
- `CORS_ORIGINS` includes `http://localhost:5173`.
- The browser is using the Vite URL, not the backend URL.

## Development commands

Build the frontend for production:

```powershell
cd C:\Users\dubba\Downloads\rag_projec\frontend
npm run build
```

Preview the production frontend build:

```powershell
npm run preview
```

The ChromaDB files are stored in `backend\data\chroma` when the backend is run from the backend directory. Do not delete this directory unless you intentionally want to remove the indexed document data.
#   B a s i c _ r a g  
 