<div align="center">
  <img src="images/carepath-ai-logo.png" alt="CarePath AI Logo" width = "220"/>
  <h1>CarePath AI</h1>
  <p><b>AI-Powered Clinical Intelligence & Continuity-of-Care Platform</b></p>

  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pydantic-Structured_AI-E92063?style=flat-square&logo=pydantic&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F00?style=flat-square"/>
  <img src="https://img.shields.io/badge/EasyOCR-OCR-4285F4?style=flat-square"/>
  <img src="https://img.shields.io/badge/PyTorch-Computer_Vision-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pytest-177_Passed-2EA44F?style=flat-square&logo=pytest"/>
</div>

<br />

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#key-features">Key Features</a> ·
  <a href="#technology-stack">Tech Stack</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#core-modules">Core Modules</a> ·
  <a href="#key-metrics">Key Project Metrics</a> ·
  <a href="#getting-started">Getting Started</a> ·
  <a href="#testing">Testing</a> ·
  <a href="#safety">Safety</a>
</p>

<a id="overview"></a>

Overview

CarePath AI is an autonomous multi-agent healthcare navigation platform designed to help patients move from symptoms and medical records toward the appropriate specialist, evidence-backed clinical context, care preparation, and follow-up.

Instead of building another medical chatbot, the system is designed around a multi-agent healthcare journey. It combines Computer Vision, Clinical NLP, OCR, RAG, embeddings, clinical extraction, patient memory, timeline analysis, treatment-response intelligence, referral ranking, personalized care planning, and follow-up orchestration.

The core problem being addressed is diagnostic and navigation delay: patients may visit multiple doctors, repeat tests, struggle to understand medical documents, or fail to connect symptoms and treatment history across consultations. CarePath AI is intended to organize that information and guide the patient through the healthcare system rather than replace clinicians.

The original CarePath architecture defines the system as a healthcare-navigation platform using Computer Vision, NLP, Machine Learning, and RAG, with specialized agents collaborating through a central workflow. fileciteturn6file4L470-L478

Real Time CarePath Login / Dashboard

<p align="center">
  <img src="images/LOGIN-PAGE(README).jpeg" width="100%">
</p>

Replace the image above with the final CarePath product screenshot available in the repository.

<a id="key-features"></a>

✨ Key Features

Capability

What it enables

AI-powered patient intake

Structures symptoms, severity, duration, and patient context before downstream processing.

Medical document intelligence

OCR and clinical extraction for prescriptions, laboratory reports, clinical notes, and other medical documents.

Medical computer vision

Processes medical images and DICOM-compatible inputs and returns structured visual findings and confidence information.

Clinical NLP / Bio-NER

Extracts symptoms, medications, diagnoses, anatomy, procedures, and laboratory-related entities with negation awareness.

Evidence-based RAG

Retrieves relevant clinical guideline content from ChromaDB and returns evidence/source information.

Clinical timeline

Organizes patient events, symptoms, records, treatments, and consultations chronologically.

Clinical reasoning

Combines structured patient information, evidence, and previous outputs to form navigation-oriented clinical insights.

Specialist referral

Ranks appropriate specialties and provides confidence, reasoning, urgency, and doctor-discussion context.

Personalized care planning

Converts patient context into structured preparation, monitoring, action, and follow-up guidance.

Treatment-response intelligence

Identifies documented improvement, worsening, mixed response, stability, or insufficient evidence.

CarePath Memory

Retains clinically relevant information for continuity across the patient's healthcare journey.

Follow-up intelligence

Identifies unresolved issues, monitoring requirements, and follow-up needs.

AI safety layer

Includes structured validation, confidence handling, prompt-injection protection concepts, PHI redaction, and a strict medication boundary.

<a id="technology-stack"></a>

🧰 Technology Stack

Layer

Technologies

Frontend

React 19, TypeScript, Vite, React Router, Tailwind CSS

