import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

print("Connecting to Groq API and normalizing raw JD json...\n")

final_jd = {
    "technical_skills": [],
    "experience": [],
    "general": [],
    "positions_of_responsibility": [],
    "achievements": []
}

with open(r"processing_files\raw_jd_sections.json", "r", encoding="utf-8") as f:
    jd_sections = json.load(f)

with open(r"prompts\section_normalizer_system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

with open(r"prompts\section_normalizer_human.txt", "r", encoding="utf-8") as f:
    human_template = f.read()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

for section_name, section_lines in jd_sections.items():

    print(f"Processing section: {section_name}")

    jd_text = "\n".join(section_lines)
    human_prompt = human_template.replace("{jd_text}", jd_text)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": human_prompt}
            ]
        )

        content = response.choices[0].message.content.strip()

        if not content:
            print(f"Empty response for section: {section_name}")
            continue

        parsed = json.loads(content)

    except Exception as e:
        print(f"\nError processing section: {section_name}")
        print(e)
        continue

    for key, value in parsed.items():

        if key not in final_jd:
            continue

        if isinstance(value, list):
            cleaned = [str(v).strip() for v in value if str(v).strip()]
            final_jd[key].extend(cleaned)

        elif isinstance(value, str):
            value = value.strip()
            if value:
                final_jd[key].append(value)

# ── DEDUPLICATION (fixed) ─────────────────────────────────────────────────────
for key in final_jd:
    if isinstance(final_jd[key], list):
        seen = []
        for item in final_jd[key]:
            if item not in seen:
                seen.append(item)
        final_jd[key] = " ".join(seen)
    elif isinstance(final_jd[key], str):
        final_jd[key] = " ".join(dict.fromkeys(final_jd[key].split()))
# ─────────────────────────────────────────────────────────────────────────────

output_path = r"processing_files\normalized_jd_sections.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_jd, f, indent=4, ensure_ascii=False)

print("\nNormalized structure formed successfully.")
print(f"Saved to: {output_path}")