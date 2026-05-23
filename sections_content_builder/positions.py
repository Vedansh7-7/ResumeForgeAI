import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_positions_section(jd_positions_text: str, user_positions_text: str, general_text: str = "") -> str | None:
    if not jd_positions_text.strip():
        jd_positions_text = general_text if general_text.strip() else "Leadership, teamwork, communication, ownership, collaboration"

    system_prompt = load_prompt("positions_prompt.txt")
    client = Groq()

    user_message = f"""
=== JD POSITIONS KEYWORDS ===
{jd_positions_text}

=== CANDIDATE POSITIONS ===
{user_positions_text}
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

    test_jd_positions = """
    Collaboration, Mentoring, Leadership, Teamwork, Ownership,
    Communication, Initiative
    """

    # Demo 1 — relevant positions
    test_user_positions_1 = """
    • Coordinator, Training and Placement Cell, IIT Indore          Feb. 2025 - Present
    • Member, The Astronomy Club, IIT Indore                        Nov. 2023 - Present
    • Member, The Music Club, IIT Indore                            Aug. 2023 - Present
    """

    # Demo 2 — no leadership or teamwork signals (should return NO_MATCH)
    test_user_positions_2 = """
    • Attendee, Annual Tech Fest, IIT Indore                        Oct. 2023
    • Participant, Intra-college Badminton Tournament               Mar. 2023
    """

    print("--- TEST 1 (relevant) ---")
    r1 = get_positions_section(test_jd_positions, test_user_positions_1)
    print(r1 if r1 else "SKIPPED — no relevant positions")

    print("\n--- TEST 2 (irrelevant) ---")
    r2 = get_positions_section(test_jd_positions, test_user_positions_2)
    print(r2 if r2 else "SKIPPED — no relevant positions")