User Experience

Motion, Lucide React, interactive architecture views

Backend API

Python, FastAPI, Uvicorn, Pydantic

AI Orchestration

LangGraph, Supervisor + specialized agent architecture

AI / Language

Gemini-compatible model integration, Clinical NLP, Bio-NER

OCR

EasyOCR, Tesseract-compatible OCR pipeline

Computer Vision

PyTorch, TorchVision, NumPy, Pillow

Medical Imaging

DICOM / pydicom-compatible processing

RAG / Retrieval

ChromaDB, embeddings, guideline retrieval

Data Layer

PostgreSQL, Supabase, SQLAlchemy

File Storage

Supabase Storage

Security

JWT, password hashing, PHI redaction, prompt-injection defenses

Testing

Pytest, integration tests, interface tests, AI-service tests

Deployment

Docker, Docker Compose

The CarePath team architecture originally specifies React + Tailwind for the frontend, FastAPI for the backend, PostgreSQL + ChromaDB for data, n8n/LangGraph-style orchestration, Gemini/OpenAI + OCR + Computer Vision for AI, and Docker-based deployment. fileciteturn6file8L971-L977

flowchart LR
    UI[React CarePath Console] --> API[FastAPI API Gateway]
    UI --> AGENTS[Multi-Agent Workflow]

    API --> AUTH[Authentication & RBAC]
    API --> CORE[Core Patient Services]
    API --> AI[AI Intelligence Layer]

    AGENTS --> SAFETY[Safety Agent]
    AGENTS --> INTAKE[Intake Agent]
    AGENTS --> VISION[Vision Agent]
    AGENTS --> DOCS[Medical Docs Agent]
    AGENTS --> TIMELINE[Timeline Agent]
    AGENTS --> EVIDENCE[Evidence Agent]
    AGENTS --> REASONING[Clinical Reasoning]
    AGENTS --> REFERRAL[Referral Agent]
    AGENTS --> CAREPLAN[Care Plan Agent]
    AGENTS --> FOLLOWUP[Follow-up Agent]

    AI --> OCR[OCR]
    AI --> NLP[Clinical NLP]
    AI --> CV[Computer Vision]
    AI --> RAG[RAG / Embeddings]

    CORE --> PG[(PostgreSQL / Supabase)]
    CORE --> STORAGE[Supabase Storage]
    RAG --> CHROMA[(ChromaDB)]

The project is organized into four major operational domains so that the AI, healthcare-navigation, data, and product layers remain modular and maintainable.

<a id="architecture"></a>

🏗️ Architecture & Domain Deep-Dive

🧠 1. Artificial Intelligence (AI) Domain

The AI domain acts as the clinical intelligence layer powering document understanding, medical image analysis, evidence retrieval, structured extraction, and CarePath synthesis.

Feature

Technical Breakdown & Capability

📄 Smart Document Analysis

OCR extracts medical text and downstream services structure prescriptions, laboratory metrics, clinical notes, and document metadata.

🧬 Clinical Bio-NER

Identifies symptoms, medications, diagnoses, anatomy, procedures, and laboratory-related entities, including negation and confidence.

🩻 Medical Computer Vision

Parses standard images/DICOM-compatible inputs and produces structured findings, pathology scores, metadata, and explainability output.

📚 Medical RAG

Uses ChromaDB and an embedding/retrieval layer to retrieve relevant clinical guideline evidence and source information.

🧠 Clinical Synthesis

Combines OCR, NLP, Vision, and RAG outputs into a structured CarePath clinical context.

📊 Clinical Intelligence

Supports confidence scoring, treatment-response classification, referral ranking, follow-up intelligence, and personalized care-plan generation.

The original CarePath AI/ML ownership explicitly covers Computer Vision, NLP, OCR, RAG, treatment-failure detection, referral ranking, confidence scoring, explainable AI, and AI inference APIs. fileciteturn6file6L721-L788

