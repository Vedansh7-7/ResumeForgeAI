# This file is responsible for fetching user data from the database, cleaning it, and then passing it to the respective section content builders to generate the content for each section of the resume.
import json
from collections import defaultdict
import re
from user.db.db_queries import get_achievements, get_courses, get_education, get_experience, get_personal_info, get_positions, get_projects, get_skills, get_user_by_name
from sections_content_builder.skills import get_skills_section
from sections_content_builder.experience import get_experience_section
from sections_content_builder.positions import get_positions_section
from sections_content_builder.courses import get_courses_section
from sections_content_builder.projects import get_projects_section




# user = ""

# row = get_user_by_name(user)

# if not row:
#     print("User not found.")
# else:
#     user_id = row["id"]

#     functions = [get_achievements, get_courses, get_education, get_experience, 
#                  get_personal_info, get_positions, get_projects, get_skills]
#     name_of_functions = ['achievements', 'courses', 'education', 'experience', 
#                          'personal info', 'positions', 'projects', 'skills']

#     print(f"Printing details of {user}: {row}\n" + "-"*50)

#     # for idx in range(len(functions)):
#     #     print(f"User's {name_of_functions[idx]}: {functions[idx](user_id)}")

# #------------------------------------------------------------------------------------ Skill Section
# ## function to clean user DB skill section
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
    with open(r"processing_files/normalized_jd_sections.json", 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        return jd_data["technical_skills"]  # pass this directly
    
# Skill_description = get_skills_section(clean_skills_JD(), clean_skills_user(user_id))
# print(Skill_description if Skill_description else "na")

# #------------------------------------------------------------------------------------ Experience Section
# ## function to clean user DB skill section
def clean_exp_user(userID):
    rows = get_experience(user_id=userID)
    lines = []
    for row in rows:
        lines.append(
            f"{row['company']} | {row['start_date']} - {row['end_date']}\n"
            f"{row['role']}, {row['location']}\n"
            f"{row['description']}"
        )
    return "\n\n".join(lines)
 
def clean_exp_JD():
    with open(r"processing_files/normalized_jd_sections.json", 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        return jd_data.get("experience", ""), jd_data.get("general", "")
 
# jd_exp, jd_general = clean_exp_JD()
# Experience_description = get_experience_section(jd_exp, clean_exp_user(user_id), general_text=jd_general)
# print(Experience_description if Experience_description else "na")

# #------------------------------------------------------------------------------------ Project Section
def clean_projects_user(userID):
    rows = get_projects(user_id=userID)
    lines = []
    for row in rows:
        lines.append(
            f"{row['name']} | {row['tech_stack']}\n"
            f"{row['description']}\n"
            f"Link: {row['link'] or 'N/A'}"
        )
    return "\n\n".join(lines)
 
def clean_projects_JD():
    with open(r"processing_files/normalized_jd_sections.json", 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        return jd_data.get("technical_skills", ""), jd_data.get("general", "")
 
# jd_proj_skills, jd_general = clean_projects_JD()
# Projects_description = get_projects_section(jd_proj_skills, clean_projects_user(user_id), general_text=jd_general)
# print(Projects_description if Projects_description else "na")

# #------------------------------------------------------------------------------------ Course Section
def clean_courses_user(userID):
    rows = get_courses(user_id=userID)
    # courses prompt expects a flat list
    return ", ".join(row["course_name"] for row in rows)
 
def clean_courses_JD():
    with open(r"processing_files/normalized_jd_sections.json", 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        return jd_data.get("technical_skills", ""), jd_data.get("general", "")
 
# jd_courses_skills, jd_general = clean_courses_JD()
# Courses_description = get_courses_section(jd_courses_skills, clean_courses_user(user_id), general_text=jd_general)
# print(Courses_description if Courses_description else "na")

# #------------------------------------------------------------------------------------ POR Section
def clean_positions_user(userID):
    rows = get_positions(user_id=userID)
    lines = []
    for row in rows:
        # match the bullet format the positions prompt expects
        lines.append(
            f"• {row['title']}, {row['organisation']}"
            f"          {row['start_date']} - {row['end_date']}"
        )
    return "\n".join(lines)
 
def clean_positions_JD():
    with open(r"processing_files/normalized_jd_sections.json", 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        return jd_data.get("positions_of_responsibility", ""), jd_data.get("general", "")
 
# jd_pos, jd_general = clean_positions_JD()
# Positions_description = get_positions_section(jd_pos, clean_positions_user(user_id), general_text=jd_general)
# print(Positions_description if Positions_description else "na")