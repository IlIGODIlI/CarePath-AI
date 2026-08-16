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

# ✨ Key Features

| Capability | What it enables |
| :--- | :--- |
| 🧠 **AI-Powered Patient Intake** | Structures symptoms, patient context, history, and encounter information for downstream AI workflows. |
| 📄 **Smart Document Analyzer** | Extracts structured information from uploaded medical reports, prescriptions, and supported documents. |
| 💊 **Medication Companion** | Analyzes prescription information, supports medication confirmation, and enables reminders and adherence workflows. |
| 📚 **Evidence-Backed Guidance (RAG)** | Retrieves relevant medical evidence and supporting sources to make AI guidance more transparent and explainable. |
| 🩺 **Explainable Referral Card** | Summarizes symptoms, medical history, reasoning, and evidence to explain why a specialist is recommended. |
| 👨‍⚕️ **CarePath Doctor Bridge** | Prepares a doctor-ready medical summary, generates case-specific questions, and enables expert review of AI outputs. |
| 🧠 **CarePath Memory** | Retains relevant patient context across interactions to provide consistent, context-aware guidance. |
| 🕐 **AI-Generated Patient Timeline** | Organizes symptoms, consultations, reports, prescriptions, referrals, treatments, and follow-ups into a chronological journey. |
| 📝 **Personalized Care Plan** | Converts relevant patient context and clinician input into structured next steps, monitoring, and follow-up guidance. |
| 🔔 **Follow-up Intelligence** | Supports post-consultation check-ins, reminders, treatment-response tracking, and escalation workflows. |
| 🛡️ **Safety-First Agent** | Detects configured safety signals and can interrupt the normal workflow when priority handling is required. |
| 🤖 **Multi-Agent Orchestration** | Uses LangGraph to coordinate specialized healthcare agents through shared state and conditional routing. |
| 🤝 **Human-in-the-Loop Review** | Allows AI workflows to pause for clinician review and resume with expert feedback incorporated into the patient context. |
| 📡 **SSE Workflow Streaming** | Streams agent execution, evidence retrieval, review requests, completion, and failure events to the frontend. |
| 🔗 **Structured AI Service Contracts** | Decouples the backend and LangGraph orchestration layer from individual AI providers and model implementations. |

---
## 🏗️ Architecture Overview

CarePath AI is organized into four tightly integrated domains that work
together to create a continuous healthcare navigation journey.

Each domain owns a distinct responsibility while communicating through
well-defined API, service, and orchestration contracts.

> **The frontend presents the patient journey, the backend coordinates
> the system, LangGraph orchestrates intelligence, and specialized AI
> services provide the context and evidence required for each workflow.**

## 🏛️ System Architecture

```mermaid
flowchart TD

    PATIENT(["👤 Patient"])

    UI["🎨 React Patient Experience"]

    API["⚡ FastAPI API Layer"]

    AUTH["🔐 Authentication & Authorization"]

    SUP["🤖 LangGraph Supervisor"]

    STATE[["🧠 CarePath State<br/>Shared Patient Context"]]

    AGENTS["🧩 Specialized AI Agents"]

    SERVICES["🔗 AI Service Contracts"]

    GEMINI["✨ Gemini / LLM"]
    OCR["📄 OCR / Document Intelligence"]
    VISION["👁️ Computer Vision"]
    RAG["📚 Evidence / RAG"]

    DB[("🗄️ PostgreSQL")]

    PATIENT --> UI
    UI --> API
    API --> AUTH
    AUTH --> SUP

    SUP <--> STATE
    SUP --> AGENTS

    AGENTS --> SERVICES

    SERVICES --> GEMINI
    SERVICES --> OCR
    SERVICES --> VISION
    SERVICES --> RAG

    STATE --> DB

    SUP --> DB

    SUP --> API
    API --> UI
```
The architecture separates presentation, API orchestration, agent
intelligence, AI capabilities, and persistent patient data into
independent layers. This allows individual components to evolve without
coupling the entire healthcare workflow to a single model or service.

---

## 🤖 1. AI & Multi-Agent Intelligence Domain

> *The intelligence layer of CarePath AI. It transforms patient inputs,
> medical documents, contextual information, and retrieved evidence into
> structured healthcare-navigation workflows.*

| Feature | Technical Breakdown & Capability |
| :--- | :--- |
| 🧠 **LangGraph Supervisor** | Acts as the central orchestrator and determines which specialized agent should execute based on the current CarePath state. |
| 📥 **Intake Agent** | Structures symptoms, patient context, history, encounter information, and user intent for downstream agents. |
| 📄 **Medical Records Agent** | Processes supported medical reports, prescriptions, and extracted document information into structured context. |
| 👁️ **Vision Agent** | Handles supported medical-image analysis through the Computer Vision service contract. |
| 🛡️ **Safety Agent** | Evaluates configured safety signals and can interrupt the normal workflow when priority handling is required. |
| 🧩 **Clinical Reasoning Agent** | Combines patient context, timeline information, document findings, and retrieved evidence into structured reasoning. |
| 📚 **Evidence Agent** | Retrieves relevant supporting information through the RAG layer and provides evidence for explainable outputs. |
| 🩺 **Referral Agent** | Uses available context and reasoning to generate specialist-navigation guidance with an explainable rationale. |
| 👨‍⚕️ **Doctor Bridge** | Produces a doctor-ready summary, generates case-specific questions, and supports clinician review of AI-generated information. |
| 📝 **Care Plan Agent** | Organizes relevant context into structured next steps and monitoring guidance while preserving clinician input. |
| 💊 **Medication Agent** | Processes prescription-derived medication information and supports patient-confirmed medication workflows. |
| 🔔 **Follow-up Agent** | Coordinates follow-up workflows, monitoring, reminders, and escalation paths. |
| 🤝 **Human-in-the-Loop** | Allows an AI workflow to pause for clinician review and resume with expert feedback incorporated into the shared state. |

### 🔄 AI Agent Workflow

```mermaid
flowchart TD

    INPUT(["👤 Patient Request"])

    SUP["🤖 LangGraph Supervisor"]

    STATE[["🧠 CarePath State"]]

    SAFETY["🛡️ Safety Agent"]

    INTAKE["📥 Intake Agent"]
    RECORDS["📄 Medical Records Agent"]
    VISION["👁️ Vision Agent"]
    TIMELINE["🕐 Timeline Agent"]

    REASONING["🧩 Clinical Reasoning"]

    EVIDENCE["📚 Evidence Agent"]

    REFERRAL["🩺 Referral Agent"]

    DOCTOR["👨‍⚕️ Doctor Bridge"]

    REVIEW{"👨‍⚕️ Human Review?"}

    CARE["📝 Care Plan"]

    MED["💊 Medication"]

    FOLLOW["🔔 Follow-up"]

    OUTPUT(["📊 Patient Dashboard"])

    INPUT --> SUP
    SUP <--> STATE

    SUP --> SAFETY

    SAFETY -->|Continue| INTAKE
    SAFETY -->|Priority| OUTPUT

    SUP --> RECORDS
    SUP --> VISION
    SUP --> TIMELINE

    INTAKE --> STATE
    RECORDS --> STATE
    VISION --> STATE
    TIMELINE --> STATE

    STATE --> REASONING
    REASONING --> EVIDENCE
    EVIDENCE --> REASONING

    REASONING --> REFERRAL
    REFERRAL --> DOCTOR

    DOCTOR --> REVIEW

    REVIEW -->|Review Required| DOCTOR
    REVIEW -->|Continue| CARE

    CARE --> MED
    MED --> FOLLOW

    FOLLOW --> STATE

    STATE --> OUTPUT

```
### Design Principle

