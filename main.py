# import subprocess
# from parse import parsePdf

# def main():
    
#     with open("./processing_files/output.txt", "r", encoding="utf-8") as file:
#         content = file.read()
#     print(f"Characters in the parsed text = {len(content)}")

# if __name__ == "__main__":
#     print("Hello from new-project!\n\n")
#     file = input("Enter file name after adding it in the .\pdf: ")
#     result = parsePdf(file)
#     if result == r"Extracted into ./processing_files/output.txt":
#         main()
#     else:
#         print("Please check your pdf, we are not able to see any pages in it.")
#     result = subprocess.run(['python', 'section_extractor.py'], capture_output=True, text=True)
#     print(result.stdout)

import json
from collections import defaultdict
from user.db.db_queries import get_achievements, get_courses, get_education, get_experience, get_personal_info, get_positions, get_projects, get_skills, get_user_by_name
from sections_content_builder.skills import get_skills_section

user = input("What is your username?\n")
row = get_user_by_name(user)

if not row:
    print("User not found.")
else:
    user_id = row["id"]

    functions = [get_achievements, get_courses, get_education, get_experience, 
                 get_personal_info, get_positions, get_projects, get_skills]
    name_of_functions = ['achievements', 'courses', 'education', 'experience', 
                         'personal info', 'positions', 'projects', 'skills']

    print(f"Printing details of {user}: {row}\n" + "-"*50)

    for idx in range(len(functions)):
        print(f"User's {name_of_functions[idx]}: {functions[idx](user_id)}")

#------------------------------------------------------------------------------------ Skill Section
## function to clean user DB skill section
def clean_skills_user(userID):
    skills_json = get_skills(user_id=userID)
    grouped = defaultdict(list)

    for row in skills_json:
        grouped[row["category"]].append(row["skill_name"])

    user_skills_text = "\n".join(
        f"{cat}: {', '.join(skills)}" for cat, skills in grouped.items()
    )
    return user_skills_text

def clean_skills_JD():
    with open("processing_files\normalized_jd_sections.json", 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        return jd_data["technical_skills"]  # pass this directly
    
Skill_description = get_skills_section(clean_skills_JD(), clean_skills_user(user_id))
print(Skill_description)

#------------------------------------------------------------------------------------ Experience Section


#------------------------------------------------------------------------------------ Project Section


#------------------------------------------------------------------------------------ Course Section


#------------------------------------------------------------------------------------ Achievement Section


#------------------------------------------------------------------------------------ POR Section
