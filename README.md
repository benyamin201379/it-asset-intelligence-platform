# IT Asset Intelligence Platform

A backend API for managing IT assets, tracking system dependencies, analyzing impact, and calculating risk scores.

## Overview

Modern IT environments are highly interconnected.  
This project models IT assets and their relationships, making it possible to understand dependencies between systems, detect cascading effects, and estimate operational risk.

The platform is built as a backend service using FastAPI, SQLAlchemy, and SQLite.

## Key Features

- Full CRUD for IT assets
- Relationship management between systems
- Dependency tracking
- Impact analysis
- Risk scoring based on asset criticality and dependencies
- Prevention of duplicate relationships
- Interactive API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite

## API Endpoints

### Assets
- `POST /assets`
- `GET /assets`
- `GET /assets/{id}`
- `PUT /assets/{id}`
- `DELETE /assets/{id}`
- `GET /assets/critical/list`

### Relations
- `POST /relations`
- `GET /relations`

### Analysis
- `GET /assets/{id}/dependencies`
- `GET /assets/{id}/impact`
- `GET /assets/{id}/risk`

## Example Use Case

This project can be used to model scenarios such as:

- An application server depends on a database server
- A database server depends on storage or network services
- If one component fails, downstream systems can be identified
- A simple risk score can be calculated automatically

This makes the project useful as a simplified prototype for IT asset intelligence, CMDB-like system modeling, or infrastructure dependency analysis.

## Run Locally

1. Clone the repository

```bash
git clone https://github.com/benyamin201379/it-asset-intelligence-platform.git
cd it-asset-intelligence-platform
## 🔗 API Documentation

Swagger UI available at:

http://127.0.0.1:8000/docs