<br>

🤖 2. Multi-Agent Healthcare Navigation Domain

The multi-agent layer transforms individual AI capabilities into an autonomous healthcare-navigation workflow.

flowchart TD
    SUP[Supervisor Agent]

    SUP --> SAFETY[Safety Agent]
    SUP --> INTAKE[Intake Agent]
    SUP --> VISION[Vision Agent]
    SUP --> DOCS[Medical Docs Agent]
    SUP --> TIMELINE[Timeline Agent]
    SUP --> EVIDENCE[Evidence Agent]
    SUP --> REASONING[Clinical Reasoning Agent]
    SUP --> REFERRAL[Referral Agent]
    SUP --> CAREPLAN[Care Plan Agent]
    SUP --> FOLLOWUP[Follow-up Agent]

    SAFETY -->|Safe| INTAKE
    SAFETY -->|Emergency| EXIT[Emergency / Short Circuit]

    INTAKE --> TIMELINE
    VISION --> TIMELINE
    DOCS --> TIMELINE

    TIMELINE --> EVIDENCE
    EVIDENCE --> REASONING
    REASONING --> REFERRAL
    REFERRAL --> CAREPLAN
    CAREPLAN --> FOLLOWUP

The project architecture defines 11 specialized agents: Supervisor, Intake, Vision, Medical Docs, Timeline, Evidence, Clinical Reasoning, Referral, Safety, Care Plan, and Follow-up. fileciteturn6file8L978-L989

Agent responsibilities

Agent

Responsibility

Supervisor Agent

Controls routing and decides which agent should execute next.

Safety Agent

Detects red flags and urgent conditions.

Intake Agent

Processes symptoms and patient information.

Vision Agent

Analyzes medical images.

Medical Docs Agent

Extracts information from reports and prescriptions.

Timeline Agent

Builds the patient's medical journey.

Evidence Agent

Retrieves relevant medical guidelines through RAG.

Clinical Reasoning Agent

Combines evidence and patient context into clinical insights.

Referral Agent

Recommends and ranks specialists.

Care Plan Agent

Prepares the patient for the next stage of care.

Follow-up Agent

Monitors progress and schedules follow-up intelligence.

🗄️ 3. Data, Memory & Evidence Domain

The data domain preserves structured patient history while separating medical files, relational records, longitudinal memory, and vector evidence.

flowchart LR
    APP[CarePath Application]

    APP --> CRUD[Domain CRUD Layer]
    CRUD --> ORM[SQLAlchemy]
    ORM --> PG[(PostgreSQL / Supabase)]

    APP --> FILES[Storage Service]
    FILES --> OBJECT[(Supabase Storage)]

    APP --> MEMORY[CarePath Memory]
    MEMORY --> PG

    AI[AI / Evidence Layer] --> EMB[Embedding Service]
    EMB --> CHROMA[(ChromaDB)]

Data responsibilities

Layer

Purpose

PostgreSQL / Supabase

Structured users, patients, visits, symptoms, medications, analyses, recommendations, care plans, follow-ups, feedback, timelines, and audit records.

Supabase Storage

Medical reports, prescriptions, images, PDFs, and other uploaded files.

ChromaDB

Vector-based clinical guideline/evidence retrieval.

CarePath Memory

Longitudinal clinical information used across summaries, timelines, treatment response, and follow-up.

Audit / Agent Runs

Traceability for AI and multi-agent execution.

The repository's database design includes a PostgreSQL/Supabase relational layer, Supabase Storage for medical files, ChromaDB for evidence retrieval, and domain-specific CRUD modules.

👤 4. Patient Experience & Continuity Domain

The patient domain turns AI outputs into a continuous healthcare journey instead of a single isolated AI response.

Feature

Technical Breakdown & Capability

📝 Patient Intake

Captures symptoms, duration, severity, and relevant context.

📋 Patient Summary

