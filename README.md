# ResumeForge AI

An AI-powered resume tailoring platform that customises resumes against a Job Description using deterministic parsing, semantic retrieval, local LLMs, and automated PDF rendering — built without relying on black-box generation.

> JD parsing and normalisation run locally via Ollama + Llama 3.2. Resume section generation uses Groq API.

---

## What It Does

Most resume tools either ask you to write everything yourself or hand everything to a black-box AI. ResumeForge AI does neither.

It maintains a structured record of your professional profile — skills, projects, experience, education, achievements — and when you upload a JD, it understands what the role needs, retrieves the most relevant parts of your profile, and generates a tailored, ATS-optimised resume section by section.

The result is a resume that is genuinely yours, reframed intelligently for each role.

---

## System Architecture

The platform runs two independent tracks after JD parsing:

```
                        JD PDF
                          │
                          ▼
                    PDF Parser (pypdf)
                    generates output.txt
                          │
                          ▼
              RegEx Section Extractor
              raw_jd_sections.json
                          │
                          ▼
            LLM JD Normalizer (Llama 3.2)
            normalized_jd_sections.json
                          │
              ┌───────────┴────────────┐
              │                        │
              ▼                        ▼
   ┌──────────────────┐    ┌─────────────────────────┐
   │  FAISS Semantic  │    │   Resume Writing        │
   │  Matching Engine │    │   Pipeline              │
   │                  │    │                         │
   │  JD + User       │    │  resume_builder.py      │
   │  Profile         │    │  calls section scripts  │
   │                  │    │  one by one:            │
   │  Output:         │    │  skills.py              │
   │  JD-Profile      │    │  experience.py          │
   │  Match %         │    │  projects.py  ...       │
   └──────────────────┘    │        │                │
                           │        ▼                │
                           │  Each script fetches:   │
                           │  - JD section (JSON)    │
                           │  - User section (DB)    │
                           │  - Calls Groq LLM       │
                           │  - Returns plain text   │
                           │        │                │
                           │        ▼                │
                           │  Resume JSON Schema     │
                           │  (filled section-wise)  │
                           │        │                │
                           │        ▼                │
                           │  Jinja2 + LaTeX → .tex  │
                           │        │                │
                           │        ▼                │
                           │  pdflatex → PDF         │
                           └─────────────────────────┘
```

---

## Pipeline in Detail

### Stage 1 — JD Parsing
- `pypdf` extracts raw text from the uploaded JD PDF
- Output saved as `output.txt`

### Stage 2 — Section Extraction
- RegEx-based heading detection splits JD into semantic sections
- Output saved as `raw_jd_sections.json`

### Stage 3 — LLM Normalisation
- Llama 3.2 (via Ollama, running locally) normalises raw sections
- Maps JD content into resume-relevant categories
- Output saved as `normalized_jd_sections.json`

### Track A — Semantic Matching (Evaluation Only)
- FAISS + Sentence Transformers compares JD against user profile
- Returns a JD-to-profile match percentage
- Used for insight and scoring — not part of resume writing

### Track B — Resume Writing
- `resume_builder.py` orchestrates section-wise generation
- For each resume section, calls a dedicated script (`skills.py`, `experience.py`, etc.)
- Each script fetches its relevant slice from `normalized_jd_sections.json` and the user's MySQL profile
- Builds a system prompt + human prompt and calls Groq LLM
- Receives plain formatted text back (e.g. categorised skill bullets)
- `resume_builder.py` fills each response into the canonical Resume JSON Schema
- Once all sections are filled, the JSON is passed to the rendering pipeline

### Stage 4 — Rendering
- Jinja2 templates render the JSON into a `.tex` file
- `pdflatex` compiles the `.tex` into a final PDF resume

---

## Features

### JD Understanding
- PDF parsing with unicode-safe text extraction
- RegEx + semantic heading detection for section splitting
- Local LLM normalisation into structured resume-relevant JSON
- ATS keyword preservation throughout

### Professional Profile System
Maintains a persistent, structured profile per user across 8 sections:
- Personal Information
- Education
- Experience
- Projects
- Technical Skills
- Key Courses Taken
- Positions of Responsibility
- Achievements

### Semantic Matching (Evaluation)
- FAISS vector search + Sentence Transformer embeddings
- Scores user profile relevance against a given JD
- Helps users understand how well their profile fits a role

### Resume Generation
- Section-wise LLM prompting via Groq for controllable output
- Each section script is independent and focused
- All output assembled into a canonical JSON schema
- Schema is the single contract between generator and renderer