CarePath AI does not rely on a fixed sequence where every patient must
pass through every agent.

The LangGraph Supervisor evaluates the current shared state and routes
the workflow to the capabilities required for the current interaction.

```text
Current Patient State
        ↓
Determine Required Capability
        ↓
Execute Specialized Agent
        ↓
Update Shared State
        ↓
Re-evaluate
        ↓
Continue / Interrupt / Complete

> **Unlike a fixed sequential pipeline, CarePath AI uses a shared state and conditional agent routing. The LangGraph Supervisor determines which capabilities are required for the current patient context and coordinates the appropriate agents.**

---

## 🧠 2. Patient & Clinical Intelligence Domain

> *The continuity layer of CarePath AI. It transforms fragmented healthcare information into persistent patient context, chronological history, evidence-backed guidance, doctor-ready information, and personalized next steps.*
 
| Feature | Technical Breakdown & Capability |
| :--- | :--- |
| 🧠 **CarePath Memory** | Retains relevant patient context across interactions so subsequent workflows can use previously available information instead of starting from zero. |
| 🕐 **AI-Generated Patient Timeline** | Organizes symptoms, consultations, medical documents, prescriptions, referrals, care plans, and follow-ups into a chronological healthcare journey. |
| 📄 **Smart Document Analyzer** | Processes supported reports and prescriptions, extracts relevant information, and makes the resulting context available to downstream workflows. |
| 📚 **Evidence-Backed Guidance** | Connects healthcare-navigation workflows with retrieved evidence through the RAG layer, allowing supporting sources to accompany relevant outputs. |
| 🩺 **Explainable Referral Card** | Summarizes relevant medical history, current symptoms, identified problems, reasoning, and supporting evidence so the specialist recommendation is understandable. |
| 👨‍⚕️ **CarePath Doctor Bridge** | Handles the doctor interaction layer by preparing a concise patient summary, generating case-specific questions, and supporting expert review of AI-generated outputs. |
| 📝 **Personalized Care Plan** | Organizes relevant patient context and clinician input into structured next steps, monitoring points, and follow-up guidance. |
| 💊 **Medication Companion** | Extracts medication information from supported prescriptions and connects confirmed medication details with reminder and adherence workflows. |
| 🔔 **Follow-up Intelligence** | Extends the healthcare journey beyond the initial consultation through check-ins, follow-up scheduling, treatment-response tracking, and escalation workflows. |

### 🔄 Patient Continuity Architecture

```mermaid
flowchart TD

    INPUT["📥 Patient Information"]

    MEMORY["🧠 CarePath Memory"]

    DOCS["📄 Smart Document Analyzer"]

    TIMELINE["🕐 AI Patient Timeline"]

    EVIDENCE["📚 Evidence / RAG"]

    REFERRAL["🩺 Explainable Referral Card"]

    DOCTOR["👨‍⚕️ CarePath Doctor Bridge"]

    REVIEW["👨‍⚕️ Expert Review"]

    CARE["📝 Personalized Care Plan"]

    MED["💊 Medication Companion"]

    FOLLOW["🔔 Follow-up Intelligence"]

    CONTEXT[["🧠 Unified Patient Context"]]

    INPUT --> MEMORY
    INPUT --> DOCS

    MEMORY --> CONTEXT
    DOCS --> CONTEXT

    CONTEXT --> TIMELINE
    CONTEXT --> EVIDENCE

    EVIDENCE --> REFERRAL

    TIMELINE --> REFERRAL
    TIMELINE --> DOCTOR

    REFERRAL --> DOCTOR

    DOCTOR --> REVIEW
    REVIEW --> CONTEXT

    CONTEXT --> CARE

    CARE --> MED
    CARE --> FOLLOW

    MED --> CONTEXT
    FOLLOW --> CONTEXT

    CONTEXT --> TIMELINE
```

### Continuity Principle


CarePath AI treats the patient's healthcare journey as **persistent
context rather than isolated conversations**.

New symptoms, documents, consultations, referrals, clinician feedback,
medication information, care plans, and follow-up events can contribute
to the patient's evolving context.

```text
New Information
       ↓
Patient Context
       ↓
Timeline + Memory
       ↓
Evidence + Reasoning
       ↓
Doctor Interaction
       ↓
Care Plan
       ↓
Medication + Follow-up
       ↓
Updated Patient Context
```
---
```
## 🎨 3. Frontend & Patient Experience Domain

> *The patient-facing experience layer of CarePath AI. It transforms complex AI workflows and clinical information into a clear, accessible, and actionable healthcare journey.*

| Feature | Technical Breakdown & Capability |
| :--- | :--- |
| 📊 **CarePath Dashboard** | Provides a centralized view of the patient's current healthcare journey, timeline, care plan, medications, referrals, and upcoming follow-ups. |
| 🕐 **Patient Timeline Interface** | Presents symptoms, consultations, documents, prescriptions, referrals, and follow-up events as a chronological healthcare journey. |
| 📄 **Document Upload Interface** | Allows patients to securely upload supported medical reports, prescriptions, and other healthcare documents for processing. |
| 🩺 **Referral Card Interface** | Presents the recommended specialist, supporting reasoning, relevant patient context, and evidence in an understandable format. |
| 👨‍⚕️ **Doctor Bridge Interface** | Presents the doctor-ready summary, case-specific questions, and clinician-review workflow before and during consultation. |
| 💊 **Medication Interface** | Displays confirmed medication information, schedules, reminders, and adherence-related actions. |
| 📝 **Care Plan Interface** | Converts the personalized care plan into clear actions, monitoring points, and follow-up steps for the patient. |
| 📚 **Evidence Presentation** | Displays relevant evidence and supporting sources returned by the RAG workflow without overwhelming the patient with technical information. |
| 🔔 **Follow-up Experience** | Provides reminders, check-ins, progress updates, and follow-up actions throughout the patient's journey. |
| 📡 **Real-Time Workflow Updates** | Uses Server-Sent Events (SSE) to display workflow progress while long-running backend and agent operations are executing. |
| 🌐 **Responsive Experience** | Provides a consistent experience across desktop and mobile layouts while keeping important healthcare information easy to access. |

### 🔄 Frontend Communication Architecture

