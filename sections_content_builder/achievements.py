import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_achievements_section(jd_achievements_text: str, user_achievements_text: str, general_text: str = "") -> str | None:
    if not jd_achievements_text.strip():
        jd_achievements_text = general_text if general_text.strip() else "Competitions, awards, rankings, research, hackathons"

    system_prompt = load_prompt("achievements_prompt.txt")
    client = Groq()

    user_message = f"""
=== JD ACHIEVEMENTS KEYWORDS ===
{jd_achievements_text}

=== CANDIDATE ACHIEVEMENTS ===
{user_achievements_text}
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

    test_jd_achievements = """
    Competitions, Research exposure, Publications, Kaggle, Hackathons, Rankings, Awards
    """

    # Demo 1 — relevant
    test_user_achievements_1 = """
    Google Gen AI Study Jams — Top Finisher. Completed all Generative AI and LLM tracks
    on Google Cloud Skills Boost, ranked in top 10% nationally. Sep 2024.

    Top 5% on Kaggle Tabular Playground Series. Ranked in top 5% out of 3200 teams
    in a structured prediction competition using gradient boosting and feature engineering. Mar 2025.

    Published Research Abstract at ICML Student Workshop. Submitted paper on RAG pipeline
    optimization for academic search, accepted for poster presentation. Feb 2025.
    """

    # Demo 2 — irrelevant
    test_user_achievements_2 = """
    Won inter-hostel cricket tournament in 2023.
    Participated in college cultural fest dance competition 2024.
    Completed 30-day fitness challenge organized by sports committee.
    """

    print("--- TEST 1 (relevant) ---")
    r1 = get_achievements_section(test_jd_achievements, test_user_achievements_1)
    print(r1 if r1 else "SKIPPED — no relevant achievements")

    print("\n--- TEST 2 (irrelevant) ---")
    r2 = get_achievements_section(test_jd_achievements, test_user_achievements_2)
    print(r2 if r2 else "SKIPPED — no relevant achievements")