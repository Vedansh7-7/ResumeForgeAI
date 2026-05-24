from LLM.skills import get_skills_section
from LLM.experience import get_experience_section
import json, os

# Load the already-existing JSON
with open("processing_files/normalized_jd_sections.json", "r", encoding="utf-8") as f:
    jd = json.load(f)

jd_skills     = jd.get("technical_skills", "")
jd_experience = jd.get("experience", "")
jd_general    = jd.get("general", "")

USER_SKILLS = """
Programming: Python, C++, Verilog
Tools & Frameworks: CustomTkinter, Matplotlib, Numpy, Pandas,
SciPy, Apache Spark, FAISS, PySpark
Databases & Data Platforms: Databricks, Delta Lake
Operating Systems: Windows, Linux
Data Analysis and ML: ROOT (CERN), RAG, Bayesian inference,
Feature engineering
"""

USER_EXPERIENCE = """
Research Intern | IIT Indore | Jan 2025 – Present
Worked on Landsat 8 multispectral imagery analysis using Python and Rasterio.
Processed satellite data for urban land cover classification.

Project: Kirana AI Assistant | BharatBricks Hackathon | 2025
Built mobile-first POS and inventory management app using Databricks free tier.
Implemented K-Means clustering for reorder alerts and AI-driven insights.
"""

print("===== SKILLS SECTION =====")
print(get_skills_section(jd_skills, USER_SKILLS, jd_general))

print("\n===== EXPERIENCE SECTION =====")
print(get_experience_section(jd_experience, USER_EXPERIENCE, jd_general))