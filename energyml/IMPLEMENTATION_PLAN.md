# EnergyML Research Platform — Implementation Plan

## Architecture

EnergyML is a layered FastAPI application. API routers validate requests and delegate to
services; services own dataset, experiment, model, and inference workflows; SQLAlchemy
repositories persist metadata; ML modules contain deterministic generators, feature
engineering, estimators, metrics, and plotting; `ArtifactManager` is the only component
that writes or loads model artifacts. A lightweight server-rendered dashboard consumes the
same APIs. CLI scripts call application services instead of duplicating training logic.

## Database schema

- `datasets`: immutable dataset identity, type/version/seed, generation configuration,
  row count, safe CSV path and SHA-256 hash.
- `experiments`: lifecycle state, dataset relationship, configuration, deterministic seed,
  timings, metrics, artifact directory/hash, code version, performance metadata, and errors.
- `models`: one versioned artifact per completed experiment, metrics, task type and active flag.
- `inference_runs`: model/experiment references, task, hashed input, prediction and duration.

Foreign keys and indexes support traceability. Referenced datasets cannot be deleted. SQLite
is the local/test default; PostgreSQL is selected with `DATABASE_URL` in Docker Compose.
Alembic owns schema migration for deployment.

## Dataset generation

The renewable generator uses `numpy.random.Generator` with seasonal and diurnal signals,
temporally correlated wind/cloud weather, capacity-based solar and wind production, and
controlled noise. The state-estimation generator creates network operating states from
load/generation factors and a documented linearised radial voltage-drop model, then adds
Gaussian uncertainty to measurements. Identical configuration and seed yield byte-equivalent
data values and stable dataset hashes.

## Feature engineering

Renewable features include calendar/weather values plus lags 1/3/6/24 and shifted rolling
means 3/6/24. All rolling windows are shifted before aggregation so a row can never use its
own or future target. Rows made incomplete by lagging are dropped. Splits are strictly
chronological and configurable. State estimation selects measurement columns and multiple
bus-voltage targets from the registered dataset.

## Forecasting pipeline

`HistGradientBoostingRegressor` is used because it is deterministic with fixed input and
parameters, handles non-linear weather interactions, and is efficient for a year of hourly
data. A scikit-learn `Pipeline` packages imputation, scaling, and the estimator for identical
training/inference preprocessing. Held-out test metrics are compared with a 24-hour
persistence baseline. Permutation importance provides model-agnostic feature importance.

## State-estimation pipeline

`RandomForestRegressor` directly performs deterministic multi-output regression with a fixed
seed and configurable forest parameters. A `Pipeline` packages median imputation and the
forest. Evaluation reports aggregate and per-bus MAE/RMSE/R2 plus diagnostic plots.

## Experiment tracking

`BaseExperimentRunner` implements pending/running/completed/failed lifecycle handling,
timings, dataset loading, artifact finalisation, model registration, and error persistence.
Specialised runners only prepare data, train, evaluate and plot. Configurations, seed,
dataset version/hash, code version, feature list, timings, feature count, dataset size and
model size are stored with every run.

## Artifact management

Artifacts live under generated task/experiment UUID directories. The manager validates all
paths against its configured root, writes joblib pipelines, JSON metadata/config/metrics and
PNG plots, calculates SHA-256 hashes, and only deserialises paths already registered in the
database. No API accepts an arbitrary model path.

## API design

Version-neutral `/api` endpoints expose health/stats; dataset generation/list/detail/delete;
forecasting and state-estimation experiments; comparison, metrics and artifact manifests;
model list/detail/activation; and both inference tasks. Pydantic rejects non-finite or
out-of-range values. Domain errors map to concise HTTP errors without stack traces.

## Dashboard

FastAPI serves a compact HTML/CSS/JavaScript research dashboard with overview, dataset,
experiment, model and inference panels. It calls the public APIs and is intentionally kept
lightweight so engineering effort remains concentrated on reproducible ML workflows.

## Testing

Unit tests cover deterministic generation, seed differences, schemas, leakage-safe features,
chronological splitting, metrics, baselines, both estimators, artifact hashing/loading and
configuration. Integration tests use temporary SQLite databases and artifact/data roots to
exercise generation → training → registration → activation → inference, along with health,
comparison, validation, deletion protection and failed lifecycle behaviour.

## Docker deployment

The Python 3.12 image installs the locked project, runs Alembic, and starts Uvicorn as an
unprivileged user. Compose provisions PostgreSQL with a health check plus persistent database,
dataset and artifact volumes. The app health check calls `/api/health`.

## Security

Configuration is environment based and secrets are never committed. Generated UUIDs—not
user paths—select files; path resolution is root constrained; payload sizes and numeric
ranges are validated; only registry-owned artifacts are loaded; logs omit full datasets,
model objects and raw inference payloads.

## Reproducibility strategy

Every stochastic component receives the recorded seed. Dataset configuration is canonicalised
before hashing, time-series order is stable, scikit-learn model seeds are explicit, and all
train/validation/test boundaries are recorded. The full demo uses seed 42 and application
services. CI repeats formatting, linting, type checking, tests and image build.
