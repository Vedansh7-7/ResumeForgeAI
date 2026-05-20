import re
import json

HEADING_PATTERNS = {
    "skills": [
        r"^skills?$",
        r"^technical skills?$",
        r"^required skills?$",
        r"^core skills?$"
    ],

    "responsibilities": [
        r"^responsibilities$",
        r"^key responsibilities$",
        r"^what you'll do$",
        r"^duties$"
    ],

    "requirements": [
        r"^requirements$",
        r"^qualifications$",
        r"^required qualifications$",
        r"^what we're looking for$"
    ],

    "preferred": [
        r"^preferred qualifications$",
        r"^good to have$",
        r"^nice to have$"
    ]
}


def clean_text(text):

    text = text.replace("\uf0b7", "-")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def normalize_heading(line):

    line = line.lower()
    line = line.strip()

    line = re.sub(r"[:\-]+$", "", line)

    return line


def detect_heading(line):

    normalized = normalize_heading(line)

    for section, patterns in HEADING_PATTERNS.items():

        for pattern in patterns:

            if re.match(pattern, normalized):
                return section

    return None


with open("./processing_files/output.txt", "r", encoding="utf-8") as file:

    content = file.read()

text = clean_text(content)

sections = {}

current_heading = "general"

sections[current_heading] = []

for line in text.split("\n"):

    line = line.strip()

    if not line:
        continue

    heading = detect_heading(line)

    if heading:

        current_heading = heading

        if current_heading not in sections:
            sections[current_heading] = []

    else:
        sections[current_heading].append(line)


# Remove empty sections
sections = {
    key: value
    for key, value in sections.items()
    if value
}

# Write JSON
with open("./processing_files/raw_jd_sections.json", "w", encoding="utf-8") as json_file:

    json.dump(
        sections,
        json_file,
        indent=4,
        ensure_ascii=False
    )

print("JD sections saved successfully.")