```mermaid
flowchart TD

    PATIENT(["👤 Patient"])

    UI["🎨 React Application"]

    DASH["📊 CarePath Dashboard"]

    TIMELINE["🕐 Patient Timeline"]

    DOCUMENTS["📄 Document Upload"]

    REFERRAL["🩺 Referral Card"]

    DOCTOR["👨‍⚕️ Doctor Bridge"]

    MEDICATION["💊 Medication"]

    CARE["📝 Care Plan"]

    FOLLOWUP["🔔 Follow-up"]

    API["⚡ FastAPI API"]

    SSE["📡 SSE Stream"]

    AGENTS["🤖 LangGraph Workflow"]

    RESULT["📦 Structured Response"]

    PATIENT --> UI

    UI --> DASH
    UI --> TIMELINE
    UI --> DOCUMENTS
    UI --> REFERRAL
    UI --> DOCTOR
    UI --> MEDICATION
    UI --> CARE
    UI --> FOLLOWUP

    DASH --> API
    TIMELINE --> API
    DOCUMENTS --> API
    REFERRAL --> API
    DOCTOR --> API
    MEDICATION --> API
    CARE --> API
    FOLLOWUP --> API

    API --> AGENTS

    AGENTS --> RESULT
    RESULT --> API

    API --> SSE
    SSE --> UI

    UI --> PATIENT
```

### Frontend Design Principle

The frontend does not directly communicate with individual AI agents.

Instead, all agent execution is mediated through the backend API layer.

```text
Patient
   ↓
React Interface
   ↓
FastAPI API
   ↓
LangGraph Workflow
   ↓
Structured Result
   ↓
FastAPI
   ↓
JSON + SSE Events
   ↓
React Interface
   ↓
Patient



```
---

## ⚙️ 4. Backend & Integration Domain

> *The engineering backbone of CarePath AI. The backend provides secure APIs, authentication, validation, workflow orchestration, AI service integration, real-time communication, and persistence across the healthcare journey.*

| Component | Technical Breakdown & Capability |
| :--- | :--- |
| ⚡ **FastAPI API Layer** | Provides REST endpoints between the React application and backend services. |
| 🔐 **Authentication & Authorization** | Protects patient resources using JWT-based authentication and authorization controls. |
| 🛣️ **API Routers** | Organizes endpoints by functional domain while keeping HTTP concerns separated from application logic. |
| ⚙️ **Service Layer** | Coordinates application logic, patient workflows, persistence, and LangGraph execution. |
| ✅ **Pydantic Validation** | Validates incoming requests and structures outgoing responses using typed schemas. |
| 🤖 **LangGraph Integration** | Connects backend requests to stateful multi-agent workflows and conditional agent routing. |
| 🧠 **CarePath State** | Maintains shared context between agents throughout an active workflow. |
| 🔗 **AI Service Contracts** | Provides provider-independent interfaces for LLM, OCR, Computer Vision, and evidence-retrieval capabilities. |
| 📡 **SSE Streaming** | Streams agent execution, workflow progress, human-review requests, completion, and failure events to the frontend. |
| 🗄️ **Database Integration** | Connects backend services with the persistent healthcare data layer through defined repository/data-access interfaces. |
| ⚠️ **Error Handling** | Converts validation, service, AI, and workflow failures into controlled API responses. |
| 📝 **Logging & Observability** | Captures relevant backend and workflow events to support debugging and operational visibility. |
| 🛡️ **Security Boundaries** | Separates authentication, patient data access, AI processing, and workflow execution to reduce unnecessary coupling and exposure. |

### 🔄 Backend Request Lifecycle

```mermaid
sequenceDiagram

    participant P as 👤 Patient
    participant UI as 🎨 React
    participant API as ⚡ FastAPI
    participant AUTH as 🔐 Auth
    participant SERVICE as ⚙️ Service Layer
    participant GRAPH as 🤖 LangGraph
    participant AGENT as 🧩 Agent
    participant AI as 🔗 AI Service
    participant DB as 🗄️ Database

    P->>UI: Submit request

    UI->>API: HTTP Request

    API->>AUTH: Validate credentials

    AUTH-->>API: Authorized request

    API->>SERVICE: Validated input

    SERVICE->>DB: Retrieve context

    DB-->>SERVICE: Patient data

    SERVICE->>GRAPH: Start workflow

    GRAPH->>AGENT: Route task

    AGENT->>AI: Execute AI capability

    AI-->>AGENT: Structured result

    AGENT-->>GRAPH: Update CarePathState

    GRAPH-->>SERVICE: Workflow result

    SERVICE->>DB: Persist relevant result

    SERVICE-->>API: Structured response

    API-->>UI: JSON / SSE events

    UI-->>P: Updated healthcare journey
```
### 🧩 Backend Architecture

```mermaid
flowchart TD

    CLIENT["🎨 React Frontend"]

    API["⚡ FastAPI API Gateway"]

    AUTH["🔐 Authentication & Authorization"]

    ROUTERS["🛣️ API Routers"]

    VALIDATION["✅ Pydantic Validation"]

    SERVICE["⚙️ Backend Service Layer"]

    GRAPH["🤖 LangGraph Supervisor"]

    STATE[["🧠 CarePathState"]]

    AGENTS["🧩 Specialized Agents"]

    CONTRACTS["🔗 AI Service Contracts"]

    LLM["✨ Gemini / LLM"]

    OCR["📄 OCR / Document Intelligence"]

    VISION["👁️ Computer Vision"]

    RAG["📚 Evidence / RAG"]

    DB[("🗄️ PostgreSQL")]

    SSE["📡 SSE Streaming"]

    ERRORS["⚠️ Error Handling"]

    CLIENT --> API

    API --> AUTH
    AUTH --> ROUTERS

    ROUTERS --> VALIDATION
    VALIDATION --> SERVICE

    SERVICE --> GRAPH
    SERVICE --> DB

    GRAPH <--> STATE
    GRAPH --> AGENTS

    AGENTS --> CONTRACTS

    CONTRACTS --> LLM
    CONTRACTS --> OCR
    CONTRACTS --> VISION
    CONTRACTS --> RAG

    AGENTS --> STATE

    STATE --> GRAPH

    GRAPH --> SERVICE

    SERVICE --> SSE
    SSE --> CLIENT

    API --> ERRORS
    SERVICE --> ERRORS
    GRAPH --> ERRORS
```
### 🔗 AI Service Contract Architecture

```mermaid
flowchart LR

    GRAPH["🤖 LangGraph Agents"]

    CONTRACT["🔗 AI Service Contracts"]

    LLM["✨ LLM Service"]
    DOC["📄 Document Analysis"]
    VISION["👁️ Vision Service"]
    EVIDENCE["📚 Evidence Service"]

    PROVIDER["AI Provider / Model"]

    VECTOR[("ChromaDB")]

    GRAPH --> CONTRACT

    CONTRACT --> LLM
    CONTRACT --> DOC
    CONTRACT --> VISION
    CONTRACT --> EVIDENCE

    LLM --> PROVIDER
    DOC --> PROVIDER
    VISION --> PROVIDER
    EVIDENCE --> VECTOR
```

The service-contract approach keeps the orchestration layer independent
of individual AI providers and model implementations.

```text
LangGraph Agent
       ↓
AI Service Contract
       ↓
Provider / Implementation
       ↓
Structured Result
       ↓
Agent State
```

