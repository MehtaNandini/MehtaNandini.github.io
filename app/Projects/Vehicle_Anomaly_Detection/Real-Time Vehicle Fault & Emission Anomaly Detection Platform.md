# Real-Time Vehicle Fault & Emission Anomaly Detection Platform

A cloud-native automotive monitoring platform that streams vehicle telemetry, detects vehicle faults and emission anomalies, and generates AI-powered root-cause explanations using Gemini AI.

## Overview
This platform simulates live vehicle sensor data, stores it in PostgreSQL, detects anomalies using a rule-based engine, and generates human-readable AI diagnostic explanations. The React frontend presents a live dashboard with WebSockets for real-time fleet monitoring.

## Features
- Real-time telemetry ingestion
- Rule-based anomaly scoring (Emissions, Thermal, Fuel Systems)
- Gemini AI root-cause analysis explanations
- Live WebSocket broadcasts
- Modern dark automotive React dashboard

## Tech Stack
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, PostgreSQL, Google GenAI SDK
- **Frontend**: React, TypeScript, Vite, Vanilla CSS
- **DevOps**: Docker, Docker Compose, GitHub Actions CI

## Architecture
See `docs/architecture.md` for full component interactions.

## API Endpoints
- `GET /` - API Health check
- `POST /telemetry` - Submit telemetry payload
- `GET /telemetry/latest` - Last 20 records
- `GET /alerts` - Active anomalies
- `GET /vehicles` - Unique vehicles list
- `WS /ws/live` - WebSocket for live events

### Example Payload
```json
{
  "vehicle_id": "VH-101",
  "speed": 82,
  "rpm": 2300,
  "engine_temp": 91,
  "exhaust_temp": 430,
  "nox": 120,
  "co2": 180,
  "fuel_rate": 6.8,
  "engine_load": 64
}
```

## Local Setup

### Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your `GEMINI_API_KEY`. If left empty, a robust fallback explanation generator will be used.

### Docker Compose Instructions
Run the entire stack (Database, Backend, Simulator) locally:
```bash
docker compose up --build
```
This command maps the backend to `localhost:8000`.

### Frontend Setup
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```

## Testing Instructions

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

### Simulator
If you want to run the simulator directly outside docker:
```bash
cd simulator
export API_URL=http://localhost:8000/telemetry
python vehicle_simulator.py
```

## Deployment Notes for DigitalOcean
To deploy this on DigitalOcean:
1. Provision a DigitalOcean managed PostgreSQL database.
2. Update the `DATABASE_URL` environment variable.
3. Deploy the backend to DigitalOcean App Platform and configure the port to `8000`.
4. Deploy the frontend to App Platform as a Static Site.
5. Deploy the Simulator as a background worker component in App Platform.

## Future Improvements
- Isolation Forest ML model
- Autoencoder anomaly detection
- OBD/OBM fault-code mapping
- Grafana monitoring
- Authentication
- Kubernetes deployment
- DigitalOcean production deployment

## Screenshots
*(Placeholder)*

## Live Demo
[http://159.223.25.120](
  
)
run on local machine: http://localhost