Consolidates extracted and verified clinical information into a structured overview.

❓ Doctor Questions

Generates case-specific questions for the next consultation.

🧠 CarePath Memory

Retains clinically relevant information for future retrieval.

📅 Patient Timeline

Organizes clinical events chronologically.

📈 Treatment Response

Tracks documented improvement, worsening, mixed response, or insufficient information.

⏰ Follow-up Intelligence

Identifies unresolved issues and future checkpoints.

📋 Personalized Care Plan

Organizes action items, monitoring, appointment preparation, and questions for clinicians.

The original project plan explicitly defines patient dashboard, doctor recommendations, timeline, analytics, medical-report/prescription/image uploads, confidence, evidence, history, charts, progress, and notifications as key product experiences. fileciteturn6file6L661-L720

<br>

<a id="core-modules"></a>

🚀 Core Modules

Module

Technology / Approach

Current Implementation

Planned Evaluation

Smart Document Analyzer

EasyOCR + structured Pydantic schemas

OCR extraction, document type, prescriptions, laboratory metrics, text lines, confidence and processing time.

OCR accuracy, field extraction accuracy, confidence calibration

Clinical NLP / Bio-NER

Pattern-based medical entity extraction + coding maps

Symptoms, medications, diagnoses, anatomy, negation, confidence, ICD-10/SNOMED metadata.

Entity precision/recall, negation accuracy, coding correctness

Medical Vision

PyTorch/TorchVision + image processing

DICOM parsing, metadata extraction, image normalization, pathology scores and explainability output.

Classification quality, robustness, confidence, explainability

Medical RAG

Embeddings + ChromaDB + fallback retrieval

Guideline retrieval, source metadata, relevance scores, synthesized evidence answer.

Precision@K, Recall@K, groundedness, citation correctness

Clinical Extraction

Structured clinical schemas

Consolidates medical information from patient/document inputs.

Field completeness, structured-output validity

Patient Summary

Evidence-aware clinical synthesis

Generates structured patient context and tracks confidence/missing information.

Factual consistency, completeness, hallucination rate

Case Questions

Context-aware generation

Produces prioritized doctor discussion questions from the case.

Relevance, completeness, evidence grounding

Doctor Feedback

Structured interpretation

Preserves doctor-stated information and separates it from AI interpretation.

Provenance accuracy, safety

Treatment Response

Rule/AI-assisted classification

Classifies documented response as improved, worsened, mixed, stable, or insufficient data.

Classification accuracy, evidence grounding

Follow-up Intelligence

Longitudinal analysis

Identifies follow-up needs, unresolved issues and monitoring requirements.

Temporal accuracy, completeness

Personalized Care Plan

Multimodal clinical synthesis

Combines patient context, treatment response, doctor feedback and evidence into structured care guidance.

Groundedness, personalization, safety

CarePath Memory

Patient longitudinal context

Retains relevant information for timeline, summary and follow-up workflows.

Retrieval relevance, memory correctness

AI Safety Evaluation

Regression + adversarial testing

Structured validation, confidence testing, prompt-injection defenses, failure handling and medication boundary tests.

Hallucination rate, safety violations, regression coverage

<a id="key-metrics"></a>

📌 Key Project Metrics

Metric

Value

Specialized AI / Intelligence Engines

13

Multi-Agent Healthcare Agents

11

Database Models

19

Backend Domain Services

12

Architecture Topics

15

Frontend Command Center Areas

6

Latest Reported Pytest Result

82 passed

Reported Test Failures

0

Vector Database

ChromaDB

Relational Database

PostgreSQL / Supabase

Object Storage

Supabase Storage

AI Intelligence Engines

OCR Engine

Clinical NLP / Bio-NER Engine

Clinical Extraction Engine

Vision Engine

Embedding Service

RAG Knowledge Engine

CarePath Synthesis Engine

Patient Summary Engine

Case Question Engine

