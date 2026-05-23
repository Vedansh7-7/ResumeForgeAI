import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_projects_section(jd_skills_text: str, user_projects_text: str, general_text: str = "") -> str | None:
    if not jd_skills_text.strip():
        jd_skills_text = general_text if general_text.strip() else "Software development, problem solving, building projects"

    system_prompt = load_prompt("projects_prompt.txt")
    client = Groq()

    user_message = f"""
=== JD SKILLS ===
{jd_skills_text}

=== CANDIDATE PROJECTS ===
{user_projects_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    if raw == "NO_MATCH" or raw.startswith("NO_MATCH"):
        return None

    return raw


if __name__ == "__main__":

    test_jd_skills = """
    Machine Learning, Deep Learning, Generative AI, NLP, predictive analytics,
    Python, SQL, Pandas, NumPy, Scikit-learn, TensorFlow, data preprocessing,
    feature engineering, model optimization, data visualization, AI/ML projects
    """

    # Demo 1 — relevant project (ML/AI related)
    test_user_projects_1 = """
    Kirana AI Assistant | Oct 2024 - Dec 2024 | Hackathon
    BharatBricks Hackathon, IIT Indore
    I built a mobile-first AI assistant for small retail shop owners in India. The system
    had a POS logging module, inventory management, and an AI engine that ran nightly.
    I used K-Means clustering to group products by sales pattern and generate reorder
    alerts. The backend used Databricks free tier with Delta tables for data persistence
    and PySpark for batch processing. I also built a nightly insight generator that
    summarized sales trends using statistical analysis with Pandas and NumPy.
    """

    # Demo 2 — partially relevant project
    test_user_projects_2 = """
    Micro Mouse | May 2024 - July 2024 | Github, Certificate
    IITSoC Summer of Code 2024, Intelligent Vehicles and Robotics Division, IIT Indore
    I investigated and implemented various maze scanning algorithms including wall follower,
    Tremaux, Floodfill, and Breadth First Search to autonomously solve a maze. The project
    involved programming the robot in Python, collecting sensor data, and writing scripts
    to compare algorithm efficiency across different maze configurations. I also visualized
    algorithm paths using Matplotlib.
    """

    # Demo 3 — irrelevant project (should return NO_MATCH)
    test_user_projects_3 = """
    College Fest Website | Aug 2023 - Sep 2023 | Github
    Cultural Committee, IIT Indore
    I built a static website for the annual college cultural festival using HTML, CSS,
    and JavaScript. The site had event listings, registration forms, and a photo gallery.
    It received around 2000 visits during the fest week.
    """

    print("--- TEST 1 (relevant) ---")
    r1 = get_projects_section(test_jd_skills, test_user_projects_1)
    print(r1 if r1 else "")

    print("\n--- TEST 2 (partially relevant) ---")
    r2 = get_projects_section(test_jd_skills, test_user_projects_2)
    print(r2 if r2 else "")

    print("\n--- TEST 3 (irrelevant) ---")
    r3 = get_projects_section(test_jd_skills, test_user_projects_3)
    print(r3 if r3 else "")