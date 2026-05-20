from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import json

model = "llama3.2"
print("Connecting to local processor via LangChain and normalizing raw JD json...")

final_jd = {
    "technical_skills": [],
    "experience": [],
    "projects": [],
    "positions_of_responsibility": [],
    "achievements": []
}

with open(r"processing_files\raw_jd_sections.json", "r") as f:
    jd_sections = json.load(f)

llm = ChatOllama(model=model, temperature=0)

with open(r"prompts\section_normalizer_human.txt", "r") as f:
    human_template = f.read()

with open(r"prompts\section_normalizer_system.txt", "r") as f:
    system_prompt = f.read()

for section_name, section_lines in jd_sections.items():
    jd_text = "\n".join(section_lines)

    human_prompt = human_template.replace("{jd_text}", jd_text)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    response = llm.invoke(messages)
    parsed = json.loads(response.content)

    for key, value in parsed.items():
        if value and key in final_jd:
            final_jd[key].append(value)

# merge + deduplicate
final_jd = {
    k: " ".join(dict.fromkeys(v))
    for k, v in final_jd.items()
}

with open(r"processing_files\normalized_jd_sections.json", "w", encoding="utf-8") as f:
    json.dump(final_jd, f, indent=4, ensure_ascii=False)

print("Normalised structure formed")