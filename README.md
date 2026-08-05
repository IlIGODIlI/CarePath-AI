# CarePath-AI

**Autonomous Multi-Agent Healthcare Navigation System & Architecture Command Center**

## Overview
CarePath-AI is an autonomous multi-agent healthcare navigation system. This repository contains the architecture command center, LangGraph agent simulator, API contract explorer, database schema viewer, and backend integration.

## Getting Started

### 1. Frontend & Command Center
**Prerequisites:** Node.js

1. Install dependencies:
   ```bash
   npm install
   ```
2. Configure environment variables in `.env` or `.env.example`:
   Set `GEMINI_API_KEY` and backend URLs as needed.
3. Start local development server:
   ```bash
   npm run dev
   ```

### 2. Backend & Agent Engine
**Prerequisites:** Python 3.10+

1. Navigate to backend directory:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

