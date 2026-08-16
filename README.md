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

Overview

CarePath AI is an AI-powered clinical intelligence and continuity-of-care platform designed to transform medical documents, clinical notes, patient history, and medical knowledge into structured, traceable, and human-reviewable clinical intelligence.

The platform combines medical OCR, clinical NLP, computer vision, Retrieval-Augmented Generation, patient memory, longitudinal analysis, doctor feedback interpretation, follow-up intelligence, and personalized care-plan organization into one connected workflow.

CarePath AI is intentionally designed as a human-in-the-loop clinical intelligence system. It assists with extraction, organization, retrieval, summarization, and analysis, while maintaining a strict boundary against autonomous prescribing or medication modification.

Real-time Clinical Intelligence Workflow

<p align="center">
  <img src="images/carepath-dashboard.png" width="100%">
</p>

Replace images/carepath-dashboard.png with the actual screenshot when the final UI is available.

<a id="key-features"></a>

✨ Key Features

Capability

What it enables

Smart Document Analyzer

Converts medical documents into structured clinical information using OCR and medical-field extraction.

Prescription Understanding

Extracts documented medication names, dosage, frequency, and duration for patient verification.

Clinical NLP & Bio-NER

Identifies symptoms, medications, diagnoses, anatomy, procedures, and laboratory-related entities.

Medical Computer Vision

Processes medical images and DICOM-compatible inputs into structured imaging-analysis results with explainability output.

Medical RAG

Retrieves relevant clinical guideline content from a vector knowledge store and preserves source/evidence information.

Doctor Bridge

Generates patient summaries, case-specific questions, and structured interpretation of documented doctor feedback.

CarePath Memory

Organizes clinically relevant information that should be retained and retrieved across the patient's care journey.

Patient Timeline

Extracts and summarizes clinically relevant events over time.

Symptom Trend Analysis

Organizes documented symptom changes across the patient timeline.

Treatment-Response Analysis

Analyzes documented treatment response without independently changing treatment.

Follow-up Intelligence

Identifies documented follow-ups, pending information, unresolved issues, and continuity needs.

Personalized Care Plan

Combines verified patient information, doctor-stated instructions, trends, follow-ups, and evidence into a structured care plan.

AI Safety Evaluation

Tests hallucination resistance, prompt injection, confidence behavior, structured outputs, medication safety, and failure scenarios.

<a id="technology-stack"></a>

🧰 Technology Stack

Layer

Technologies

AI / Backend

Python 3.13, FastAPI, Uvicorn, Pydantic

OCR

EasyOCR, Tesseract-compatible OCR pipeline

Clinical NLP

Python pattern-based Bio-NER, ICD-10 mapping, negation detection

Computer Vision

PyTorch, TorchVision, NumPy, Pillow

Medical Imaging

DICOM / pydicom-compatible processing

RAG / Retrieval

ChromaDB, vector retrieval, deterministic fallback ranking

Knowledge Base

Medical clinical-guideline documents and structured evidence

Validation

Pydantic schemas, input validation, structured output validation

Testing

Pytest, adversarial AI testing, integration testing

UI / Demo

Streamlit

Deployment

Docker, Docker Compose

Configuration

Environment-based application settings

<a id="architecture"></a>

🏗️ Architecture

flowchart LR
    UI[CarePath AI Interface] --> API[FastAPI API Gateway]

    API --> OCR[OCR Engine]
    API --> NLP[Clinical NLP / Bio-NER]
    API --> VISION[Medical Vision Engine]
    API --> RAG[RAG Knowledge Engine]
    API --> CORE[CarePath Clinical Synthesis]

    OCR --> DATA[Structured Clinical Data]
    NLP --> DATA
    VISION --> DATA

    RAG --> CHROMA[(ChromaDB)]
    RAG --> EVIDENCE[Evidence + Citations]

    DATA --> SUMMARY[Patient Summary]
    SUMMARY --> QUESTIONS[Case-Specific Questions]
    QUESTIONS --> DOCTOR[Doctor Feedback]

    DOCTOR --> MEMORY[CarePath Memory]
    MEMORY --> TIMELINE[Patient Timeline]

    TIMELINE --> TRENDS[Symptom Trends]
    TRENDS --> RESPONSE[Treatment Response]
    RESPONSE --> FOLLOWUP[Follow-up Intelligence]
    FOLLOWUP --> PLAN[Personalized Care Plan]

    EVIDENCE --> PLAN
    PLAN --> UI

