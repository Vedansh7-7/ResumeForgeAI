# from langchain_ollama import ChatOllama
# from langchain_core.messages import SystemMessage, HumanMessage # Local LLM
# import json

# model = "llama3.2"
# print("Connecting to local processor via LangChain and normalizing raw JD json\n")

# final_jd = {
#     "technical_skills": [],
#     "experience": [],
#     "general": [],
#     "positions_of_responsibility": [],
#     "achievements": []
# }

# with open(r"processing_files\raw_jd_sections.json", "r", encoding="utf-8") as f:
#     jd_sections = json.load(f)

# llm = ChatOllama(model=model, temperature=0)

# with open(r"prompts\section_normalizer_human.txt", "r", encoding="utf-8") as f:
#     human_template = f.read()

# with open(r"prompts\section_normalizer_system.txt", "r", encoding="utf-8") as f:
#     system_prompt = f.read()

# for section_name, section_lines in jd_sections.items():
#     jd_text = "\n".join(section_lines)

#     human_prompt = human_template.replace("{jd_text}", jd_text)

#     messages = [
#         SystemMessage(content=system_prompt),
#         HumanMessage(content=human_prompt)
#     ]

#     response = llm.invoke(messages)
#     parsed = json.loads(response.content)

#     for key, value in parsed.items():
#         if key in final_jd and value:
#             if isinstance(value, list):
#                 final_jd[key].extend(value)   # flatten list
#             else:
#                 final_jd[key].append(value)


# # merge + deduplicate
# final_jd = {k: " ".join(dict.fromkeys(v)) for k, v in final_jd.items()}

# with open(r"processing_files\normalized_jd_sections.jso, n", "w", encoding="utf-8") as f:
#     json.dump(final_jd, f, indent=4, ensure_ascii=False)

# print("Normalised structure formed")



# from langchain_ollama import ChatOllama
# from langchain_core.messages import SystemMessage, HumanMessage # Local LLM

import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

model = "llama3-70b-8192"

print("Connecting to Groq API and normalizing raw JD json\n")

final_jd = {
    "technical_skills": [],
    "experience": [],
    "general": [],
    "positions_of_resibility": [],
    "achievements": []
}

with open(r"processing_files\raw_jd_sections.json", "r", encoding="utf-8") as f:
    jd_sections = json.load(f)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open(r"prompts\section_normalizer_human.txt", "r", encoding="utf-8") as f:
    human_template = f.read()

with open(r"prompts\section_normalizer_system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

for section_name, section_lines in jd_sections.items():
    jd_text = "\n".join(section_lines)

    human_prompt = human_template.replace("{jd_text}", jd_text)

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": human_prompt
            }
        ]
    )

    parsed = json.loads(response.choices[0].message.content)

    for key, value in parsed.items():
        if key in final_jd and value:
            if isinstance(value, list):
                final_jd[key].extend(value)   # flatten list
            else:
                final_jd[key].append(value)

# merge + deduplicate
final_jd = {k: " ".join(dict.fromkeys(v)) for k, v in final_jd.items()}

with open(r"processing_files\normalized_jd_sections.json", "w", encoding="utf-8") as f:
    json.dump(final_jd, f, indent=4, ensure_ascii=False)

print("Normalised structure formed")