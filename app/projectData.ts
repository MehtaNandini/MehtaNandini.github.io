export type ProjectScreenshot = {
  src: string;
  alt: string;
  caption: string;
};

export type PortfolioProject = {
  phase: string;
  title: string;
  shortTitle: string;
  statement: string;
  description: string;
  input: string;
  output: string;
  status: string;
  stack: readonly string[];
  technologies: readonly string[];
  features: readonly string[];
  future: readonly string[];
  screenshots: readonly ProjectScreenshot[];
};

export const projects: readonly PortfolioProject[] = [
  {
    phase: "Extract",
    title: "Document Classification & Extraction (NLP/OCR)",
    shortTitle: "Document Classification & Extraction AI",
    statement: "Classify heterogeneous documents and extract structured fields from scanned or digital input.",
    description:
      "A production-oriented document intelligence pipeline for invoices, receipts, ID cards, and bank statements. It detects scanned versus digital files, applies OCR when needed, classifies content with zero-shot NLP, and returns validated key-value data through an asynchronous API and interactive UI.",
    input: "PDF and image documents",
    output: "Classified structured data",
    status: "Production-ready demonstration",
    stack: ["Python", "FastAPI", "Streamlit", "Tesseract", "Transformers"],
    technologies: [
      "Python 3.11+",
      "FastAPI",
      "Pydantic",
      "Streamlit",
      "Tesseract OCR",
      "Hugging Face Transformers",
      "BART zero-shot classification",
      "Docker Compose",
    ],
    features: [
      "PDF, PNG, JPG, and JPEG ingestion",
      "Automatic digital-versus-scanned document detection",
      "Image preprocessing, denoising, thresholding, and OCR",
      "Zero-shot document classification",
      "Document-specific field extraction",
      "Asynchronous REST API with validated responses",
    ],
    future: [
      "Integrate LayoutLM or another NER model for stronger field extraction",
      "Add AWS Textract or Google Cloud Vision fallbacks",
      "Introduce Celery and Redis queues for large document batches",
    ],
    screenshots: [
      { src: "./projects/document-ai/01-dashboard.png", alt: "Document Classification and Extraction AI upload dashboard", caption: "Document ingestion dashboard" },
      { src: "./projects/document-ai/02-process-document.png", alt: "Processed document classification results", caption: "Processed document result" },
      { src: "./projects/document-ai/03-confidence-scores.png", alt: "Classification confidence scores and raw JSON", caption: "Classification confidence scores" },
      { src: "./projects/document-ai/04-raw-json-response.png", alt: "Structured raw JSON extraction response", caption: "Structured extraction response" },
    ],
  },
  {
    phase: "Retrieve",
    title: "RAG-Based LLM Application",
    shortTitle: "RAG-Based LLM Application",
    statement: "Generate grounded answers from uploaded documents with citations to the retrieved source chunks.",
    description:
      "A locally runnable retrieval-augmented generation system that accepts PDF, TXT, and Markdown files, chunks and embeds their content, retrieves relevant context from ChromaDB, and answers through configurable OpenAI, Ollama, or mock language models.",
    input: "Uploaded knowledge files",
    output: "Grounded cited answers",
    status: "Production-oriented local application",
    stack: ["Python", "FastAPI", "Streamlit", "ChromaDB", "RAG"],
    technologies: [
      "Python 3.11+",
      "FastAPI",
      "Pydantic",
      "Streamlit",
      "ChromaDB",
      "SentenceTransformers",
      "OpenAI API",
      "Ollama",
      "Pytest",
    ],
    features: [
      "Multi-format PDF, TXT, and Markdown upload",
      "Overlap-based sliding-window text chunking",
      "Local sentence-transformer embeddings",
      "ChromaDB similarity search",
      "Pluggable hosted, local, and mock LLM providers",
      "Strict grounding guardrails and source citations",
    ],
    future: [
      "Add multi-query and parent-document retrieval strategies",
      "Add conversation memory for follow-up questions",
      "Integrate OCR for scanned PDFs",
      "Complete Docker and Docker Compose deployment",
    ],
    screenshots: [
      { src: "./projects/rag-llm/01-dashboard.png", alt: "RAG application upload and question dashboard", caption: "Document upload and question interface" },
      { src: "./projects/rag-llm/02-grounded-answer.png", alt: "RAG application grounded positive answer", caption: "Grounded answer" },
      { src: "./projects/rag-llm/03-source-chunk.png", alt: "RAG answer source chunk citation", caption: "Retrieved source chunk" },
      { src: "./projects/rag-llm/04-grounding-guardrail.png", alt: "RAG application negative response when context is missing", caption: "Grounding guardrail response" },
    ],
  },
  {
    phase: "Model",
    title: "Manufacturing Knowledge Graph & Semantic Search Platform",
    shortTitle: "Manufacturing Knowledge Graph Platform",
    statement: "Turn manufacturing documents into reviewed, validated, and searchable semantic knowledge.",
    description:
      "A full-stack semantic modelling platform that extracts entities and relationships from manufacturing content, sends them through human review, validates RDF/OWL data with SHACL, and combines vector retrieval with SPARQL graph queries.",
    input: "Manufacturing documents",
    output: "Validated semantic graph",
    status: "Full-stack platform scope implemented",
    stack: ["Python", "React", "RDF/OWL", "Qdrant", "SPARQL"],
    technologies: [
      "Python 3.11",
      "FastAPI",
      "SQLAlchemy",
      "PostgreSQL",
      "RDFLib",
      "PySHACL",
      "SpaCy",
      "SentenceTransformers",
      "React and TypeScript",
      "Cytoscape.js",
      "Qdrant",
      "Apache Jena Fuseki",
      "Docker",
    ],
    features: [
      "PDF, DOCX, TXT, and HTML document ingestion",
      "Entity and relationship extraction",
      "Human approval and rejection workflow",
      "RDF/OWL graph generation with SHACL validation",
      "Hybrid vector and BM25 semantic search",
      "SPARQL query interface and interactive graph explorer",
      "JWT authentication and role-based access control",
    ],
    future: [
      "The supplied project notes do not list a separate future-work roadmap",
      "Current documented scope focuses on platform hardening, tests, and secure role-based operation",
    ],
    screenshots: [
      { src: "./projects/manufacturing-kg/01-dashboard.png", alt: "Manufacturing knowledge graph platform dashboard", caption: "Platform overview" },
      { src: "./projects/manufacturing-kg/02-documents.png", alt: "Manufacturing document ingestion view", caption: "Document ingestion" },
      { src: "./projects/manufacturing-kg/03-review-workflow.png", alt: "Knowledge extraction review workflow", caption: "Human review queue" },
      { src: "./projects/manufacturing-kg/04-review-detail.png", alt: "Detailed manufacturing entity review", caption: "Entity review detail" },
      { src: "./projects/manufacturing-kg/05-review-approved.png", alt: "Approved manufacturing knowledge review", caption: "Approved knowledge" },
      { src: "./projects/manufacturing-kg/06-review-pending.png", alt: "Pending manufacturing knowledge review", caption: "Pending knowledge" },
      { src: "./projects/manufacturing-kg/07-review-rejected.png", alt: "Rejected manufacturing knowledge review", caption: "Rejected knowledge" },
      { src: "./projects/manufacturing-kg/08-graph-explorer.png", alt: "Manufacturing graph explorer", caption: "Knowledge graph explorer" },
      { src: "./projects/manufacturing-kg/09-graph-detail.png", alt: "Manufacturing knowledge graph detail", caption: "Connected entity detail" },
      { src: "./projects/manufacturing-kg/10-semantic-search.png", alt: "Manufacturing semantic search interface", caption: "Semantic search" },
      { src: "./projects/manufacturing-kg/11-sparql-search.png", alt: "Manufacturing SPARQL query results", caption: "SPARQL query" },
      { src: "./projects/manufacturing-kg/12-sparql-limit.png", alt: "Manufacturing SPARQL query limited results", caption: "Controlled SPARQL result set" },
    ],
  },
  {
    phase: "Act",
    title: "Agentic AI Assistant with LangGraph",
    shortTitle: "Agentic AI Assistant",
    statement: "Plan multi-step tasks, choose tools, reflect on results, and retain useful conversational memory.",
    description:
      "A personal AI assistant built around a LangGraph state machine, a FastAPI service, and a Streamlit interface. It decomposes tasks, calls calculator, file, note, and web-search tools, evaluates intermediate results, and persists checkpoints in SQLite.",
    input: "Natural-language tasks",
    output: "Tool-assisted execution",
    status: "Production-ready personal assistant",
    stack: ["Python", "LangGraph", "FastAPI", "Streamlit", "SQLite"],
    technologies: [
      "Python 3.11+",
      "LangGraph",
      "LangChain",
      "FastAPI",
      "Streamlit",
      "SQLite checkpoints",
      "Pydantic",
      "Pytest",
      "Ruff",
    ],
    features: [
      "Dynamic multi-step task planning and execution",
      "Calculator, local file, memory, and web-search tools",
      "Reflection on intermediate tool results",
      "Stateful conversation checkpoints",
      "FastAPI backend with validated schemas",
      "Interactive UI showing safe execution progress",
    ],
    future: [
      "Add Tavily or Google Custom Search",
      "Stream tokens in real time",
      "Strengthen local-file permission boundaries",
      "Migrate checkpoints from SQLite to PostgreSQL",
    ],
    screenshots: [
      { src: "./projects/agentic-assistant/01-dashboard.png", alt: "Agentic AI Assistant chat dashboard", caption: "Assistant workspace" },
      { src: "./projects/agentic-assistant/02-task-response.png", alt: "Agentic assistant multi-step task response", caption: "Multi-step task execution" },
      { src: "./projects/agentic-assistant/03-task-follow-up.png", alt: "Agentic assistant follow-up response", caption: "Follow-up execution" },
      { src: "./projects/agentic-assistant/04-memory-test.png", alt: "Agentic assistant memory test", caption: "Stateful memory test" },
      { src: "./projects/agentic-assistant/05-personal-project-answer.png", alt: "Agentic assistant answer from a personal project file", caption: "Local project knowledge response" },
    ],
  },
  {
    phase: "Assess",
    title: "ClaimVision AI — Multimodal Insurance Claim Analyzer",
    shortTitle: "ClaimVision AI",
    statement: "Combine damage imagery, documents, invoices, and descriptions into a structured insurance assessment.",
    description:
      "A production-style multimodal platform that applies OCR, computer vision, document extraction, and LLM reasoning to vehicle claims. It classifies damage, extracts fields, compares evidence with invoice values, generates risk indicators, and presents the result in a modern claims dashboard.",
    input: "Claim images and documents",
    output: "Risk-scored claim report",
    status: "Production-style demonstration platform",
    stack: ["React", "FastAPI", "PostgreSQL", "Vision AI", "OCR"],
    technologies: [
      "React",
      "TypeScript",
      "Vite",
      "Python",
      "FastAPI",
      "PostgreSQL",
      "PyMuPDF",
      "PyTesseract",
      "Vision APIs",
      "LLM field extraction",
      "Docker Compose",
    ],
    features: [
      "Multimodal reasoning across images, invoices, and claim text",
      "Vehicle-part and damage-severity image analysis",
      "OCR fallback for scanned claim documents",
      "Structured field extraction and claim summaries",
      "Invoice-versus-damage anomaly detection",
      "Risk scoring, reporting, and claims management",
    ],
    future: [
      "Integrate local Hugging Face vision models",
      "Train more granular risk scoring on historical claim data",
      "Improve complex multi-page invoice layout extraction",
    ],
    screenshots: [
      { src: "./projects/claimvision-ai/01-dashboard.png", alt: "ClaimVision AI dashboard", caption: "Claims intelligence dashboard" },
      { src: "./projects/claimvision-ai/02-claims-management.png", alt: "ClaimVision claims management table", caption: "Claims management" },
      { src: "./projects/claimvision-ai/03-ai-insights.png", alt: "ClaimVision AI insight panel", caption: "AI-generated insights" },
      { src: "./projects/claimvision-ai/04-primary-damage.png", alt: "ClaimVision primary vehicle damage analysis", caption: "Primary damage analysis" },
      { src: "./projects/claimvision-ai/05-rear-impact.png", alt: "ClaimVision rear impact analysis", caption: "Rear-impact analysis" },
      { src: "./projects/claimvision-ai/06-notifications.png", alt: "ClaimVision notification center", caption: "Risk notifications" },
      { src: "./projects/claimvision-ai/07-reporting.png", alt: "ClaimVision reporting dashboard", caption: "Claims reporting" },
      { src: "./projects/claimvision-ai/08-risk-models.png", alt: "ClaimVision risk model interface", caption: "Risk models" },
      { src: "./projects/claimvision-ai/09-settings.png", alt: "ClaimVision settings", caption: "Platform settings" },
    ],
  },
  {
    phase: "Monitor",
    title: "Real-Time Vehicle Fault & Emission Anomaly Detection Platform",
    shortTitle: "Vehicle Anomaly Detection",
    statement: "Stream vehicle telemetry, detect faults and emission anomalies, and explain likely root causes.",
    description:
      "A cloud-native automotive monitoring system that simulates live sensor telemetry, stores it in PostgreSQL, scores emissions, thermal, and fuel-system anomalies, and broadcasts fleet state through WebSockets with Gemini-powered diagnostic explanations.",
    input: "Live vehicle telemetry",
    output: "Fault alerts and diagnostics",
    status: "Locally running full-stack platform",
    stack: ["Python", "React", "WebSockets", "PostgreSQL", "Gemini"],
    technologies: [
      "Python 3.11",
      "FastAPI",
      "SQLAlchemy",
      "PostgreSQL",
      "Google GenAI SDK",
      "React",
      "TypeScript",
      "Vite",
      "WebSockets",
      "Docker Compose",
      "GitHub Actions",
    ],
    features: [
      "Real-time telemetry ingestion and simulation",
      "Emissions, thermal, and fuel-system anomaly scoring",
      "Gemini AI root-cause explanations with a fallback generator",
      "Live WebSocket fleet broadcasts",
      "Vehicle, anomaly, and history dashboards",
      "Containerized backend, database, and simulator",
    ],
    future: [
      "Add Isolation Forest and autoencoder models",
      "Map OBD and OBM fault codes",
      "Add Grafana observability and authentication",
      "Prepare Kubernetes and DigitalOcean production deployment",
    ],
    screenshots: [
      { src: "./projects/vehicle-anomaly/01-dashboard-healthy.png", alt: "Vehicle anomaly dashboard showing a healthy fleet", caption: "Healthy fleet dashboard" },
      { src: "./projects/vehicle-anomaly/02-dashboard-anomaly.png", alt: "Vehicle anomaly dashboard showing reduced fleet health", caption: "Fleet anomaly state" },
      { src: "./projects/vehicle-anomaly/03-anomaly-logs.png", alt: "Vehicle fault and emission anomaly logs", caption: "Anomaly logs" },
      { src: "./projects/vehicle-anomaly/04-history-logs.png", alt: "Vehicle telemetry history logs", caption: "Telemetry history" },
      { src: "./projects/vehicle-anomaly/05-fleet-view.png", alt: "Vehicle anomaly fleet view", caption: "Fleet view" },
      { src: "./projects/vehicle-anomaly/06-telemetry-vh103.png", alt: "Vehicle VH-103 telemetry detail", caption: "VH-103 telemetry" },
      { src: "./projects/vehicle-anomaly/07-telemetry-vh104.png", alt: "Vehicle VH-104 medium anomaly telemetry detail", caption: "VH-104 anomaly telemetry" },
    ],
  },
];