Doctor Feedback Engine

Treatment Response Engine

Follow-up Intelligence Engine

Personalized Care Plan Engine

Important: metrics such as confidence, risk score, probability, and relevance are system-level AI signals. They are not presented as clinically validated accuracy percentages.

📊 AI Confidence & Prediction Signals

Signal

Typical Representation

Purpose

OCR confidence

0–1

Reliability of extracted document text

Entity confidence

0–1

Reliability of a clinical entity

NLP confidence

0–1

Reliability of clinical extraction

Vision confidence

0–1

Confidence attached to visual findings

RAG relevance

0–1

Relevance of retrieved evidence

Summary confidence

0–1

Confidence in synthesized patient context

Treatment-response confidence

0–1

Confidence in response classification

Follow-up confidence

0–1

Confidence in follow-up insight

Care-plan confidence

0–1

Confidence in care-plan generation

Differential probability

0–1

Structured differential field

Risk score

0–100

Structured risk-prioritization signal

Care-plan completion

%

Completion analytics

Medication adherence

%

Medication-status analytics

Prediction / scoring pipeline

flowchart LR
    DATA[Patient + Clinical Data] --> FACTS[Structured Clinical Facts]

    FACTS --> OCR[OCR Confidence]
    FACTS --> NLP[NLP Confidence]
    FACTS --> VIS[Vision Confidence]
    FACTS --> RAG[RAG Relevance]

    OCR --> SUMMARY[Patient Summary]
    NLP --> SUMMARY
    VIS --> SUMMARY

    RAG --> REASONING[Clinical Reasoning]
    SUMMARY --> REASONING

    REASONING --> DIFF[Differential Probability]
    REASONING --> RISK[Risk Score]

    REASONING --> REFERRAL[Referral Ranking]
    REFERRAL --> CAREPLAN[Personalized Care Plan]
    CAREPLAN --> FOLLOW[Follow-up Confidence]

The original project architecture specifically identifies confidence estimation, severity estimation, treatment-failure detection, referral ranking, and explainable AI as AI/ML responsibilities. fileciteturn6file6L727-L781

🧪 AI Evaluation Metrics

AI Component

Evaluation Metrics

OCR

Character/word accuracy, field extraction accuracy, confidence calibration

NLP / Bio-NER

Precision, Recall, F1, negation accuracy

Vision

Accuracy, Precision, Recall, F1, AUROC where validated

RAG

Precision@K, Recall@K, MRR, groundedness, citation correctness

Referral Ranking

Top-1/Top-K specialist accuracy, ranking quality

Treatment Response

Classification accuracy, macro F1

Follow-up Intelligence

Recall of required follow-ups, false-positive rate

Care Plan

Groundedness, completeness, human evaluation

Safety

Prompt-injection success rate, hallucination rate, unsafe-action rate

No unmeasured benchmark values are claimed here; these are the evaluation targets defined for the platform.

<a id="database"></a>

🗄️ Database Architecture

CarePath AI uses a hybrid storage architecture:

                 CAREPATH APPLICATION
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     PostgreSQL     Supabase Storage  ChromaDB
          │              │              │
   Structured Data    Medical Files   Evidence
          │              │              │
          ├──── Patient │              │
          ├──── Visits  ├── PDFs       ├── Embeddings
          ├──── Symptoms├── Reports    ├── Guidelines
          ├──── Meds    ├── Images     └── Retrieval
          ├──── AI      └── X-rays
          ├──── Plans
          ├──── Timeline
          └──── Audit

Core relational domains

Users
Patients
Family Members

Visits
Symptom Sessions
Patient Symptoms
Medications
Medical Files

AI Analyses
Recommendations
Care Plans
Follow-ups

Feedback
Notifications

Prompt Templates
Audit History
Agent Runs

Timeline Events
Evidence Retrieval

Database design principles

PostgreSQL for structured healthcare/application data.

