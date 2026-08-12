# 📚 RAG-Based LLM Application

> A complete, locally-run Retrieval-Augmented Generation (RAG) pipeline built with Python, FastAPI, and Streamlit.

This project demonstrates a production-ready, interview-friendly implementation of a Retrieval-Augmented Generation (RAG) system. It allows users to upload documents (PDF, TXT, MD), indexes them into a vector database, and generates grounded answers using a Large Language Model (LLM) based purely on the provided context.

## ✨ Features

- **📄 Multi-format Document Upload**: Support for PDF, TXT, and Markdown files.
- **🔪 Custom Text Chunking**: Clean, overlap-based sliding window text chunking strategy.
- **🧠 Local Embeddings**: Uses `sentence-transformers` for fast, private, and free vector embeddings.
- **🗃️ Vector Database**: Uses `ChromaDB` for efficient similarity search and retrieval.
- **🤖 Pluggable LLMs**: Configurable support for OpenAI, Ollama (local models like Llama 3), and a Mock LLM for testing.
- **🛡️ Strict Grounding Guardrails**: Built-in prompts to prevent hallucinations. The LLM will explicitly state if information is missing from the context.
- **🔗 Source Citations**: Every answer includes references to the exact document chunks used.
- **🎨 Interactive UI**: A clean, user-friendly frontend built with Streamlit.
- **🚀 API-First**: Backend powered by a robust, asynchronous FastAPI application.

## 🏗️ Architecture

See the [Architecture Document](architecture.md) for detailed Mermaid diagrams of the ingestion and retrieval flows.

### Core Tech Stack
- **Backend**: FastAPI, Pydantic, Python 3.11+
- **Frontend**: Streamlit
- **Vector DB**: ChromaDB
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`)
- **LLM Integration**: OpenAI API, Ollama (Local)
- **Tooling**: Pytest, Ruff, python-dotenv

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/rag-based-llm-application.git
cd rag-based-llm-application
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Copy the example environment file and edit it to your preference:
```bash
cp .env.example .env
```
Open `.env` and set `LLM_PROVIDER` to `mock`, `openai`, or `ollama`. If using `openai`, add your API key.

### 5. Run the Application

**Start the FastAPI Backend:**
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000/docs`

**Start the Streamlit Frontend (in a new terminal):**
```bash
streamlit run ui/streamlit_app.py
```
The UI will open in your browser at `http://localhost:8501`

## 🧪 Testing and Evaluation

**Run Unit Tests:**
```bash
pytest tests/
```

**Run Evaluation Script:**
Start the backend server, then run:
```bash
python evaluation/eval_rag.py
```

## 📸 Screenshots
*(Placeholder: Add screenshots of your Streamlit UI here)*

## 🔮 Future Improvements
- [ ] Implement advanced retrieval strategies (e.g., Multi-Query, Parent-Document Retriever).
- [ ] Add conversation history memory for follow-up questions.
- [ ] Integrate OCR for scanned PDFs.
- [ ] Deploy using Docker and Docker Compose.

## 📄 License
This project is licensed under the MIT License.
