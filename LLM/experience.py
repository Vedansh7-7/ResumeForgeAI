import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_experience_section(jd_experience_text: str, user_experience_text: str, general_text: str = "") -> str:
    # Fallback: if JD has no experience section, use general
    if not jd_experience_text.strip():
        jd_experience_text = general_text if general_text.strip() else "Software development, collaboration, problem solving, building projects"

    system_prompt = load_prompt("experience_prompt.txt")
    client = Groq()

    user_message = f"""
=== JD EXPERIENCE REQUIREMENTS ===
{jd_experience_text}

=== CANDIDATE EXPERIENCE ===
{user_experience_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    return response.text if hasattr(response, "text") else response.choices[0].message.content