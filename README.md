# IT Asset Intelligence Platform

A backend system for managing IT assets, dependencies, and risk analysis using FastAPI and SQLite.

## Features

- Asset Management (CRUD)
- Asset Relationships
- Dependency Tracking
- Impact Analysis
- Risk Scoring System

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Python

## API Endpoints

### Assets
- POST /assets
- GET /assets
- GET /assets/{id}
- PUT /assets/{id}
- DELETE /assets/{id}

### Relations
- POST /relations
- GET /relations

### Analysis
- GET /assets/{id}/dependencies
- GET /assets/{id}/impact
- GET /assets/{id}/risk

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy

python3 -m uvicorn app.main:app --reload
