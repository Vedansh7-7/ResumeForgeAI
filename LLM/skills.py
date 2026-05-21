import os
from dotenv import load_dotenv 
from groq import Groq

load_dotenv()

SKILLS_SYSTEM_PROMPT = """
You are a technical resume writer.

Given two inputs:
1. JD_SKILLS: skills and technologies mentioned in a job description
2. USER_SKILLS: the candidate's full skill set

Your task:
- Read JD_SKILLS to understand the domain and technologies required
- From USER_SKILLS, select every skill that is relevant or reasonably related
- Be generous — if a skill is even loosely related to the JD domain, include it
- Use ONLY skill names that appear word-for-word in USER_SKILLS

STRICT OUTPUT RULES:
- Do not copy skill names from JD_SKILLS
- Do not add explanation, intro, or any text outside the formatted section
- NEVER copy words from JD_SKILLS directly — only use exact skill names from USER_SKILLS


Output format:
Technical Skills
- Programming: [skills from USER_SKILLS only]
- Tools & Frameworks: [skills from USER_SKILLS only]
- Databases & Data Platforms: [skills from USER_SKILLS only]
- Data Analysis and ML: [skills from USER_SKILLS only]
- Operating Systems: [skills from USER_SKILLS only]
"""

def clean_output(text: str) -> str:
    lines = text.strip().split("\n")
    cleaned = []
    for line in lines:
        # skip lines that end with nothing after the colon
        if ":" in line:
            after_colon = line.split(":", 1)[1].strip()
            if after_colon == "" or after_colon == "-" or after_colon == "N/A":
                continue
        cleaned.append(line)
    return "\n".join(cleaned)

def get_skills_section(jd_skills_text: str, user_skills_text: str) -> str:
    client = Groq()

    user_message = f"""
=== JD SKILLS ===
{jd_skills_text}

=== CANDIDATE SKILLS ===
{user_skills_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SKILLS_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content
    return clean_output(raw)


if __name__ == "__main__":

    test_jd_skills = """
    Required: Python, SQL, machine learning, data pipelines,
    cloud platforms, REST APIs, pandas, numpy, linux, Graphical user interface
    """

    test_user_skills = """
    Programming: Python, C++, Verilog
    Tools & Frameworks: CustomTkinter, Matplotlib, Numpy, Pandas,
    SciPy, Apache Spark, FAISS, PySpark
    Databases & Data Platforms: Databricks, Delta Lake
    Operating Systems: Windows, Linux
    Data Analysis and ML: ROOT (CERN), RAG, Bayesian inference,
    Feature engineering
    """

    result = get_skills_section(test_jd_skills, test_user_skills)
    print(result)