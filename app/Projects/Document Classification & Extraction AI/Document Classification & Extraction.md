# Document Classification & Extraction (NLP/OCR)

**An intelligent pipeline for extracting and classifying information from scanned and digital documents using Computer Vision and Natural Language Processing.**

This project demonstrates a production-ready approach to processing heterogeneous documents (invoices, receipts, ID cards, bank statements). It intelligently detects whether a document requires Optical Character Recognition (OCR) or direct text extraction, classifies the document using Zero-Shot NLP models, and extracts structured key-value fields.

## Features
- **Smart Ingestion:** Accepts PDF, PNG, JPG, and JPEG. Detects digital vs. scanned PDFs.
- **Robust OCR:** Image preprocessing (denoising, thresholding) and Tesseract OCR integration.
- **NLP Classification:** Zero-shot classification powered by Hugging Face (`facebook/bart-large-mnli`).
- **Targeted Field Extraction:** Context-aware regex and NLP extraction based on document type.
- **FastAPI Backend:** Fully asynchronous REST API with Pydantic validation.
- **Streamlit UI:** Interactive frontend for testing and demonstrating the pipeline.

## Architecture
See [Architecture Diagram](architecture.md) for a complete system flow.

## Setup & Installation

### Prerequisites
1. **Python 3.11+**
2. **Tesseract OCR:** 
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`
3. **Poppler (for PDF support):**
   - macOS: `brew install poppler`
   - Linux: `sudo apt-get install poppler-utils`

### Installation
```bash
git clone https://github.com/MehtaNandini/Document-_Classification-Extraction.git
cd Document-_Classification-Extraction
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Running the Application

### Option 1: Using Docker (Recommended)
You can easily spin up both the FastAPI backend and Streamlit UI using Docker Compose:
```bash
docker compose up --build -d
```
- **Streamlit UI:** `http://localhost:8501`
- **FastAPI Documentation:** `http://localhost:8000/docs`

### Option 2: Running Locally

**Start the FastAPI Backend**
```bash
uvicorn app.main:app --reload
```
API documentation available at `http://localhost:8000/docs`

**Start the Streamlit UI**
In a new terminal window:
```bash
source venv/bin/activate
streamlit run app/ui/streamlit_app.py
```
Access the UI at `http://localhost:8501`

## API Usage Example

**Endpoint:** `POST /api/v1/process-document`

```bash
curl -X POST "http://localhost:8000/api/v1/process-document" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/sample_documents/invoice.png"
```

**Sample Output:**
```json
{
  "filename": "invoice.png",
  "extracted_text": "Invoice Number: INV-12345...",
  "classification": {
    "document_type": "invoice",
    "scores": {
      "invoice": 0.98,
      "resume/cv": 0.01,
      "generic document": 0.01
    }
  },
  "fields": {
    "document_type": "invoice",
    "extracted_fields": {
      "invoice_number": "INV-12345",
      "date": "2026-07-01",
      "total_amount": "1,250.00"
    }
  }
}
```

## Future Improvements
- Integrate Named Entity Recognition (NER) models (e.g., LayoutLM) for more robust field extraction.
- Support cloud OCR providers (AWS Textract, Google Cloud Vision) as fallbacks.
- Add asynchronous processing queues (Celery/Redis) for large document batches.

## License
MIT License
