# AI Resume Tailor

An AI-powered resume tailoring platform that intelligently customizes resumes according to a Job Description (JD) using semantic parsing, retrieval systems, local LLMs, and dynamic resume rendering.

The system parses a JD PDF, understands its semantic requirements, compares them against a user's professional profile, retrieves the most relevant experiences/projects/skills, and generates an ATS-optimized customized resume in real time.

---

# Features

## Intelligent JD Understanding
- PDF Job Description parsing
- Unicode-safe text extraction
- Regex + semantic heading detection
- LLM-powered JD normalization
- ATS keyword preservation

---

## User Professional Profile System
The platform maintains a structured professional profile for users, including:
- Education
- Experiences
- Projects
- Skills
- Positions of Responsibility
- Achievements
- Certifications
- Resume Variants

The system acts like a professional memory engine for the user.

---

## Resume Tailoring Engine
The application:
- Understands role requirements
- Matches relevant experiences/projects
- Retrieves strongest ATS keywords
- Tailors resume sections dynamically
- Optimizes descriptions for the target role

---

## Local AI Pipeline
Runs fully locally using:
- Ollama
- Llama 3.2
- LangChain

No external API dependency required.

---

## Semantic Retrieval System
The system uses:
- Embeddings
- Similarity search
- Retrieval pipelines

to identify:
- relevant projects
- relevant experiences
- matching technical skills
- leadership indicators
- achievement alignment

---

## Dynamic Resume Rendering
Users can:
- choose resume templates
- edit generated content
- preview resumes live
- export resumes as PDF

Rendering pipeline:
- JSON Resume Schema
- LaTeX template generation
- PDF compilation

---

# System Architecture

```text
                           ┌────────────────────┐
                           │   User Profile DB  │
                           │                    │
                           │ Skills             │
                           │ Projects           │
                           │ Experience         │
                           │ Education          │
                           │ Achievements       │
                           └─────────┬──────────┘
                                     │
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │ Embedding + Retrieval   │
                        │ Semantic Matching       │
                        └──────────┬──────────────┘
                                   │
                                   │
                                   ▼
┌──────────────┐        ┌─────────────────────────┐
│ JD PDF Input │ ───▶  │ PDF Parser              │
└──────────────┘        │ pypdf                   │
                        └──────────┬──────────────┘
                                   │
                                   ▼
                        ┌─────────────────────────┐
                        │ Regex Section Extractor │
                        │ Semantic Grouping       │
                        └──────────┬──────────────┘
                                   │
                                   ▼
                        ┌─────────────────────────┐
                        │ LLM JD Normalizer       │
                        │ ChatOllama + Llama3.2   │
                        └──────────┬──────────────┘
                                   │
                                   ▼
                        ┌─────────────────────────┐
                        │ Resume-Oriented JSON    │
                        └──────────┬──────────────┘
                                   │
                                   ▼
                        ┌─────────────────────────┐
                        │ Resume Generator        │
                        │ Section-wise Generation │
                        └──────────┬──────────────┘
                                   │
                                   ▼
                        ┌─────────────────────────┐
                        │ LaTeX Renderer          │
                        │ PDF Compilation         │
                        └──────────┬──────────────┘
                                   │
                                   ▼
                           ┌────────────────┐
                           │ Final Resume   │
                           │ ATS Optimized  │
                           └────────────────┘
```

---

# Resume Schema

The system internally uses a structured resume-oriented schema:

```json
{
  "personal_information": "",
  "education": "",
  "experience": "",
  "projects": "",
  "technical_skills": [],
  "key_courses_taken": "",
  "positions_of_responsibility": "",
  "achievements": ""
}
```

---

# JD Normalization Schema

Job Descriptions are normalized into semantic resume-tailoring sections:

```json
{
  "technical_skills": [],
  "experience": "",
  "projects": "",
  "positions_of_responsibility": "",
  "achievements": ""
}
```

---

# Tech Stack

## AI / NLP
- LangChain
- Ollama
- Llama 3.2
- SentenceTransformers

---

## Backend
- Python
- FastAPI (planned)

---

## Storage
- PostgreSQL (planned)
- Redis (planned)
- JSON pipelines

---

## Parsing & Rendering
- pypdf
- Regex
- LaTeX
- Jinja2

---

## Vector Search
- FAISS

---

# Repository Structure

```text
/project-root
│
├── pdf/
│
├── processing_files/
│   ├── output.txt
│   ├── raw_jd_sections.json
│   └── normalized_jd.json
│
├── prompts/
│   ├── section_normalizer_system.txt
│   └── section_normalizer_human.txt
│
├── parsers/
│   └── parse.py
│
├── extractors/
│   └── section_extractor.py
│
├── normalizers/
│   └── normalize_sections.py
│
├── renderers/
│
├── schemas/
│
├── templates/
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repo-url>
cd ai-resume-tailor
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install langchain
pip install langchain-community
pip install langchain-ollama
pip install ollama
pip install sentence-transformers
pip install faiss-cpu
pip install pypdf
pip install jinja2
```

---

# Install Ollama

Install locally:

:contentReference[oaicite:0]{index=0}

Pull model:

```bash
ollama pull llama3.2
```

---

# Current Pipeline

## 1. Parse JD PDF

```bash
python parse.py
```

Extracts clean raw text from Job Description PDFs.

---

## 2. Extract Semantic Sections

```bash
python section_extractor.py
```

Creates raw semantic JD section JSON.

---

## 3. Normalize JD Sections

```bash
python normalize_sections.py
```

Uses local LLM pipelines to generate structured resume-oriented semantic JSON.

---

## 4. Retrieve Relevant User Content

Retrieval system identifies:
- relevant projects
- relevant experiences
- matching skills
- ATS alignment

---

## 5. Generate Resume

The system generates:
- tailored experiences
- optimized project descriptions
- ATS-friendly skill sections
- role-specific resume variants

---

## 6. Render Resume

Resume JSON is transformed into:
- LaTeX
- PDF
- editable resume previews

---

# Design Philosophy

This project intentionally combines:
- deterministic pipelines
- regex extraction
- semantic retrieval
- structured prompting
- local LLM orchestration

instead of relying purely on black-box AI generation.

The goal is to build:
- reliable,
- explainable,
- ATS-aware,
- scalable

resume intelligence systems.

---

# Future Roadmap

- Interactive resume editor
- Multiple resume templates
- Recruiter-mode optimization
- Resume scoring engine
- Cover letter generation
- AI interview preparation
- Multi-user profile memory
- Web dashboard
- Real-time collaboration
- Resume versioning

---

# License

MIT License