This makes individual AI capabilities replaceable without requiring the
entire backend or agent graph to be rewritten.

### Backend Design Principles

| Principle | Implementation |
| :--- | :--- |
| **Separation of Concerns** | API routes, services, agents, schemas, and AI integrations remain independently structured. |
| **Stateful Orchestration** | LangGraph manages workflow state through the shared `CarePathState`. |
| **Provider Independence** | AI capabilities are accessed through service contracts rather than direct model coupling. |
| **Human Oversight** | Workflows can pause for clinician review where required. |
| **Secure Access** | Authentication and authorization are enforced before protected patient operations. |
| **Real-Time Feedback** | SSE provides workflow progress to the frontend without requiring continuous polling. |
| **Testability** | Backend services and AI integrations can be tested independently using controlled service implementations and mocks. |
| **Extensibility** | New agents and AI capabilities can be added without redesigning the entire API layer. |

---

# 🗄️ Database Architecture

CarePath AI uses a structured persistence layer to maintain the patient's
healthcare journey across encounters, documents, medications, referrals,
care plans, follow-ups, and timeline events.

The database provides **persistent application data**, while LangGraph's
`CarePathState` manages the **active state of an AI workflow**.

## Database Architecture

```mermaid
flowchart TD

    APP["🎨 CarePath Application"]

    API["⚡ FastAPI Backend"]

    SERVICES["⚙️ Backend Services"]

    REPOSITORY["🗂️ Repository / Data Access Layer"]

    ORM["🔗 SQLAlchemy ORM"]

    DB[("🗄️ PostgreSQL")]

    USER["👤 Users"]

    PATIENT["🧑 Patients"]

    ENCOUNTER["🩺 Encounters"]

    DOCUMENT["📄 Medical Documents"]

    MEDICATION["💊 Medications"]

    REFERRAL["🩺 Referrals"]

    CAREPLAN["📝 Care Plans"]

    FOLLOWUP["🔔 Follow-ups"]

    TIMELINE["🕐 Timeline Events"]

    APP --> API

    API --> SERVICES

    SERVICES --> REPOSITORY

    REPOSITORY --> ORM

    ORM --> DB

    DB --> USER
    DB --> PATIENT
    DB --> ENCOUNTER
    DB --> DOCUMENT
    DB --> MEDICATION
    DB --> REFERRAL
    DB --> CAREPLAN
    DB --> FOLLOWUP
    DB --> TIMELINE
```

### Persistence Flow

```text
Patient Interaction
        ↓
FastAPI Endpoint
        ↓
Backend Service
        ↓
Repository / Data Access
        ↓
SQLAlchemy ORM
        ↓
PostgreSQL
        ↓
Persistent Healthcare Data
```

---

## 🧩 Core Data Domains

| Data Domain | Purpose |
| :--- | :--- |
| 👤 **Users** | Stores authenticated user information and access-related data. |
| 🧑 **Patients** | Maintains patient profile and healthcare-navigation context. |
| 🩺 **Encounters** | Represents consultations and healthcare interactions. |
| 📄 **Medical Documents** | Maintains uploaded document metadata and associated patient/encounter context. |
| 💊 **Medications** | Stores medication information extracted from or associated with prescriptions and patient workflows. |
| 🩺 **Referrals** | Stores specialist-navigation information and referral status. |
| 📝 **Care Plans** | Stores personalized care plans and associated actions. |
| 🔔 **Follow-ups** | Maintains scheduled and completed follow-up activities. |
| 🕐 **Timeline Events** | Represents chronological events that contribute to the patient's healthcare journey. |

---

## 🔗 Patient Data Relationships

```mermaid
erDiagram

    USER ||--o| PATIENT : owns

    PATIENT ||--o{ ENCOUNTER : has
    PATIENT ||--o{ MEDICAL_DOCUMENT : uploads
    PATIENT ||--o{ MEDICATION : uses
    PATIENT ||--o{ REFERRAL : receives
    PATIENT ||--o{ CARE_PLAN : follows
    PATIENT ||--o{ FOLLOW_UP : requires
    PATIENT ||--o{ TIMELINE_EVENT : generates

    ENCOUNTER ||--o{ MEDICAL_DOCUMENT : contains
    ENCOUNTER ||--o{ REFERRAL : generates

    USER {
        uuid id PK
        string email
        string role
        datetime created_at
    }

    PATIENT {
        uuid id PK
        uuid user_id FK
        string profile
        datetime created_at
    }

    ENCOUNTER {
        uuid id PK
        uuid patient_id FK
        string type
        string summary
        datetime occurred_at
    }

    MEDICAL_DOCUMENT {
        uuid id PK
        uuid patient_id FK
        uuid encounter_id FK
        string document_type
        string storage_reference
        datetime uploaded_at
    }

    MEDICATION {
        uuid id PK
        uuid patient_id FK
        string name
        string dosage
        string frequency
        string instructions
    }

    REFERRAL {
        uuid id PK
        uuid patient_id FK
        uuid encounter_id FK
        string specialist
        string reason
        string status
    }

    CARE_PLAN {
        uuid id PK
        uuid patient_id FK
        string title
        string status
        datetime created_at
    }

    FOLLOW_UP {
        uuid id PK
        uuid patient_id FK
        string type
        datetime scheduled_at
        string status
    }

    TIMELINE_EVENT {
        uuid id PK
        uuid patient_id FK
        string event_type
        string description
        datetime occurred_at
    }
```

---

## 🧠 Persistent Data vs AI Workflow State

CarePath separates **long-term patient information** from **temporary
agent execution state**.

| Layer | Responsibility |
| :--- | :--- |
| 🗄️ **PostgreSQL** | Persistent patient and healthcare application data. |
| 🔗 **SQLAlchemy** | Provides the application's ORM/data-access abstraction. |
| 🧠 **CarePathState** | Carries the active context between LangGraph agents during a workflow. |
| 🤖 **LangGraph** | Coordinates agent execution and state transitions. |
| 📚 **ChromaDB / Vector Store** | Supports evidence retrieval for RAG workflows. |

```mermaid
flowchart LR

    PATIENT["👤 Patient"]

    API["⚡ FastAPI"]

    GRAPH["🤖 LangGraph"]

    STATE["🧠 CarePathState"]

    POSTGRES[("🗄️ PostgreSQL<br/>Persistent Data")]

    VECTOR[("📚 ChromaDB<br/>Evidence Retrieval")]

    PATIENT --> API

    API --> GRAPH

    GRAPH <--> STATE

    API --> POSTGRES
    GRAPH --> POSTGRES

    GRAPH --> VECTOR
```

> **PostgreSQL stores persistent healthcare data, while `CarePathState`
> carries active workflow context between agents. ChromaDB supports the
> evidence-retrieval layer rather than acting as the primary patient database.**

---

# 🔌 API Architecture & Endpoints

The CarePath backend exposes a RESTful API through FastAPI. The API layer
acts as the controlled entry point between the frontend, authentication
system, LangGraph workflows, AI services, and persistent data layer.

## API Request Architecture

