import os
from dotenv import load_dotenv 
from groq import Groq

load_dotenv()

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


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
    SKILLS_SYSTEM_PROMPT = load_prompt("skills_prompt.txt")
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