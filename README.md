# AI Resume Tailor

An AI-powered resume tailoring system that parses Job Descriptions (JDs), extracts resume-relevant signals, matches them against a user's professional profile, and generates customized ATS-friendly resumes.

---

# Overview

This project aims to automate resume customization using:
- PDF parsing
- Semantic section extraction
- LLM-based JD normalization
- Retrieval-based project/experience matching
- Resume generation
- LaTeX-based rendering

Instead of generating resumes blindly, the system understands the semantic intent of a job description and adapts the user's existing profile accordingly.

---

# Current Features

## JD Parsing
- Extract text from PDF Job Descriptions
- Page-wise parsing using `pypdf`
- Unicode-safe text cleaning

## Section Extraction
- Regex-based heading detection
- Semantic grouping of JD sections
- Raw section preservation

## LLM-Powered Normalization
Using:
- Ollama
- Llama 3.2
- LangChain

The system converts messy JD content into a normalized resume-oriented schema.

Example normalized output:

```json
{
  "technical_skills": [],
  "experience": "",
  "projects": "",
  "positions_of_responsibility": "",
  "achievements": ""
}