### Resume Rendering
- Jinja2 templating over LaTeX resume templates
- Automated PDF compilation via `pdflatex`

### User Interface
- Streamlit multi-page app — Login → Profile → Upload
- New user: guided section-by-section onboarding
- Returning user: sidebar navigation with inline edit and delete
- Full CRUD across all 8 profile sections
- JD upload saved to per-user local folder

---

## Tech Stack

| Layer | Tools |
|---|---|
| AI / NLP | Llama 3.2, Ollama, LangChain, Groq API |
| Vector Search | FAISS, Sentence Transformers |
| Parsing | pypdf, RegEx |
| Rendering | Jinja2, LaTeX, pdflatex |
| Database | MySQL |
| UI | Streamlit |
| Schema | Pydantic |
| Config | python-dotenv |

---

## Repository Structure

```
/ResumeForgeAI
│
├── app.py                          # Streamlit entry point
│
├── pages/
│   ├── 1_login.py                  # Name-based login
│   ├── 2_profile.py                # Profile CRUD interface
│   └── 3_upload.py                 # JD PDF upload + pipeline trigger
│
├── user/
│   ├── db/
│   │   ├── db_connect.py           # MySQL connection helper
│   │   ├── db_setup.py             # One-time DB and table creation
│   │   └── db_queries.py           # All DB read/write operations
│   └── {username}/
│       ├── uploads/                # Uploaded JD PDFs
│       └── outputs/                # Generated resume PDFs
│
├── parsers/
│   └── parse.py                    # JD PDF parser → output.txt
│
├── extractors/
│   └── section_extractor.py        # RegEx section extraction → raw_jd_sections.json
│
├── normalizers/
│   └── normalize_sections.py       # LLM normalisation → normalized_jd_sections.json
│
├── LLM/                            # Section-wise Groq LLM scripts
│   ├── skills.py
│   ├── experience.py
│   ├── projects.py
│   └── ...
│
├── resume_builder.py               # Orchestrates section scripts → fills JSON schema
│
├── schema/
│   └── resume_schema.py            # Canonical Pydantic resume JSON schema
│
├── renderers/                      # Jinja2 + LaTeX rendering pipeline
│
├── templates/                      # LaTeX resume templates
│
├── prompts/
│   ├── section_normalizer_system.txt
│   └── section_normalizer_human.txt
│
├── processing_files/
│   ├── output.txt                  # Raw JD text
│   ├── raw_jd_sections.json        # Extracted JD sections
│   └── normalized_jd_sections.json # LLM-normalised JD
│
├── .env.example
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Vedansh7-7/ResumeForgeAI
cd ResumeForgeAI
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install langchain langchain-community langchain-ollama ollama
pip install sentence-transformers faiss-cpu pypdf jinja2
pip install streamlit mysql-connector-python python-dotenv pydantic
pip install groq
```

### 4. Install Ollama and pull model as well as get an Groq API key

Download from [ollama.com](https://ollama.com), then:

```bash
ollama pull llama3.2
```

for groq API key visit: [Groq API](https://console.groq.com/keys)

### 5. Set up MySQL

Run the setup script once:

```bash
python user/db/db_setup.py
```

### 6. Configure environment

Copy `.env.example` to `.env` and fill in your credentials:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=resume_platform
GROQ_API_KEY=your_groq_api_key
```

### 7. Run the app

```bash
streamlit run app.py
```

---

## Current Status

| Component | Status |
|---|---|
| JD PDF Parser | Done |
| RegEx Section Extractor | Done |
| LLM JD Normaliser (Llama 3.2) | Done |
| User Profile System (DB + UI) | Done |
| Semantic Matching (FAISS) | In Progress |
| Section-wise Resume Generator (Groq) | Done |
| Resume JSON Schema | Done |
| LaTeX Renderer | Done |
| PDF Compilation | Done |

---

## Design Philosophy

This project is built on the principle that resume generation should be **deterministic where possible, AI-assisted where valuable**.

Rather than feeding everything to a single LLM prompt, the pipeline is broken into explicit, auditable stages — each with a clear input and output. The JD parsing, section extraction, retrieval, and rendering layers are all rule-based and inspectable. LLMs are used only where natural language understanding and generation genuinely add value: normalising JD text and rewriting resume content for a specific role.

This makes the system easier to debug, improve, and trust.

---

## Roadmap

- Interactive resume editor
- Multiple LaTeX resume templates
- Resume scoring against JD
- Cover letter generation
- Resume versioning per JD
- FastAPI backend
- Web dashboard

---

## License

MIT License