# 🩺 CarePath AI

> **Autonomous Healthcare Navigation System**

CarePath AI is an autonomous multi-agent healthcare navigation platform designed to help patients move through the healthcare system with the **right guidance, the right specialist, at the right time**.

The platform focuses on reducing diagnostic delay by connecting patient symptoms, medical records, uploaded documents, AI analysis, evidence retrieval, specialist recommendations, care planning, and follow-up into one connected healthcare journey.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [AI Multi-Agent Architecture](#-ai-multi-agent-architecture)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Database Architecture](#-database-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Backend Setup](#-backend-setup)
- [Frontend Setup](#-frontend-setup)
- [Database Setup](#-database-setup)
- [Security](#-security)
- [Testing](#-testing)
- [Future Scope](#-future-scope)
- [Disclaimer](#-disclaimer)
- [Team](#-team)

---

## 🌟 Overview

Healthcare journeys are often fragmented. A patient may experience symptoms, visit multiple doctors, undergo repeated tests, try different treatments, and still struggle to understand what should happen next.

**CarePath AI** addresses this navigation problem by creating a connected healthcare pathway around the patient.

Instead of acting as a simple chatbot, CarePath AI uses a **multi-agent architecture** to process different types of healthcare information and coordinate the next steps.

The system can work with symptoms, medical records, prescriptions, laboratory reports, medical documents, medical images, previous consultations, treatment history, and follow-up information.

---

## 🎯 Problem Statement

Patients can face significant delays before reaching the appropriate specialist.

Common problems include:

- Visiting multiple doctors before reaching the right specialist
- Repeating medical tests
- Losing important medical history between consultations
- Difficulty understanding medical documents
- Treatment failure without identifying the underlying pattern
- Lack of continuity between consultations
- Uncertainty about what to do next

This fragmentation can contribute to **diagnostic delay** and an inefficient healthcare journey.

---

## 💡 Our Solution

CarePath AI acts as an **Autonomous Healthcare Navigator**.

The platform brings together:

**Patient Input → Medical Data → AI Analysis → Evidence → Referral → Care Plan → Follow-up**

The objective is not to replace clinicians, but to improve healthcare navigation, continuity, and preparation while reducing unnecessary delays.

---

# ✨ Key Features

## 🏠 Patient Dashboard

A centralized view of the patient's current healthcare journey, including:

- Continuous care plan
- Current goals
- Medication reminders
- Symptom follow-up check-ins
- Latest milestones
- Recent actions
- Next actions
- Consultation information

## 🧭 My Care Journey

A chronological view of important healthcare events, including symptoms, consultations, medical records, AI analysis, recommendations, care plans, and follow-ups. Individual timeline events can be inspected for additional detail.

## 🤖 AI Analysis

The AI Analysis module brings together patient information and AI-generated clinical reasoning. It can provide clinical findings, risk assessment, differential information, confidence information, explainable reasoning, evidence-backed insights, healthcare advisory information, and safety assessment.

## 📤 Upload Center

Allows patients to provide medical documents for processing through an **Upload → Extraction → Analysis → Structured Medical Information** workflow. The platform can generate an **AI Clinical Extraction Report** from uploaded information.

## 📁 My Records

A centralized location for medical documents, consultation records, symptoms, medications, previous healthcare events, extracted information, and medical history.

## 🔄 Follow-up

Supports follow-up reminders, checkpoints, reassessments, follow-up history, care-plan progress, and relevant notes.

## 👨‍⚕️ Dr. Bridge

Designed to bridge the gap between patients and healthcare professionals by helping organize information required during consultations.

---

# 🧠 AI Multi-Agent Architecture

CarePath AI is designed as a **multi-agent system rather than a traditional chatbot**.

| Agent | Responsibility |
|---|---|
| **Intake Agent** | Collects and structures patient symptoms and initial information |
| **Vision Agent** | Processes relevant medical images |
| **Medical Records Agent** | Understands and organizes medical records and documents |
| **Clinical Reasoning Agent** | Identifies patterns and generates structured clinical reasoning |
| **Referral Agent** | Determines appropriate specialist direction and referral urgency |
| **Follow-up Agent** | Tracks care-plan progress and follow-up requirements |
| **Safety Agent** | Provides safety checks and healthcare advisories |

### Evidence Agent

A **RAG-powered Evidence Agent** retrieves relevant evidence to support AI-generated insights and improve explainability.

---

# 🏗 System Architecture

```text
                    ┌─────────────────────┐
                    │       Patient       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Patient Intake    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌──────────────┐
       │  Symptoms  │   │   Records  │   │ Medical      │
       │            │   │ & Reports  │   │ Images       │
       └──────┬─────┘   └──────┬─────┘   └──────┬───────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │    AI Agent Layer   │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │ Clinical   │    │  Evidence  │    │   Safety   │
      │ Reasoning  │    │    RAG     │    │   Agent    │
      └──────┬─────┘    └──────┬─────┘    └──────┬─────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                     ┌────────────────────┐
                     │ Referral & Care    │
                     │       Plan         │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │ Follow-up &        │
                     │ Continuous Care    │
                     └────────────────────┘
```

---

# 🛠 Technology Stack

### Frontend

- React
- TypeScript
- Vite

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.0
- JWT authentication
- Bcrypt password hashing
- Structlog

### Database

- PostgreSQL
- Supabase
- SQLAlchemy 2.0
- UUID-based identifiers

### Storage

- Supabase Storage for medical documents and binary files

### AI / Intelligence

- Multi-agent architecture
- LangGraph-based orchestration
- Retrieval-Augmented Generation (RAG)
- Computer Vision
- Natural Language Processing
- Machine Learning

---

# 🗄 Database Architecture

The database acts as the central system for patient information, medical history, symptoms, AI outputs, recommendations, care plans, and system activity.

### PostgreSQL Flow

```text
[ FastAPI Application ]
          ↓
[ CRUD Modules ]
          ↓
[ SQLAlchemy Models ]
          ↓
[ PostgreSQL ]
```

### Supabase Storage Flow

```text
[ User Uploads File ]
          ↓
[ FastAPI receives File ]
          ↓
[ Supabase Storage ]
          ↓
[ Metadata saved to PostgreSQL ]
          ↓
[ AI Processing Pipeline ]
```

PostgreSQL stores structured information and metadata, while Supabase Storage stores binary medical files.

## Core Database Entities

1. **Users**
2. **PatientProfile**
3. **MedicalFiles**
4. **SymptomSessions**
5. **PatientSymptoms**
6. **AIAnalysis**
7. **Recommendations**
8. **CarePlans**
9. **FollowUps**
10. **Notifications**
11. **Medications**
12. **Visits**
13. **FamilyMembers**
14. **Feedback**
15. **AuditHistory**
16. **PromptTemplates**
17. **AgentRuns**
18. **TimelineEvents**
19. **EvidenceRetrieval**

### Entity Relationships

```text
Users
 ├── PatientProfile
 ├── MedicalFiles
 ├── SymptomSessions
 │     └── PatientSymptoms
 ├── Visits
 ├── TimelineEvents
 └── AIAnalysis
        ├── Recommendations
        ├── CarePlans
        │     └── FollowUps
        └── EvidenceRetrieval
```

---

# 📂 Project Structure

```text
CarePath-AI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   └── services/
│   ├── requirements.txt
│   └── .env.example
│
├── database/
│   ├── __init__.py
│   ├── connections.py
│   ├── models.py
│   ├── storage.py
│   ├── test_database.py
│   └── crud/
│       ├── __init__.py
│       ├── utils.py
│       ├── user_crud.py
│       ├── clinical_crud.py
│       ├── ai_crud.py
│       └── system_crud.py
│
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

- Git
- Node.js and npm
- Python 3
- PostgreSQL / Supabase access
- Required environment variables

## ⚙️ Backend Setup

```bash
cd backend
python -m venv venv
```

### Windows

```bash
venv\\Scripts\\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

Run the development server:

```bash
uvicorn app.main:app --reload --port 8000
```

## 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Vite will provide the local development URL in the terminal.

## 🗃 Database Setup

Configure the required environment variables:

```text
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
```

Never commit real credentials to the repository.

---

# 🧪 Testing

The database repository includes an end-to-end test script.

```bash
python -m database.test_database
```

The tests cover:

- Database connectivity
- CRUD operations
- Transaction handling
- Supabase Storage operations
- Cleanup after testing

### Demo Upload Flow

The database layer includes a demo upload workflow demonstrating local test file generation, database setup, Supabase Storage upload, PostgreSQL metadata creation, and cleanup.

```bash
python demo_upload_flow.py
```

---

# 🔐 Security

CarePath AI follows security practices appropriate for a healthcare-oriented application.

### Authentication

- Bcrypt password hashing
- JWT-based authentication
- Environment-based configuration

### Database

- UUID identifiers
- PostgreSQL access controls
- SQLAlchemy ORM
- Transaction handling
- Audit history

### Storage

Medical files are separated from relational data and stored through Supabase Storage.

### Environment Variables

Never commit `.env` files containing database URLs, Supabase keys, JWT secrets, or other credentials.

---

# 🧩 CRUD Layer

| Module | Responsibility |
|---|---|
| `user_crud.py` | Users, patient profiles, family links |
| `clinical_crud.py` | Visits, files, symptoms, medications |
| `ai_crud.py` | Analysis, recommendations, care plans, follow-ups |
| `system_crud.py` | Notifications, timelines, audits |
| `utils.py` | Generic CRUD and transaction utilities |

---

# 🔎 Evidence & Explainability

The RAG-based evidence layer is designed to support explainable AI outputs.

The pipeline can:

1. Retrieve relevant evidence
2. Associate evidence with an AI run
3. Store evidence metadata
4. Support explainable recommendations

The `EvidenceRetrieval` entity stores evidence associated with agent execution.

---

# 🧾 Auditability

CarePath AI includes structures for tracking AI and system activity:

- `AuditHistory`
- `AgentRuns`
- `PromptTemplates`
- `EvidenceRetrieval`

These can capture information such as agent execution, model version, prompt version, execution time, token usage, retrieved evidence, system actions, errors, and status.

AI-generated reasoning is designed to remain largely immutable to support traceability.

---

# 🔄 Healthcare Navigation Workflow

```text
Patient
   ↓
Initial Symptoms / Intake
   ↓
Medical Records & Documents
   ↓
AI Processing
   ↓
Clinical Reasoning
   ↓
Evidence Retrieval
   ↓
Safety Assessment
   ↓
Referral Recommendation
   ↓
Specialist Direction
   ↓
Personalized Care Plan
   ↓
Follow-up
   ↓
Continuous Care Journey
```

---

# 🏥 Healthcare Philosophy

> **The system should help patients navigate healthcare — not replace healthcare professionals.**

CarePath AI is intended to organize healthcare information, reduce fragmentation, improve continuity, support specialist navigation, explain AI-generated insights, help patients prepare for consultations, and track follow-up requirements.

Clinical decisions remain the responsibility of qualified healthcare professionals.

---

# 🔮 Future Scope

The architecture can support future improvements such as:

- Advanced AI agent orchestration
- Expanded medical vision capabilities
- Improved evidence retrieval
- More healthcare integrations
- Database indexing
- Redis-based caching
- Database partitioning
- Automated point-in-time backups
- Performance monitoring
- Expanded clinical workflows
- Additional patient and provider tools

---

# 🧑‍💻 Development Principles

- Keep application modules modular
- Separate business logic from database operations
- Use SQLAlchemy for database interaction
- Avoid raw SQL where possible
- Use UUIDs for identifiers
- Use timezone-aware timestamps
- Keep binary files in object storage
- Maintain auditability for AI operations
- Keep sensitive credentials outside source control
- Test database and storage workflows during development

---

# 🐛 Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Database connection failure | Incorrect database configuration | Verify `DATABASE_URL` |
| Supabase connection failure | Incorrect Supabase configuration | Verify `SUPABASE_URL` and `SUPABASE_KEY` |
| `ModuleNotFoundError` | Incorrect Python execution path | Run database scripts as modules |
| Storage failure | Storage configuration or permissions | Check Supabase Storage settings |
| Missing environment variables | `.env` not configured | Create and configure `.env` |

---

# 🗺️ Project Status

### Current Foundation

- ✅ Frontend application
- ✅ Backend foundation
- ✅ Database architecture
- ✅ PostgreSQL / Supabase integration
- ✅ Supabase Storage integration
- ✅ Patient healthcare journey
- ✅ AI analysis interface
- ✅ Medical record management
- ✅ Upload workflow
- ✅ Follow-up workflow
- ✅ Multi-agent architecture
- ✅ Evidence retrieval architecture
- ✅ Audit and agent execution structures

The project continues to evolve as additional AI and healthcare navigation capabilities are integrated.

---

# 👥 Team

**CarePath AI Engineering Team**

Built as part of the **NIT Delhi Hackathon**.

---

# ⚠️ Disclaimer

CarePath AI is a healthcare navigation and decision-support project.

It is **not a replacement for a qualified medical professional, medical diagnosis, or emergency medical care**.

AI-generated information should be reviewed by appropriate healthcare professionals before being used for clinical decision-making.

---

# ❤️ CarePath AI

### **Right Guidance. Right Specialist. Right Time.**

Built to make the healthcare journey more connected, understandable, and patient-centered.