```mermaid
flowchart LR

    CLIENT["🎨 React Frontend"]

    API["⚡ FastAPI"]

    AUTH["🔐 Authentication"]

    ROUTER["🛣️ API Routers"]

    SERVICE["⚙️ Service Layer"]

    GRAPH["🤖 LangGraph"]

    DB[("🗄️ PostgreSQL")]

    AI["🧠 AI Service Contracts"]

    CLIENT --> API
    API --> AUTH
    AUTH --> ROUTER

    ROUTER --> SERVICE

    SERVICE --> GRAPH
    SERVICE --> DB

    GRAPH --> AI
    GRAPH --> DB

    SERVICE --> API
    API --> CLIENT
```

---

## 📡 API Endpoint Categories

| Category | Purpose | Communication |
| :--- | :--- | :--- |
| 🔐 **Authentication** | User registration, login, token handling, and protected-resource access. | REST / JSON |
| 👤 **Patient** | Patient profile and healthcare-navigation information. | REST / JSON |
| 🩺 **Encounters** | Create and retrieve patient healthcare encounters. | REST / JSON |
| 📄 **Documents** | Upload and manage medical documents for downstream analysis. | REST / Multipart |
| 🤖 **AI Workflows** | Start and interact with LangGraph-powered healthcare workflows. | REST / JSON |
| 📡 **Workflow Streaming** | Stream active agent execution and workflow events to the frontend. | SSE |
| 🩺 **Referral** | Retrieve specialist-navigation results and referral information. | REST / JSON |
| 📝 **Care Plans** | Retrieve and manage personalized care-plan information. | REST / JSON |
| 💊 **Medication** | Access medication information and reminder-related workflows. | REST / JSON |
| 🔔 **Follow-up** | Manage follow-up activities and patient-care continuity. | REST / JSON |

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

# 🧩 Core Modules

CarePath AI follows a modular backend structure in which API handling,
workflow orchestration, AI capabilities, state management, schemas, and
data access remain separated.

## Backend Module Architecture

```mermaid
flowchart TD

    API["⚡ API Layer"]

    SCHEMAS["📋 Schemas<br/>Request / Response Models"]

    SERVICES["⚙️ Services<br/>Application Logic"]

    AGENTS["🤖 Agents<br/>LangGraph Nodes"]

    STATE["🧠 State<br/>CarePathState"]

    CONTRACTS["🔗 AI Service Contracts"]

    REPOSITORIES["🗂️ Repositories<br/>Data Access"]

    DB[("🗄️ PostgreSQL")]

    API --> SCHEMAS
    API --> SERVICES

    SERVICES --> AGENTS
    SERVICES --> REPOSITORIES

    AGENTS --> STATE
    AGENTS --> CONTRACTS

    REPOSITORIES --> DB
```

---

## 📂 Repository Structure

```text
CarePath-AI/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── ...
│   │
│   ├── package.json
│   └── vite.config.*
│
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── dependencies/
│   │   │
│   │   ├── agents/
│   │   │   ├── supervisor/
│   │   │   ├── safety/
│   │   │   ├── intake/
│   │   │   ├── reasoning/
│   │   │   ├── evidence/
│   │   │   ├── referral/
│   │   │   ├── care_plan/
│   │   │   └── follow_up/
│   │   │
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── state/
│   │   ├── repositories/
│   │   ├── models/
│   │   └── core/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── docs/
│
├── images/
│   └── carepath-ai-logo.png
│
├── docker-compose.yml
├── .env.example
└── README.md
```

> **Note:** Update the tree above to exactly match the repository before
> publishing the final README. The README should document the actual
> project structure rather than an intended future structure.

---

## 🧱 Module Responsibilities

| Module | Responsibility |
| :--- | :--- |
| ⚡ **API** | Defines HTTP endpoints, dependencies, authentication flow, and frontend-facing communication. |
| 🤖 **Agents** | Contains specialized LangGraph agent logic and workflow nodes. |
| 🧠 **State** | Defines the shared `CarePathState` used to transfer context between agents. |
| ⚙️ **Services** | Contains application-level orchestration and integration logic. |
| 📋 **Schemas** | Defines typed request, response, configuration, and structured AI data models. |
| 🔗 **AI Contracts** | Abstracts AI capabilities such as LLM, document analysis, vision, and evidence retrieval. |
| 🗂️ **Repositories** | Provides the data-access abstraction between application services and persistence. |
| 🗄️ **Models** | Defines database/ORM representations where applicable. |
| 🧪 **Tests** | Contains API, service, agent, integration, and workflow validation. |
| 🐳 **Infrastructure** | Provides containerization and environment-specific deployment configuration. |

---

# 🧪 Testing & Quality Assurance

CarePath AI follows a layered testing strategy designed to validate the
backend API, multi-agent workflows, service integrations, data handling,
and safety boundaries independently.

The goal is to ensure that changes to individual agents or services do
not silently break the overall healthcare-navigation workflow.

## Testing Architecture

```mermaid
flowchart TD

    TEST["🧪 Test Suite"]

    UNIT["🔬 Unit Tests"]

    API["⚡ API Tests"]

    AGENT["🤖 Agent Tests"]

    GRAPH["🧠 LangGraph Workflow Tests"]

    SERVICE["🔗 AI Service Contract Tests"]

    INTEGRATION["🔄 Integration Tests"]

    SAFETY["🛡️ Safety Tests"]

    E2E["🌐 End-to-End Tests"]

    UNIT --> TEST
    API --> TEST
    AGENT --> TEST
    GRAPH --> TEST
    SERVICE --> TEST
    INTEGRATION --> TEST
    SAFETY --> TEST
    E2E --> TEST

    TEST --> RESULT["📊 Test Results"]
```

---

## 🔬 Testing Layers

| Test Layer | What is validated |
| :--- | :--- |
| **Unit Testing** | Individual backend functions, utilities, validators, schemas, and isolated business logic. |
| **API Testing** | FastAPI endpoints, request validation, authentication, response structures, and error handling. |
| **Agent Testing** | Individual LangGraph agents and their state transformations are tested independently. |
| **Workflow Testing** | Supervisor routing, conditional transitions, shared `CarePathState`, workflow completion, and interruption paths. |
| **AI Service Contract Testing** | AI integrations are tested through controlled service contracts so agent logic is not dependent on live model responses. |
| **Integration Testing** | Validates communication between API, services, agents, repositories, and persistence layers. |
| **Safety Testing** | Validates safety-first routing, priority interruption, invalid-input handling, and protected workflow paths. |
| **End-to-End Testing** | Validates complete patient workflows from frontend/API input through agent execution and final response. |

---

## 🤖 LangGraph Workflow Testing

The multi-agent layer is tested around **state transitions and routing
behavior**, rather than treating an LLM response as a deterministic
assertion.

```mermaid
flowchart LR

    INPUT["Patient Input"]

    INITIAL["Initial CarePathState"]

    SUP["Supervisor"]

    AGENT["Specialized Agent"]

    UPDATED["Updated CarePathState"]

    NEXT{"Next Node?"}

    COMPLETE["Workflow Complete"]

    INPUT --> INITIAL
    INITIAL --> SUP
    SUP --> AGENT
    AGENT --> UPDATED
    UPDATED --> NEXT

    NEXT -->|Continue| SUP
    NEXT -->|Complete| COMPLETE
```