The architecture separates AI capabilities into independently testable services while allowing the CarePath clinical synthesis layer to orchestrate information across the complete care journey.

<br>

<a id="core-modules"></a>

🚀 Core Modules

Module

Technology / Approach

Current Implementation

Planned Evaluation

Smart Document Analyzer

OCR + structured extraction

Extracts document text, prescription fields, laboratory metrics, confidence information, and structured medical fields.

OCR accuracy, extraction accuracy, confidence calibration

Clinical NLP / Bio-NER

Pattern-based clinical entity extraction + ICD-10 mapping

Detects symptoms, medications, diagnoses, anatomy and negation cues with structured confidence output.

Entity precision/recall, negation accuracy, coding correctness

Medical Computer Vision

PyTorch + TorchVision + image processing

Processes medical images/DICOM inputs and returns structured findings, pathology scores and explainability output.

Classification quality, confidence, robustness, explainability

Medical RAG

ChromaDB + retrieval + deterministic fallback

Retrieves medical guideline chunks with source metadata and supports graceful fallback when vector retrieval is unavailable.

Retrieval relevance, groundedness, citation correctness

Patient Summary

Clinical synthesis

Converts available clinical information into structured patient context for downstream workflows.

Completeness, factual consistency, hallucination rate

Case Questions

Clinical context generation

Generates case-specific questions from documented patient information for doctor review.

Relevance, evidence grounding

Doctor Feedback

Structured clinical interpretation

Separates doctor-stated information from AI interpretation.

Fact/evidence separation, safety

Symptom Trends

Timeline analysis

Organizes documented symptom changes over time.

Temporal accuracy, event extraction

Treatment Response

Longitudinal analysis

Analyzes documented response without independently modifying treatment.

Evidence grounding, temporal consistency

Follow-up Intelligence

Continuity analysis

Identifies documented follow-ups, pending information and unresolved issues.

Date accuracy, completeness, false-positive rate

Personalized Care Plan

Evidence-aware synthesis

Combines patient information, doctor instructions, trends, follow-ups and evidence into a structured care plan.

Groundedness, safety, personalization

AI Safety Testing

Adversarial + regression testing

Covers hallucination, prompt injection, structured outputs, confidence, medication safety and failure scenarios.

Regression coverage, safety violations

<br>

🧠 1. Artificial Intelligence (AI) Domain

The AI domain acts as a clinical intelligence layer that transforms unstructured medical information into structured, traceable and reviewable information.

Feature

Technical Breakdown & Capability

📄 Smart Document Analysis

Turns medical paperwork into structured data. OCR extracts text from uploaded documents and downstream extraction identifies prescriptions, laboratory metrics, symptoms and other clinical fields.

🧬 Clinical Bio-NER

Finds medically meaningful entities. Clinical text is processed for symptoms, medications, diagnoses, anatomy, procedures and laboratory-related entities, with negation and confidence information.

🩻 Medical Computer Vision

Processes medical images. DICOM-compatible and standard images are parsed, normalized and analyzed through the Vision subsystem with structured pathology scores and explainability output.

📚 Medical RAG

Retrieves evidence instead of relying only on generation. Clinical guideline content is stored and retrieved through ChromaDB, with source metadata and deterministic fallback behavior.

🧠 Clinical Synthesis

Connects the modules. OCR, NLP, Vision and RAG outputs can be combined into a structured clinical intelligence workflow.

<br>

🧠 2. Doctor + Memory Domain

The Doctor + Memory layer preserves clinically relevant context across interactions and keeps AI interpretation separate from documented clinical facts.

Feature

Technical Breakdown & Capability

👨‍⚕️ Patient Summary

Creates a structured clinical overview. Relevant documented information is organized for easier doctor review.

❓ Case-Specific Questions

Prepares focused questions for clinical review. Questions are generated from available case information rather than generic templates alone.

📝 Clinical Information Extraction

Structures clinical notes and feedback. Important entities and events are extracted into validated schemas.

💬 Doctor Feedback Interpretation

Preserves clinician intent. Doctor-stated information is explicitly distinguished from AI-generated interpretation.

🧠 CarePath Memory

Maintains continuity. Relevant information can be retained and retrieved for downstream timeline, trend and follow-up workflows.

<br>

