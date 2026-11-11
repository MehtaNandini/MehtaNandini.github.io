# Start EnergyML on another computer

The archive includes two deterministic sample datasets, two completed experiments, active
models, plots, metrics and a pre-populated SQLite registry:

- `datasets/renewable/`: 8,760 hourly observations for a full year
- `datasets/state_estimation/`: 5,000 five-bus distribution-network samples

Both datasets use seed 42. Their SHA-256 hashes are recorded in `backend/energyml.db` and are
checked before training.

The completed examples are an annual renewable forecast and a five-bus voltage state
estimator. Their model files and evaluation plots are under `artifacts/`, and both models are
already active for inference.

## Option 1: Python 3.12 (uses the bundled data)

From the extracted `energyml` directory:

### macOS or Linux

```bash
python3.12 -m venv backend/.venv
backend/.venv/bin/pip install -e backend
cp .env.example backend/.env
cd backend
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Windows PowerShell

```powershell
py -3.12 -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -e backend
Copy-Item .env.example backend/.env
Set-Location backend
.venv/Scripts/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then open:

- Dashboard: <http://127.0.0.1:8000>
- Interactive API documentation: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/api/health>

Do not open `dashboard.html` directly. A `file:///...` address cannot reach FastAPI; always use
the HTTP address printed by Uvicorn.

## Option 2: Docker

```bash
docker compose up --build
```

Docker uses PostgreSQL and its own persistent volumes, so it starts with an empty registry.
Use the dashboard or Swagger UI to generate/register datasets in that environment. The bundled
CSV files remain available for inspection and for the SQLite workflow above.

## Verify the bundled data

After starting with Option 1, open <http://127.0.0.1:8000/api/datasets>. You should see the
annual renewable dataset and the synthetic distribution-network dataset. The dashboard's
Experiments and Models sections should each contain two ready-to-use records.
