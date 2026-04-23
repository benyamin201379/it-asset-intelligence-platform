# IT Asset Intelligence Platform

A full-stack application for managing IT assets, analyzing system dependencies, and calculating operational risk.

---

##  Overview

Modern IT systems are highly interconnected.  
This project models IT assets and their relationships to:

- track dependencies between systems
- identify cascading failures
- estimate operational risk

It combines a FastAPI backend with a lightweight JavaScript frontend dashboard.

---

## 🧠 Key Features

- Full CRUD operations for IT assets
- Relationship management between systems
- Dependency tracking
- Impact analysis (cascading effects)
- Risk scoring based on:
  - asset criticality
  - number of dependencies
- Interactive dashboard with:
  - search functionality
  - visual asset cards
  - dynamic risk display

---

##  Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite

### Frontend
- HTML
- CSS
- JavaScript (Vanilla)

---

##  API Endpoints

### Assets
- `GET /assets`
- `POST /assets`
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

---

##  Example Use Case

A typical scenario:

- A web application depends on an API server  
- The API server depends on a database  
- The database depends on storage  

 If one component fails, all dependent systems can be identified  
 A risk score is calculated automatically  

This simulates real-world infrastructure dependency analysis.

---

##  Frontend Dashboard

Features:
- Search assets by name
- Visual cards for each asset
- Color-coded criticality:
  -  High
  -  Medium
  -  Low
- Click on asset → show risk score & dependencies

---

## Run Locally

### 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/it-asset-intelligence-platform.git
cd it-asset-intelligence-platform