📈 3. Continuity of Care Domain

The continuity layer connects information across time rather than treating every medical interaction as an isolated event.

Feature

Technical Breakdown & Capability

📅 Patient Timeline

Builds a chronological clinical context. Relevant patient events can be extracted and summarized across records.

📊 Symptom Trend Analysis

Tracks documented changes. Symptoms can be compared across recorded time points without inventing undocumented events.

🔄 Treatment Response

Analyzes documented response. The system organizes response information while avoiding independent treatment decisions.

⏰ Follow-up Intelligence

Surfaces continuity needs. Explicit follow-ups, pending results, unresolved issues and documented instructions are organized for review.

🗂️ Personalized Care Plan

Combines the available evidence. The plan can contain doctor-stated instructions, patient-verified actions, monitoring items, follow-ups, questions and uncertainties.

<br>

🛡️ 4. AI Safety & Evaluation Domain

Safety is treated as a core engineering requirement rather than a final-stage feature.

Feature

Technical Breakdown & Capability

🧪 Hallucination Testing

Tests incomplete, contradictory and unsupported clinical inputs to ensure the system represents uncertainty instead of fabricating facts.

🔐 Prompt Injection Testing

Tests instruction-hijacking attacks embedded in patient text, OCR output, clinical notes and retrieved content.

💊 Medication Safety

Regression tests ensure that AI does not independently prescribe, change, stop or modify medication.

📦 Structured Output Validation

Validates AI responses against strict Pydantic schemas and rejects malformed or unexpected structures.

📈 Confidence Testing

Checks that confidence remains within bounds and appropriately reflects ambiguity and evidence quality.

🚨 Failure Scenarios

Tests OCR failures, RAG failures, model-provider failures, malformed outputs, empty inputs and vector-store failures.

<br>

<a id="key-metrics"></a>

📌 Key Project Metrics

Metric

Value

Total Tests Passed

177

Test Failures

0

Test Warnings

8

AI Testing Status

PASSED

End-to-End AI Audit

PASSED

Prompt Injection Testing

PASSED

Medication Safety Regression

PASSED

Structured Output Validation

PASSED

Hallucination Testing

PASSED

RAG Fallback Testing

PASSED

Primary AI Domains

5+

Seed Clinical Guidelines

3

Performance/accuracy numbers are intentionally not fabricated. Add measured latency, OCR accuracy, retrieval precision, dataset size, or model metrics only after benchmarking them on real project data.

📊 AI Testing Results

pie title CarePath AI Test Suite
    "Passed Tests" : 177
    "Warnings" : 8

AI Safety Coverage

flowchart TD
    TEST[CarePath AI Testing] --> OCR[OCR Accuracy]
    TEST --> DOC[Document Extraction]
    TEST --> RAG[RAG Retrieval]
    TEST --> HALL[Hallucination Checks]
    TEST --> STRUCT[Structured Outputs]
    TEST --> CONF[Confidence Testing]
    TEST --> INJECT[Prompt Injection]
    TEST --> MED[Medication Safety]
    TEST --> FAIL[Failure Scenarios]
    TEST --> E2E[End-to-End Integration]

🌟 What Makes CarePath AI Different?

One connected clinical workflow: Document analysis, NLP, Vision, RAG, memory, doctor feedback, timeline analysis and follow-up intelligence are designed to work together.

Evidence-aware AI: Retrieved knowledge and patient information are kept traceable rather than presented as unsupported AI facts.

Human-in-the-loop healthcare: AI assists doctors and patients with organization and interpretation without becoming an autonomous prescribing system.

Continuity of care: The system is designed around longitudinal patient information instead of isolated medical interactions.

Strict medication boundary: Prescription → AI extracts → Patient verifies → Schedule/reminder.

Safety-first engineering: Hallucination, prompt injection, confidence, structured-output and failure-scenario testing are part of the implementation.

Graceful degradation: Components such as RAG are designed with deterministic fallback behavior when external/vector infrastructure is unavailable.

<a id="getting-started"></a>

🚀 Getting Started

Prerequisites

Python 3.13 or higher

Git

Docker / Docker Compose (optional)

Required dependencies from requirements.txt

1. Repository & Environment Setup

Clone the repository and prepare the environment.

git clone https://github.com/sanya-6976/CarePath-AI.git
cd CarePath-AI

Create and activate a virtual environment.

