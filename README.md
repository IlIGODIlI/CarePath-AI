# CarePath AI - Backend & Multi-Agent Engine Architecture

CarePath AI is an **Autonomous Healthcare Navigation Platform**. It does not diagnose diseases; instead, it helps patients navigate the healthcare system by understanding symptoms, medical images, lab reports, and prescriptions, recommending appropriate specialists with explainable evidence, and providing continuous follow-up.

---

## Technical Stack
- **API Framework**: FastAPI (Async Python 3.11+)
- **Multi-Agent Orchestrator**: LangGraph
- **Relational DB**: PostgreSQL (SQLAlchemy AsyncEngine + Alembic)
- **Vector DB**: ChromaDB
- **Structured Logging**: `structlog` (JSON format)
- **Containerization**: Docker & Docker Compose

---

## Project Directory Topology

```
c:\Users\Dell\Downloads\New folder\
├── pyproject.toml               # Dependency & Package configuration
├── .env.example                 # Environment variables template
├── docker-compose.yml           # Multi-container orchestration (FastAPI, Postgres, ChromaDB, Redis)
├── docker/
│   └── Dockerfile.dev           # Development Container Setup
├── src/
│   ├── main.py                  # FastAPI Application Lifespan & Entrypoint
│   ├── config.py                # Pydantic BaseSettings management
│   ├── api/                     # API Routers & Controllers
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── encounters.py# Triage Session & SSE Streaming Progress Endpoints
│   │       │   └── health.py    # Diagnostics & Liveness probe
│   │       └── router.py
│   ├── core/                    # Domain Core, Exceptions, Logging
│   ├── schemas/                 # Pydantic DTOs & Validation Schemas
│   ├── services/
│   │   └── ai_contracts/        # Abstract Interfaces & Mock Stubs for AI Teammate
│   └── agents/                  # LangGraph Multi-Agent Engine
│       ├── state.py             # CarePathState Schema (TypedDict)
│       ├── router.py            # Supervisor Agent Dynamic Router
│       ├── graph.py             # Compiled LangGraph StateGraph
│       └── nodes/               # Individual Agent Nodes (Supervisor, Safety, Intake...)
└── tests/                       # Pytest Suite
```

---

## Quickstart Setup

### Option 1: Running with Docker Compose (Recommended)
```bash
docker-compose up --build
```
Access points:
- **FastAPI OpenAPI Interactive Docs**: http://localhost:8000/docs
- **Health Probe**: http://localhost:8000/api/v1/health

### Option 2: Local Python Environment
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -e .[dev]
uvicorn src.main:app --reload
```

---

## Testing the Multi-Agent Triage Engine

### 1. Initialize a Navigation Encounter Session
```bash
curl -X POST "http://localhost:8000/api/v1/encounters" \
  -H "Content-Type: application/json" \
  -d '{
    "chief_complaint": "Severe crushing chest pain radiating to left arm for 15 minutes",
    "symptoms_severity": 10
  }'
```

### 2. Trigger Asynchronous LangGraph Processing
```bash
curl -X POST "http://localhost:8000/api/v1/encounters/enc_<ID>/process"
```

### 3. Stream Real-time Agent Progress (SSE)
```bash
curl -N "http://localhost:8000/api/v1/encounters/enc_<ID>/stream"
```
