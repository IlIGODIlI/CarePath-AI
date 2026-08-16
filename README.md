# 🩺 CarePath AI

<p align="center">
  <img src="images/logo.png" alt="CarePath AI Logo" width="180">
</p>

## Autonomous Healthcare Navigation System

> Right Guidance. Right Specialist. Right Time.

CarePath AI is an intelligent healthcare navigation platform designed to reduce diagnostic delays and help patients reach the most appropriate specialist faster. Instead of replacing doctors, CarePath AI acts as a healthcare navigation companion that analyzes symptoms, medical records, diagnostic reports, and treatment history to guide patients through their healthcare journey.

The platform combines Computer Vision, Natural Language Processing, Machine Learning, Retrieval-Augmented Generation (RAG), and a Multi-Agent Architecture to provide explainable, patient-centered healthcare recommendations.

---

## 🚀 Project Objectives

CarePath AI is designed to:

- Reduce diagnostic delays in healthcare.
- Guide patients toward the most appropriate specialist.
- Analyze symptoms, prescriptions, reports, and medical records.
- Detect patterns of ineffective treatments and referral needs.
- Provide explainable AI-generated healthcare insights.
- Help patients prepare for consultations.
- Support continuous care through monitoring and follow-ups.
- Improve healthcare accessibility through intelligent navigation.

---

## ❗ Problem Statement

Many patients spend months—or even years—searching for the correct diagnosis.

Common challenges include:

- Visiting multiple doctors before reaching the correct specialist.
- Undergoing repeated or unnecessary diagnostic tests.
- Difficulty understanding prescriptions and medical reports.
- Lack of visibility into their healthcare journey.
- Delayed referrals and fragmented care pathways.
- Poor follow-up and treatment adherence.

CarePath AI addresses these challenges by creating a structured, explainable, and intelligent healthcare navigation experience.

---

## 💡 Why CarePath AI Exists

Healthcare information is often scattered across reports, prescriptions, imaging scans, consultation notes, and laboratory results.

Patients frequently struggle to:

- Understand their medical information.
- Track treatment progress.
- Know when a treatment plan is not working.
- Determine which specialist they should consult next.

CarePath AI brings all healthcare information together and transforms it into actionable guidance through AI-driven clinical reasoning and healthcare navigation.

---

# 🏗 Architecture Overview

CarePath AI follows a Multi-Agent AI Architecture.

```text
Patient Input
      │
      ▼
 Intake Agent
      │
      ▼
 Medical Records Agent
      │
      ▼
 Vision Agent
      │
      ▼
 Clinical Reasoning Agent
      │
      ▼
 Referral Agent
      │
      ▼
 Safety Agent
      │
      ▼
 Follow-Up Agent
      │
      ▼
 Patient Dashboard
```

### Core AI Agents

| Agent | Responsibility |
|---------|---------------|
| Intake Agent | Collects and structures patient symptoms |
| Vision Agent | Analyzes uploaded medical images |
| Medical Records Agent | Extracts information from reports and prescriptions |
| Clinical Reasoning Agent | Performs healthcare reasoning |
| Referral Agent | Identifies appropriate specialists |
| Safety Agent | Detects risks and safety concerns |
| Follow-Up Agent | Tracks care progress and future actions |
| Evidence Agent | Retrieves supporting medical evidence using RAG |

---

# 📱 Platform Features

## 🌐 Landing Page

The landing page introduces CarePath AI and explains how the platform assists patients throughout their healthcare journey.

![Landing Page](images/landing-page.png)

---

## 🔐 Login & Authentication

Secure authentication system for accessing patient healthcare information.

![Login Page](images/login-page.png)

---

## 📊 Dashboard

The dashboard serves as the command center of the platform.

Features include:

- Continuous Care Plan
- Symptom Monitoring
- Medication Reminders
- Recent Activity Tracking
- Healthcare Milestones
- Next Recommended Actions

![Dashboard](images/dashboard.png)

---

## 🛤 My Care Journey

Provides a timeline-based view of the patient's healthcare progression.

Features:

- Healthcare milestones
- Diagnostic history
- Timeline inspection
- Progress tracking
- Event exploration

![Care Journey](images/care-journey.png)

---

## 🤖 AI Analysis

Displays AI-generated clinical insights and healthcare reasoning.

Features:

- Clinical Findings
- Risk Assessment
- Safety Evaluation
- Specialist Recommendations
- Supporting Evidence

![AI Analysis](images/ai-analysis.png)

---

## 📂 Upload Center

Centralized document upload system.

Supports:

- Medical Reports
- Prescriptions
- Lab Reports
- Imaging Results
- Consultation Documents

![Upload Center](images/upload-center.png)

---

## 📑 My Records

Unified patient record management system.

Features:

- Health Records
- Visit History
- Medical Documents
- Treatment History