Supabase Storage for medical files.

ChromaDB for vectorized clinical evidence.

SQLAlchemy for domain persistence.

Separate CRUD modules by domain.

Audit history for traceability.

Agent runs for workflow observability.

🗂️ Database Relationship Overview

erDiagram

    USER ||--|| PATIENT_PROFILE : owns
    USER ||--o{ FAMILY_MEMBER : manages

    USER ||--o{ VISIT : has
    USER ||--o{ SYMPTOM_SESSION : starts
    SYMPTOM_SESSION ||--o{ PATIENT_SYMPTOM : contains
    USER ||--o{ MEDICATION : uses
    USER ||--o{ MEDICAL_FILE : uploads

    USER ||--o{ AI_ANALYSIS : receives
    AI_ANALYSIS ||--o{ RECOMMENDATION : generates
    AI_ANALYSIS ||--o{ CARE_PLAN : generates
    CARE_PLAN ||--o{ FOLLOW_UP : schedules

    USER ||--o{ FEEDBACK : submits
    USER ||--o{ NOTIFICATION : receives

    USER ||--o{ AGENT_RUN : executes
    USER ||--o{ AUDIT_HISTORY : generates
    USER ||--o{ TIMELINE_EVENT : accumulates
    USER ||--o{ EVIDENCE_RETRIEVAL : retrieves

<a id="security"></a>

🛡️ Security, PHI & Medical Safety

Authentication

The architecture includes:

JWT authentication

password hashing

token validation

role information

token expiration

protected backend routes

PHI protection

The security sandbox covers common PHI patterns such as:

SSN
Phone
Email
MRN
Date of Birth

Prompt-injection defense

Medical documents and patient text are treated as untrusted data, not system instructions.

flowchart LR
    INPUT[Patient / Document Input]
    INPUT --> VALIDATE[Validation]
    VALIDATE --> PHI[PHI Redaction]
    PHI --> INJECTION[Prompt Injection Defense]
    INJECTION --> AI[AI / Agent]
    AI --> STRUCT[Structured Output Validation]
    STRUCT --> REVIEW[Human Review]

Medication safety boundary

CarePath follows:

Prescription
      ↓
AI extracts
      ↓
Patient verifies
      ↓
Schedule / Reminder

Not:

Symptoms
   ↓
AI
   ↓
AI independently prescribes medication

The project architecture explicitly states that CarePath is intended to guide patients rather than replace doctors or diagnose diseases autonomously. fileciteturn6file4L470-L478

<a id="getting-started"></a>

🚀 Getting Started

Prerequisites

Node.js

Python 3.10+

Git

npm

PostgreSQL/Supabase for the full data layer

ChromaDB for local vector retrieval

Optional AI provider credentials

Optional Tesseract installation for the OCR fallback

1. Repository & Environment Setup

git clone <your-repository-url>
cd CarePath-AI

Create the environment files from the supplied templates where applicable.

cp .env.example .env

Configure the required credentials such as:

GEMINI_API_KEY
DATABASE_URL
SUPABASE_URL
SUPABASE_KEY
JWT_SECRET / SECRET_KEY
PHI_SALT

Never commit real credentials, API keys, passwords, or PHI.

2. Backend Initialization (FastAPI)

Create and activate the Python environment:

python -m venv .venv

Windows:

.venv\Scripts\activate

macOS / Linux:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the AI/API service:

uvicorn app.main:app --reload

The API documentation will be available at:

http://localhost:8000/docs

3. Frontend Initialization (React / Vite)

Open a second terminal:

npm install
npm run dev

The Vite development server will display the frontend URL in the terminal.

4. Testing

PYTHONPATH=. pytest -q

Windows PowerShell:

$env:PYTHONPATH="."
pytest -q

<a id="how-to-use"></a>

📖 How to Use (Quick Workflow)

Open CarePath AI: Start from the patient-facing dashboard or architecture command center.

Start a care session: Enter the patient's symptoms, duration, severity, and relevant context.

Upload medical records: Add prescriptions, laboratory reports, clinical notes, or supported medical images.

Run AI processing: The system can route information through Intake, Vision, Medical Docs, Timeline, and Evidence agents according to available inputs.

Review extracted information: Inspect structured symptoms, medications, diagnoses, document fields, image findings, confidence values, and evidence.

Build clinical context: Timeline and memory organize information across the patient journey.

Review evidence: RAG retrieves relevant medical guidelines and source information.

Generate navigation: Clinical Reasoning and Referral produce specialist-oriented navigation, urgency, reasoning, and questions.

Prepare for care: Care Plan organizes patient preparation, monitoring, action items, and doctor questions.

Continue the journey: Follow-up Intelligence and CarePath Memory preserve continuity for future interactions.

flowchart TD
    A[Login / Open CarePath] --> B[Dashboard]
    B --> C[Start Patient Care Session]

    C --> D[Enter Symptoms]
    D --> E{Medical Files?}

    E -->|Image| F[Vision Agent]
    E -->|Document| G[Medical Docs Agent]
    E -->|No| H[Intake + Timeline]

    F --> H
    G --> H

    H --> I[Evidence / RAG]
    I --> J[Clinical Reasoning]
    J --> K[Specialist Referral]
    K --> L[Care Plan]
    L --> M[Follow-up Intelligence]
    M --> N[CarePath Memory]
    N --> O[Next Care Interaction]

🧭 How the Supervisor Works

The Supervisor is the most important orchestration component.

It decides:

If an image exists → run Vision.

If a medical document exists → run Medical Docs.

If symptoms trigger a safety concern → prioritize Safety.

If a required artifact is missing → skip unnecessary agents.

Wait for required outputs.

Merge the results.

Send the structured context to Clinical Reasoning.

Continue to Referral, Care Plan, and Follow-up.

This is what makes the platform dynamic rather than a fixed pipeline. The original CarePath workflow describes the Supervisor as deciding which agents run based on available inputs and patient conditions. fileciteturn6file9L1190-L1204

🔍 Example Agent Flow

Vision Agent

Supervisor
    ↓
Uploaded Image
    ↓
Vision Processing
    ↓
Finding Extraction
    ↓
Confidence + Metadata
    ↓
Structured JSON

Medical Docs Agent

Supervisor
    ↓
PDF / Prescription
    ↓
OCR
    ↓
Clinical NLP
    ↓
Medications / Diagnoses / Labs
    ↓
Structured JSON

Evidence Agent

Clinical Question
      ↓
Embedding
      ↓
ChromaDB
      ↓
Top-K Evidence
      ↓
Source Metadata
      ↓
Evidence Summary

Referral Agent

Symptoms
+
Timeline
+
Vision
+
Documents
+
Evidence
      ↓
Referral Ranking
      ↓
Specialty
+
Confidence
+
Reasoning
+
Urgency
+
Doctor Questions

The original architecture describes these agent-level workflows and their structured outputs in the CarePath design. fileciteturn6file9L1151-L1189

🧪 Testing & Verification

Latest reported development result

82 passed
0 failed

The test suite covers:

domain models

integration

service interfaces

main API

NLP

OCR

RAG

validation

Vision

database functionality

AI evaluation framework

flowchart TD
    TEST[CarePath AI Evaluation]

    TEST --> OCR[OCR Accuracy]
    TEST --> NLP[NLP Entity Extraction]
    TEST --> VISION[Vision Evaluation]
    TEST --> RAG[RAG Retrieval]
    TEST --> HALL[Hallucination Checks]
    TEST --> STRUCT[Structured Output Validation]
    TEST --> CONF[Confidence Testing]
    TEST --> INJECT[Prompt Injection]
    TEST --> MED[Medication Safety]
    TEST --> FAIL[AI Failure Scenarios]

🌟 What Makes CarePath AI Different?

One connected healthcare workflow: It connects symptoms, documents, images, evidence, referral, care planning, memory, and follow-up instead of treating each AI task as an isolated chatbot request.

Built for healthcare navigation: The system focuses on helping patients reach the right specialist and prepare for care rather than positioning itself as an autonomous doctor.

Multimodal clinical intelligence: Text, medical documents, images, structured records, and clinical evidence can contribute to one patient context.

Continuity, not just one-time answers: Timeline, CarePath Memory, treatment response, and follow-up intelligence are designed around the patient's journey over time.

Evidence-aware AI: RAG provides a dedicated evidence retrieval layer with source information.

Human-in-the-loop healthcare: AI-derived information is intended for review rather than unquestioned automation.

Strict medication boundary: The system extracts and organizes prescription information but does not independently prescribe or modify medication.

Modular agent architecture: Each major healthcare-navigation responsibility maps to a specialized agent, keeping the system easier to reason about and integrate.

🛣️ Development Roadmap

The original CarePath project plan uses four major sprint stages:

Sprint 0 — Planning

Problem validation

Literature review

Competitor analysis

Architecture

GitHub setup

Technology stack

API contracts

Folder structure

Sprint 1 — Foundation

Database

Storage

Backend

Authentication

Baseline AI

Frontend skeleton

Sprint 2 — Core Workflow

Goal: Complete end-to-end patient journey

Patient Upload
      ↓
Backend
      ↓
AI Agents
      ↓
Recommendation
      ↓
Frontend Display

Sprint 3 — Innovation

Examples from the CarePath plan:

Medical Knowledge Graph

Patient Timeline Database

Dynamic Supervisor Agent

Event-driven orchestration

WebSockets

Voice Assistant UI

Interactive Medical Timeline

Treatment Failure Detection

Personalized Care Recommendations

Explainable AI with evidence citations

Sprint 4 — Final Integration

Bug fixing

Integration

Testing

Deployment

README

Architecture diagram

Demo video

Pitch deck

Presentation

Mock judging

The sprint structure and innovation items come directly from the project's earlier CarePath development plan. fileciteturn6file6L789-L887

📦 Repository Ownership / Architecture

carepath-ai/
│
├── frontend/              → Frontend & UX
├── backend/               → Backend + Agent Orchestration
├── database/              → Database & Storage
│
├── app/                   → AI Intelligence Layer
│   ├── vision/            → Computer Vision
│   ├── nlp/               → Clinical NLP
│   ├── rag/               → RAG / Evidence
│   ├── ocr/               → OCR
│   └── evaluation/        → AI Evaluation
│
├── deployment/            → Infrastructure
├── docs/                  → Architecture & Documentation
├── tests/                 → Testing
└── pitch/                 → Demo & Presentation

The original team plan assigns the AI intelligence layer to Computer Vision, NLP, RAG, OCR, evaluation, and AI inference APIs, while the backend, frontend, database, and infrastructure are separate ownership areas. fileciteturn6file6L888-L921

⚠️ Medical & Technical Disclaimer

CarePath AI is a software/AI research and development project for healthcare navigation and clinical decision support.

It is not a replacement for a qualified healthcare professional.

The current repository should not be interpreted as demonstrating:

regulatory approval

clinical diagnostic validation

autonomous prescribing

clinical-grade risk prediction

HIPAA certification

prospective clinical validation

external model validation

Confidence, probability, risk, relevance, and pathology scores are software-level AI signals unless separately validated on appropriate clinical datasets.

<div align="center">

🩺 CarePath AI

From symptoms to the right care pathway.

Understand → Structure → Retrieve Evidence → Reason → Refer → Plan → Follow Up

<br/>

Built with React • FastAPI • LangGraph • Python • ChromaDB • PostgreSQL • PyTorch

</div>
