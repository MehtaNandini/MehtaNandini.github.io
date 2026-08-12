# Manufacturing Knowledge Graph and Semantic Search Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Overview
A full-stack semantic modelling and machine learning platform for manufacturing knowledge management. The platform ingests manufacturing documents, extracts entities and relationships, creates an RDF/OWL knowledge graph validated with SHACL, and provides hybrid semantic search using vector embeddings and SPARQL graph queries.

## Problem Statement
Manufacturing industries generate vast amounts of unstructured data (maintenance logs, quality reports, sensor specs). Finding actionable insights, tracing defects to root causes, or searching for specific measurements across thousands of documents is incredibly challenging. This platform solves this by structuring unstructured text into a queried semantic knowledge graph.

## Features
- **Document Ingestion:** Upload PDF, DOCX, TXT, HTML.
- **NLP Pipeline:** Entity and Relationship extraction using SpaCy and Transformers.
- **Human-in-the-Loop:** Review, approve, and reject extracted knowledge before it enters the graph.
- **Knowledge Graph:** RDF/OWL knowledge graph backed by Apache Jena Fuseki.
- **SHACL Validation:** Validates data against the Core Manufacturing Ontology.
- **Semantic Search:** Hybrid search using Qdrant for vector embeddings and BM25.
- **SPARQL Interface:** Execute complex graph queries.
- **Graph Visualization:** Cytoscape.js powered interactive graph explorer.

## Architecture Diagram
Please see [docs/architecture.md](docs/architecture.md).

## Technology Stack
- **Backend:** Python 3.11, FastAPI, SQLAlchemy, PostgreSQL, RDFLib, SPARQLWrapper, PySHACL, SpaCy, Sentence Transformers.
- **Frontend:** React, TypeScript, Vite, React Router, TanStack Query, Cytoscape.js.
- **Infrastructure:** Docker, Qdrant (Vector DB), Apache Jena Fuseki (Triple Store).

## Local Setup
1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Run `docker compose up --build`.
4. Access frontend at `http://localhost:3000` and API docs at `http://localhost:8000/docs`.

## Generate Demo Data
Run the following script to generate 20 sample manufacturing documents:
```bash
python scripts/generate_sample_documents.py
```

## Testing
Run backend unit tests:
```bash
cd backend
pytest tests/
```

## Security
- JWT based authentication.
- Role-based access control (Admin, Researcher, Viewer).
- Read-only SPARQL access for viewers.
- Path traversal protection on file uploads.

## License
MIT License.