python -m venv .venv
.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Copy the environment template:

Copy-Item .env.example .env

Populate .env with the required configuration.

Never commit .env or API keys to GitHub.

2. Backend Initialization (FastAPI)

Start the CarePath AI backend:

uvicorn app.main:app --reload

The API documentation will be available at:

http://127.0.0.1:8000/docs

3. Frontend / Demo Initialization

If using the included Streamlit interface:

streamlit run ui/app.py

📖 How to Use (Quick Workflow)

Upload a medical document: Provide a prescription, report, clinical note or supported medical document.

Run document analysis: OCR extracts the document content.

Extract clinical information: NLP structures symptoms, medications, diagnoses and other entities.

Review patient context: Generate a structured patient summary and case-specific questions.

Use medical RAG: Query the knowledge base when evidence retrieval is required.

Add doctor feedback: Preserve explicit clinician statements separately from AI interpretation.

Build continuity: Use timeline, symptom trends and treatment-response information.

Follow-up intelligence: Surface documented follow-ups, pending information and unresolved issues.

Generate care plan: Organize verified information and evidence into a structured personalized care plan.

Human review: Patient and/or clinician reviews the generated information before taking action.

flowchart TD
    A[Upload Medical Document] --> B[OCR]
    B --> C[Clinical Information Extraction]
    C --> D[Patient Summary]
    D --> E[Case-Specific Questions]
    E --> F[Doctor Feedback]
    F --> G[CarePath Memory]
    G --> H[Patient Timeline]
    H --> I[Symptom Trends]
    I --> J[Treatment Response]
    J --> K[Follow-up Intelligence]
    K --> L[Personalized Care Plan]
    L --> M[Patient / Doctor Review]

🧪 Testing

Run the complete test suite:

pytest -q

Current audited result:

177 passed, 8 warnings

The test suite includes:

OCR and document extraction

RAG retrieval and fallback

Hallucination prevention

Strict Pydantic validation

Dynamic confidence testing

Prompt injection defense

Medication safety regression

AI failure scenarios

End-to-end pipeline integration

Fact/evidence separation

Medical safety disclaimer validation

<a id="safety"></a>

🛡️ Security & Medical Safety

Medication safety: AI does not independently prescribe, modify, start or stop medication.

Human verification: Prescription information follows the extraction → patient verification → scheduling/reminder workflow.

Evidence traceability: AI interpretation is separated from doctor-stated and extracted information.

Prompt injection defense: Patient documents, OCR text, clinical notes and retrieved content are treated as untrusted data.

Structured validation: AI responses are validated through Pydantic schemas.

Secret management: API keys and credentials belong in .env and must not be committed to Git.

Graceful failure: External model and retrieval failures should degrade safely rather than silently fabricate information.

Medical Disclaimer

CarePath AI is an AI/software development project intended to assist with medical information organization, extraction, retrieval, summarization and continuity-of-care workflows.

It is not a replacement for a qualified healthcare professional and must not be used as an autonomous prescribing or treatment-decision system.

🗺️ Development Roadmap

timeline
    title CarePath AI Development Roadmap

    Sprint 1 : Core Product Features
             : Smart Document Analyzer
             : OCR
             : Prescription Extraction
             : Report Extraction
             : RAG
             : Evidence Formatting

    Sprint 2 : Doctor + Memory
             : Patient Summary
             : Case-Specific Questions
             : Clinical Information Extraction
             : Doctor Feedback Interpretation

    Sprint 3 : Continuity of Care
             : Symptom Trend Analysis
             : Treatment-Response Analysis
             : Follow-up Intelligence
             : Personalized Care Plan

    Sprint 4 : AI Testing Only
             : OCR Accuracy
             : Document Extraction
             : RAG Retrieval
             : Hallucination Checks
             : Structured Output Validation
             : Confidence Testing
             : Prompt Injection
             : Medication Safety
             : AI Failure Scenarios

🤝 Contribution

When contributing to the AI branch:

Keep AI services modular.

Preserve existing service interfaces.

Add tests for meaningful behavior changes.

Do not weaken tests to make them pass.

Preserve evidence and source traceability.

Maintain the medication-safety boundary.

Do not commit secrets or .env files.

Run the complete test suite before submitting changes.

<div align="center">
  <sub>Built with a safety-first, human-in-the-loop approach for connected clinical intelligence.</sub>
</div>