![My Records](images/my-records.png)

---

## 💊 Medications

Medication management and adherence tracking.

Features:

- Medication Schedule
- Dosage Tracking
- Reminders
- Adherence Monitoring

![Medications](images/medications.png)

---

## 🔄 Follow-Up Center

Continuous healthcare monitoring and reassessment.

Features:

- Follow-Up Tasks
- Progress Tracking
- Reassessment Logs
- Health Checkpoints

![Follow Up](images/follow-up.png)

---

## 👨‍⚕️ Dr Bridge

Bridges communication between AI insights and healthcare professionals.

Features:

- Consultation Preparation
- Question Generation
- Clinical Summaries
- Appointment Assistance

![Doctor Bridge](images/doctor-bridge.png)

---

# 🔬 AI Workflow

```text
Patient Symptoms
        │
        ▼
Symptom Intake
        │
        ▼
Medical Record Analysis
        │
        ▼
Image Analysis
        │
        ▼
Clinical Reasoning
        │
        ▼
Evidence Retrieval (RAG)
        │
        ▼
Specialist Recommendation
        │
        ▼
Care Plan Generation
        │
        ▼
Continuous Follow-Up
```

---

# ⚙ Backend Architecture

The backend is built using FastAPI and follows a modular architecture.

### Components

- FastAPI API Layer
- Authentication Services
- Clinical Services
- Patient Services
- Medical Record Services
- AI Integration Layer
- Agent Orchestration Layer

### Backend Technologies

- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Bcrypt Password Hashing
- Structlog Logging

---

# 🗄 Database Architecture

The database layer uses PostgreSQL with Supabase Storage integration.

### Database Components

- PostgreSQL Database
- SQLAlchemy ORM
- Supabase Storage
- CRUD Layer
- Audit Logging
- Relationship Management

### Core Tables

- Users
- PatientProfile
- MedicalFiles
- SymptomSessions
- PatientSymptoms
- AIAnalysis
- Recommendations
- CarePlans
- FollowUps
- Notifications
- Medications
- Visits
- FamilyMembers
- Feedback
- AuditHistory
- AgentRuns
- TimelineEvents
- EvidenceRetrieval

---

# 🔄 End-to-End Data Flow

```text
Patient Input
      │
      ▼
Symptom Collection
      │
      ▼
Medical Record Processing
      │
      ▼
AI Clinical Analysis
      │
      ▼
Evidence Retrieval
      │
      ▼
Specialist Recommendation
      │
      ▼
Care Plan Creation
      │
      ▼
Patient Dashboard
      │
      ▼
Continuous Follow-Up
```

---

# 🛠 Local Setup

### Clone Repository

```bash
git clone <repository-url>
cd CarePath-AI
```

### Install Frontend

```bash
npm install
npm run dev
```

### Install Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

# 🔐 Environment Variables

Create a `.env` file.

```env
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
JWT_SECRET_KEY=
```

Never commit `.env` files or credentials.

---

# 🛡 Security

- JWT Authentication
- Password Hashing using Bcrypt
- Secure Environment Variables
- Audit Logging
- Role-Based Access Control
- Protected API Endpoints

---

# 🧰 Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | React |
| Language | TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Backend | FastAPI |
| Database | PostgreSQL |
| Storage | Supabase |
| ORM | SQLAlchemy |
| Authentication | JWT |
| AI | NLP, Computer Vision, RAG |
| Logging | Structlog |

---

# 🏆 Achievements

- Built an Autonomous Healthcare Navigation Platform.
- Implemented a Multi-Agent AI Architecture.
- Developed an intelligent healthcare journey system.
- Integrated document and report analysis.
- Added AI-powered clinical reasoning.
- Implemented specialist referral recommendations.
- Developed continuous care and follow-up workflows.
- Built an explainable AI evidence retrieval system.

---

# 🚀 Future Improvements

- Real-time healthcare monitoring.
- Voice-based symptom intake.
- Wearable device integration.
- Hospital and EHR integrations.
- Multilingual healthcare support.
- Advanced predictive healthcare analytics.
- Personalized treatment pathway recommendations.

---

# 👥 Contributors

| Role | Team |
|--------|--------|
| Frontend Development | CarePath Team |
| Backend Development | CarePath Team |
| Database Engineering | CarePath Team |
| AI Development | CarePath Team |
| Documentation | CarePath Team |

---

# 📜 License & Disclaimer

CarePath AI is intended for healthcare navigation and educational support.

The platform does **not replace licensed medical professionals** and should not be used as a substitute for professional medical advice, diagnosis, or treatment.

---

# 📌 Project Status

```text
Status: Active Development

Frontend: Implemented
Backend: In Progress
Database: Implemented
AI Agents: In Development
Healthcare Navigation System: Active
```

Made with ❤️ by the CarePath AI Team.