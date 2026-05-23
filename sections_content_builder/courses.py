import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_courses_section(jd_skills_text: str, user_courses_text: str, general_text: str = "") -> str | None:
    if not jd_skills_text.strip():
        jd_skills_text = general_text if general_text.strip() else "Software development, data analysis, mathematics, computer science"

    system_prompt = load_prompt("courses_prompt.txt")
    client = Groq()

    user_message = f"""
=== JD SKILLS ===
{jd_skills_text}

=== CANDIDATE COURSES ===
{user_courses_text}
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
    Machine Learning, Deep Learning, NLP, predictive analytics,
    Python, Pandas, NumPy, Scikit-learn, data preprocessing,
    feature engineering, statistics, data visualization
    """

    # Demo 1 — mixed courses, some relevant some not
    test_user_courses_1 = """
    Linear Algebra, Basic Calculus, Numerical Methods, Differential Equations,
    Complex Analysis, Scientific Computing Lab, Markov Chain Monte Carlo,
    Probability and Statistics, Data Structures and Algorithms, Computer Networks,
    Digital Electronics, Signals and Systems, Engineering Drawing,
    Introduction to Machine Learning, Database Management Systems
    """

    # Demo 2 — mostly irrelevant courses
    test_user_courses_2 = """
    Engineering Drawing, Manufacturing Processes, Fluid Mechanics,
    Thermodynamics, Theory of Machines, Material Science
    """

    print("--- TEST 1 (mixed) ---")
    r1 = get_courses_section(test_jd_skills, test_user_courses_1)
    print(r1 if r1 else "")

    print("\n--- TEST 2 (irrelevant) ---")
    r2 = get_courses_section(test_jd_skills, test_user_courses_2)
    print(r2 if r2 else "")