The workflow tests verify that:

- Required state is created correctly.
- The Supervisor routes to the appropriate capability.
- Agents update the shared state correctly.
- Conditional transitions behave as expected.
- Safety paths can interrupt normal execution.
- Human-review workflows can pause and resume.
- Workflow completion produces a structured result.

### Running Tests

From the backend project directory:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

For a specific test module:

```bash
pytest tests/<test_file>.py -v
```

For asynchronous tests:

```bash
pytest -v
```

The test suite should be executed before merging changes to backend
services, agent workflows, API contracts, or shared state definitions.

---

## 🔗 AI Service Isolation

AI capabilities are accessed through service contracts, allowing tests
to replace external model calls with deterministic test implementations
or mocks.

```mermaid
flowchart LR

    AGENT["🤖 LangGraph Agent"]

    CONTRACT["🔗 AI Service Contract"]

    REAL["✨ Real AI Provider"]

    MOCK["🧪 Mock / Test Implementation"]

    RESULT["📦 Structured Result"]

    AGENT --> CONTRACT

    CONTRACT --> REAL
    CONTRACT --> MOCK

    REAL --> RESULT
    MOCK --> RESULT

    RESULT --> AGENT
```

This separation allows the orchestration layer to be tested for routing,
state management, validation, and failure handling without requiring a
live external AI request for every test case.

---

## 🛡️ Safety & Failure Validation

Because CarePath AI operates in a healthcare-navigation context, testing
also considers failure and safety conditions.

| Scenario | Expected Behaviour |
| :--- | :--- |
| **Invalid Request** | Request is rejected through structured validation errors. |
| **Unauthorized Request** | Protected resources remain inaccessible. |
| **AI Service Failure** | Workflow handles the service failure without silently treating it as a successful result. |
| **Missing Patient Context** | Workflow requests or handles missing information rather than assuming unavailable data. |
| **Safety Signal** | Safety workflow takes priority over normal navigation. |
| **Human Review Required** | Workflow can pause and wait for clinician input where supported. |
| **Workflow Failure** | Failure is surfaced through controlled backend responses and streaming events where applicable. |
| **External Dependency Failure** | The system avoids presenting unavailable external information as confirmed results. |

> **Testing validates system behaviour and safety boundaries; it does not
> establish clinical efficacy or replace clinical validation.**



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


### 🔄 AI Workflow

```mermaid
flowchart TD

    START(["👤 Patient Request"])

    INTAKE["📥 Intake Agent<br/>Symptoms + Context"]

    SAFETY{"🛡️ Safety Agent<br/>Safety Check"}

    MEMORY["🧠 CarePath Memory<br/>Retrieve Patient Context"]

    DOCS["📄 Medical Documents Agent<br/>Reports + Prescriptions"]

    VISION["👁️ Vision Agent<br/>Supported Medical Images"]

    TIMELINE["🕐 Timeline Agent<br/>Build Healthcare Journey"]

    REASONING["🧩 Clinical Reasoning Agent<br/>Combine Patient Context"]

    EVIDENCE["📚 Evidence Agent<br/>RAG + Trusted Sources"]

    REFERRAL["🩺 Referral Agent<br/>Specialist Navigation"]

    DOCTOR["👨‍⚕️ Doctor Bridge<br/>Patient Brief + Questions"]

    REVIEW{"🤝 Clinician Review<br/>Required?"}

    CARE["📝 Care Plan Agent<br/>Personalized Next Steps"]

    MED["💊 Medication Agent<br/>Medication Workflow"]

    FOLLOW["🔔 Follow-up Agent<br/>Monitoring + Follow-up"]

    SUP["🤖 LangGraph Supervisor<br/>State + Agent Routing"]

    END(["✅ Structured CarePath Response"])


    START --> INTAKE

    INTAKE --> SUP

    SUP --> SAFETY

    SAFETY -->|Safety concern| END
    SAFETY -->|Continue| MEMORY

    MEMORY --> DOCS
    MEMORY --> VISION

    DOCS --> TIMELINE
    VISION --> TIMELINE

    TIMELINE --> REASONING

    REASONING --> EVIDENCE

    EVIDENCE --> REFERRAL

    REFERRAL --> DOCTOR

    DOCTOR --> REVIEW

    REVIEW -->|Yes| DOCTOR
    REVIEW -->|Approved / Continue| CARE

    CARE --> MED
    MED --> FOLLOW

    FOLLOW --> SUP

    SUP --> END
```

### Workflow Logic

```text
Patient Input
     ↓
Safety Check
     ↓
Retrieve Patient Context
     ↓
Analyze Documents / Images
     ↓
Build Patient Timeline
     ↓
Clinical Reasoning
     ↓
Evidence Retrieval (RAG)
     ↓
Specialist Navigation
     ↓
Doctor Interaction
     ↓
Human Review
     ↓
Personalized Care Plan
     ↓
Medication Support
     ↓
Follow-up Intelligence
     ↓
Updated Patient Context
```

The workflow is **state-driven rather than a fixed linear pipeline**.  
The LangGraph Supervisor evaluates the current patient state and routes
execution to the relevant specialized agent. Agents update the shared
workflow state, allowing subsequent decisions to use the accumulated
context.
---

### ⚙️ Backend Architecture

```mermaid
flowchart TD

    CLIENT["🎨 React Frontend"]

    API["⚡ FastAPI API Gateway"]

    AUTH["🔐 Authentication<br/>JWT + Authorization"]

    ROUTER["🛣️ API Routers"]

    SERVICE["⚙️ Backend Service Layer"]

    VALIDATION["✅ Pydantic<br/>Validation"]

    GRAPH["🤖 LangGraph Supervisor"]

    STATE["🧠 CarePathState<br/>Shared Workflow State"]

    AGENTS["🧩 Specialized Agents"]

    CONTRACTS["🔗 AI Service Contracts"]

    GEMINI["✨ Gemini / LLM"]

    OCR["📄 OCR / Document Intelligence"]

    VISION["👁️ Computer Vision"]

    RAG["📚 Evidence / RAG"]

    DB["🗄️ PostgreSQL"]

    SSE["📡 SSE Streaming"]

    ERROR["⚠️ Error Handling<br/>Structured Responses"]

    CLIENT -->|HTTP / JSON| API

    API --> AUTH

    AUTH --> ROUTER

    ROUTER --> VALIDATION

    VALIDATION --> SERVICE

    SERVICE --> GRAPH

    SERVICE --> DB

    GRAPH --> STATE

    STATE --> AGENTS

    AGENTS --> CONTRACTS

    CONTRACTS --> GEMINI
    CONTRACTS --> OCR
    CONTRACTS --> VISION
    CONTRACTS --> RAG

    AGENTS --> STATE

    STATE --> GRAPH

    GRAPH --> SERVICE

    SERVICE --> SSE

    SSE --> CLIENT

    API --> ERROR
    SERVICE --> ERROR
    GRAPH --> ERROR
```

