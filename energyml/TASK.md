# EnergyML delivery checklist

Status legend: `[ ]` pending, `[x]` verified.

## Phase 1 — Foundation

- [x] Inspect the existing repository and preserve unrelated work
- [x] Define architecture, database schema, reproducibility, API, testing and deployment plan
- [x] Create project packaging, configuration, logging and database session foundation
- [x] Add SQLAlchemy entities and Alembic migration

## Phase 2 — Datasets and features

- [x] Implement deterministic renewable generator and CSV registry
- [x] Implement leakage-safe forecasting feature engineering and chronological split
- [x] Implement consistent network state generator with configurable measurement noise
- [x] Add reproducibility and leakage tests

## Phase 3 — ML and artifacts

- [x] Implement forecasting pipeline, persistence baseline, metrics and plots
- [x] Implement multi-output state-estimation pipeline, per-bus metrics and plots
- [x] Implement root-constrained artifact storage, hashing and model metadata
- [x] Implement reusable experiment runners with failure lifecycle

## Phase 4 — Platform APIs

- [x] Implement dataset, experiment, comparison and artifact endpoints
- [x] Implement model registry and one-active-model-per-task activation
- [x] Implement forecasting/state inference with run logging
- [x] Implement health and platform statistics
- [x] Implement validation and safe error handling

## Phase 5 — Interfaces and operations

- [x] Add research dashboard
- [x] Add CLI scripts and full reproducible demo
- [x] Add Dockerfile, Compose, Makefile, environment example and GitHub Actions
- [x] Write professional README with live, non-hardcoded demo results

## Phase 6 — Verification and publication

- [x] Pass Ruff, Black, Mypy and Pytest
- [x] Run Alembic migration and the full demo
- [ ] Build Docker image and verify Compose/PostgreSQL persistence (blocked: host disk is full)
- [x] Verify both inference endpoints
- [x] Add EnergyML to portfolio and verify the portfolio build/tests
- [ ] Commit and publish the completed changes to Git