### Backend Request Lifecycle

```mermaid
sequenceDiagram

    participant UI as React Frontend
    participant API as FastAPI
    participant AUTH as Auth Layer
    participant SERVICE as Service Layer
    participant GRAPH as LangGraph
    participant AGENT as AI Agent
    participant AI as AI Service
    participant DB as PostgreSQL

    UI->>API: HTTP Request

    API->>AUTH: Validate JWT
    AUTH-->>API: Authorized User

    API->>SERVICE: Validated Request

    SERVICE->>DB: Retrieve Patient Context
    DB-->>SERVICE: Patient Data

    SERVICE->>GRAPH: Start Workflow

    GRAPH->>AGENT: Route Task

    AGENT->>AI: Execute AI Capability
    AI-->>AGENT: Structured Result

    AGENT-->>GRAPH: Update CarePathState

    GRAPH-->>SERVICE: Workflow Result

    SERVICE->>DB: Persist Result

    SERVICE-->>API: Structured Response

    API-->>UI: JSON / SSE Events
```

### Backend Responsibilities

| Component | Technical Responsibility |
| :--- | :--- |
| ⚡ **FastAPI API Gateway** | Exposes REST endpoints and acts as the entry point between the frontend and backend services. |
| 🔐 **Authentication Layer** | Validates JWT credentials and controls access to protected resources. |
| 🛣️ **API Routers** | Organize endpoints by functional area while keeping HTTP concerns separate from business logic. |
| ⚙️ **Service Layer** | Contains backend application logic and coordinates database and LangGraph operations. |
| ✅ **Pydantic Validation** | Validates incoming requests and structures outgoing API responses. |
| 🤖 **LangGraph Engine** | Executes stateful multi-agent workflows and controls conditional agent routing. |
| 🧠 **CarePathState** | Maintains shared context exchanged between agents during a workflow. |
| 🔗 **AI Service Contracts** | Provide provider-independent interfaces for LLM, OCR, vision, and evidence capabilities. |
| 🗄️ **PostgreSQL** | Stores persistent patient, encounter, document, workflow, and care-related data handled by the backend. |
| 📡 **SSE Streaming** | Sends real-time workflow events from backend execution to the frontend. |
| ⚠️ **Error Handling** | Converts validation, service, AI, and workflow failures into controlled API responses. |
---

# 🗄 Database Architecture

---

# 🗄️ Database Architecture

CarePath AI uses a structured relational data layer to maintain patient
context, healthcare encounters, documents, medications, care plans,
referrals, timelines, and follow-up information.

The database acts as the persistent source of truth for the patient's
healthcare journey, while LangGraph maintains workflow state during
agent execution.

## Entity Relationship Architecture

```mermaid
erDiagram

    USER ||--o| PATIENT : "has profile"

    PATIENT ||--o{ ENCOUNTER : "has"
    PATIENT ||--o{ MEDICAL_DOCUMENT : "uploads"
    PATIENT ||--o{ MEDICATION : "uses"
    PATIENT ||--o{ REFERRAL : "receives"
    PATIENT ||--o{ CARE_PLAN : "has"
    PATIENT ||--o{ FOLLOW_UP : "requires"
    PATIENT ||--o{ TIMELINE_EVENT : "generates"

    ENCOUNTER ||--o{ MEDICAL_DOCUMENT : "contains"
    ENCOUNTER ||--o{ REFERRAL : "produces"

    MEDICAL_DOCUMENT ||--o{ DOCUMENT_EXTRACTION : "produces"

    REFERRAL ||--o{ DOCTOR_REVIEW : "reviewed through"

    CARE_PLAN ||--o{ CARE_PLAN_ITEM : "contains"

    MEDICATION ||--o{ MEDICATION_REMINDER : "has"

    USER {
        uuid id PK
        string email
        string role
        datetime created_at
    }

    PATIENT {
        uuid id PK
        uuid user_id FK
        string name
        date date_of_birth
        string preferences
        datetime created_at
    }

    ENCOUNTER {
        uuid id PK
        uuid patient_id FK
        string encounter_type
        string summary
        datetime occurred_at
    }

    MEDICAL_DOCUMENT {
        uuid id PK
        uuid patient_id FK
        uuid encounter_id FK
        string document_type
        string file_location
        datetime uploaded_at
    }

    DOCUMENT_EXTRACTION {
        uuid id PK
        uuid document_id FK
        string extraction_type
        json extracted_data
        float confidence
    }

    MEDICATION {
        uuid id PK
        uuid patient_id FK
        string medication_name
        string dosage
        string frequency
        string instructions
    }

    MEDICATION_REMINDER {
        uuid id PK
        uuid medication_id FK
        string schedule
        boolean active
    }

    REFERRAL {
        uuid id PK
        uuid patient_id FK
        uuid encounter_id FK
        string specialist
        string reason
        float confidence
        string status
    }

    DOCTOR_REVIEW {
        uuid id PK
        uuid referral_id FK
        string reviewer
        string feedback
        datetime reviewed_at
    }

    CARE_PLAN {
        uuid id PK
        uuid patient_id FK
        string title
        string status
        datetime created_at
    }

    CARE_PLAN_ITEM {
        uuid id PK
        uuid care_plan_id FK
        string action
        string status
        datetime due_at
    }

    FOLLOW_UP {
        uuid id PK
        uuid patient_id FK
        string type
        datetime scheduled_at
        string status
    }

    TIMELINE_EVENT {
        uuid id PK
        uuid patient_id FK
        string event_type
        string description
        datetime occurred_at
    }
```

## Data Flow

```mermaid
flowchart LR

    USER["👤 User"]

    PATIENT["🧑 Patient Profile"]

    ENCOUNTER["🩺 Encounters"]

    DOCUMENTS["📄 Medical Documents"]

    EXTRACTION["🔍 Document Extraction"]

    MEDICATION["💊 Medications"]

    REFERRAL["🩺 Referrals"]

    REVIEW["👨‍⚕️ Doctor Review"]

    CARE["📝 Care Plans"]

    FOLLOWUP["🔔 Follow-ups"]

    TIMELINE["🕐 Patient Timeline"]

    DB[("PostgreSQL")]

    USER --> PATIENT

    PATIENT --> ENCOUNTER
    PATIENT --> DOCUMENTS
    PATIENT --> MEDICATION
    PATIENT --> REFERRAL
    PATIENT --> CARE
    PATIENT --> FOLLOWUP
    PATIENT --> TIMELINE

    DOCUMENTS --> EXTRACTION

    REFERRAL --> REVIEW

    ENCOUNTER --> TIMELINE
    DOCUMENTS --> TIMELINE
    MEDICATION --> TIMELINE
    REFERRAL --> TIMELINE
    CARE --> TIMELINE
    FOLLOWUP --> TIMELINE

    PATIENT --> DB
    ENCOUNTER --> DB
    DOCUMENTS --> DB
    EXTRACTION --> DB
    MEDICATION --> DB
    REFERRAL --> DB
    REVIEW --> DB
    CARE --> DB
    FOLLOWUP --> DB
    TIMELINE --> DB
```

## Database Responsibilities

| Component | Responsibility |
| :--- | :--- |
| 👤 **User & Patient Data** | Stores authenticated user information and the associated patient profile. |
| 🩺 **Encounter Data** | Maintains consultation and healthcare interaction records. |
| 📄 **Medical Documents** | Stores document metadata and references to uploaded medical files. |
| 🔍 **Document Extraction** | Stores structured information produced from supported document-analysis workflows. |
| 💊 **Medication Data** | Maintains patient-confirmed medication information used by medication workflows. |
| 🩺 **Referral Data** | Stores specialist-navigation results, rationale, confidence, and status. |
| 👨‍⚕️ **Doctor Review** | Persists clinician feedback and human-in-the-loop review information. |
| 📝 **Care Plans** | Stores personalized care plans and their individual action items. |
| 🔔 **Follow-ups** | Maintains scheduled follow-up activities and their status. |
| 🕐 **Patient Timeline** | Provides a persistent chronological representation of the patient's healthcare journey. |

### Persistence Principle

```text
                    ┌──────────────────────┐
                    │    Patient Context   │
                    └──────────┬───────────┘
                               ↓
              ┌────────────────────────────────┐
              │           PostgreSQL            │
              ├────────────────────────────────┤
              │ Encounters                      │
              │ Documents                       │
              │ Medications                     │
              │ Referrals                       │
              │ Doctor Reviews                  │
              │ Care Plans                      │
              │ Follow-ups                      │
              │ Timeline Events                 │
              └────────────────────────────────┘
                               ↑
                               │
                    ┌──────────┴───────────┐
                    │   Backend Services   │
                    │   + LangGraph        │
                    └──────────────────────┘
```

> **PostgreSQL provides persistent healthcare data, while LangGraph manages
> transient workflow state during multi-agent execution.**

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

CarePath AI transforms fragmented patient information into a continuous,
context-aware healthcare navigation workflow.

```mermaid
flowchart TD

    PATIENT(["👤 Patient"])

    INPUT["📥 Patient Input<br/>Symptoms • History • Questions"]

    UPLOAD["📄 Documents & Images<br/>Reports • Prescriptions"]

    API["⚡ FastAPI API Layer"]

    INTAKE["📋 Intake Agent<br/>Structure Patient Information"]

    MEMORY["🧠 CarePath Memory<br/>Retrieve Relevant Context"]

    SUP["🤖 LangGraph Supervisor<br/>Coordinate Agent Workflow"]

    RECORDS["📄 Medical Records Agent"]

    VISION["👁️ Vision Agent"]

    TIMELINE["🕐 Timeline Agent"]

    SAFETY["🛡️ Safety Agent"]

    REASONING["🧩 Clinical Reasoning Agent"]

    EVIDENCE["📚 Evidence Agent<br/>RAG + Trusted Sources"]

    REFERRAL["🩺 Explainable Referral<br/>Specialist Navigation"]

    DOCTOR["👨‍⚕️ Doctor Bridge<br/>Summary + Case Questions"]

    REVIEW{"👨‍⚕️ Expert Review<br/>Required?"}

    CARE["📝 Personalized Care Plan"]

    MEDICATION["💊 Medication Companion"]

    FOLLOWUP["🔔 Follow-up Intelligence"]

    TIMELINE_OUT["🕐 AI Patient Timeline"]

    DB[("🗄️ PostgreSQL")]

    DASHBOARD["📊 CarePath Dashboard"]

    PATIENT --> INPUT
    PATIENT --> UPLOAD

    INPUT --> API
    UPLOAD --> API

    API --> INTAKE

    INTAKE --> MEMORY

    MEMORY --> SUP

    SUP --> RECORDS
    SUP --> VISION
    SUP --> TIMELINE
    SUP --> SAFETY

    RECORDS --> SUP
    VISION --> SUP
    TIMELINE --> SUP
    SAFETY --> SUP

    SUP --> REASONING

    REASONING --> EVIDENCE
    EVIDENCE --> REASONING

    REASONING --> REFERRAL

    REFERRAL --> DOCTOR

    DOCTOR --> REVIEW

    REVIEW -->|Yes| DOCTOR
    REVIEW -->|Continue| CARE

    CARE --> MEDICATION
    MEDICATION --> FOLLOWUP

    FOLLOWUP --> SUP

    SUP --> TIMELINE_OUT

    MEMORY --> DB
    TIMELINE_OUT --> DB
    REFERRAL --> DB
    DOCTOR --> DB
    CARE --> DB
    MEDICATION --> DB
    FOLLOWUP --> DB

    DB --> DASHBOARD
    TIMELINE_OUT --> DASHBOARD
    CARE --> DASHBOARD
    FOLLOWUP --> DASHBOARD

    DASHBOARD --> PATIENT
```

### 🔁 Data Transformation

```mermaid
flowchart LR

    A["Raw Patient Information"]
    B["Structured Patient Context"]
    C["Shared CarePath State"]
    D["AI Analysis + Evidence"]
    E["Specialist Navigation"]
    F["Doctor Review"]
    G["Personalized Care"]
    H["Continuous Follow-up"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> C
```

### Core Data Flow

```text
Patient Input
      ↓
FastAPI
      ↓
Patient Context
      ↓
CarePath Memory
      ↓
LangGraph Supervisor
      ↓
Specialized Agents
      ↓
Clinical Reasoning
      ↓
Evidence / RAG
      ↓
Explainable Referral
      ↓
Doctor Bridge
      ↓
Personalized Care Plan
      ↓
Medication + Follow-up
      ↓
Patient Timeline
      ↓
Dashboard
      ↓
Continuous Care
```

> **The key distinction is that CarePath is not a one-way pipeline. Follow-up information and new patient interactions are fed back into the patient's persistent context, allowing subsequent workflows to build on the existing healthcare journey.**



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

# 💼 Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 19, TypeScript, Vite, React Router |
| **UI & Visualization** | Tailwind CSS 4, Lucide React, Recharts, Motion, React Markdown |
| **Backend API** | Python 3.13, FastAPI, Uvicorn, Pydantic |
| **Multi-Agent Orchestration** | LangGraph, LangChain Core |
| **AI & Language** | Google Gemini, structured AI service contracts, medical NLP workflows |
| **Document Intelligence** | EasyOCR, OCR service contracts, document parsing |
| **Computer Vision** | PyTorch, vision service contracts |
| **Evidence & RAG** | ChromaDB, vector retrieval, Evidence Agent |
| **Data Layer** | PostgreSQL, SQLAlchemy, AsyncPG, Alembic |
| **Workflow Communication** | Server-Sent Events (SSE), REST APIs |
| **Authentication & Security** | JWT, password hashing, authorization controls |
| **Validation & Configuration** | Pydantic, Pydantic Settings |
| **Testing** | Pytest, pytest-asyncio, API tests, LangGraph workflow tests |
| **Infrastructure** | Docker, environment-based configuration |
| **Logging & Observability** | Structlog |

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
