import re
import json

from user.db.db_connect import get_connection
from user.db.db_queries import get_achievements, get_education, get_personal_info

name =""
def get_name(userID):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (userID,))
    user = cursor.fetchone()
    if user:
        name = user['name']
    cursor.close()
    conn.close()
    return name
name = get_name(2)  # Example usage, replace with actual userID input


def skill_to_json_type_structure(skill_text):
    skill_dict = {}
    pattern = r'-\s*(.+?):\s*(.+)'
    
    for match in re.finditer(pattern, skill_text):
        category = match.group(1).strip()
        skills_str = match.group(2).strip()
        skills = [skill.strip() for skill in re.split(r',\s*', skills_str)]
        skill_dict[category] = skills
    return skill_dict


def experiences_to_json(experiences_text):
    blocks = re.split(r'\n(?=-\s)', experiences_text.strip())
    blocks = [block.strip() for block in blocks if block.strip()]
    
    experiences = []
    for block in blocks:
        exp = {}
        name_match  = re.search(r'-\s*(.+?)\s*\|', block)
        duration_match = re.search(r'\|\s*(.+?)\s*(?:\n|$)', block)
        role_match  = re.search(r'\n\s*(.+?),\s*.+?\s*\|', block)
        loc_match   = re.search(r',\s*(.+?)\s*\|', block)
        type_match  = re.search(r'\|\s*(\w+)\s*$', block, re.MULTILINE)
        flat_block  = block.replace('\n', ' ')
        points      = re.findall(r'–\s*(.+?)(?=\s*–|$)', flat_block)

        if name_match:
            exp["company"]         = name_match.group(1).strip()
            exp["duration"]        = duration_match.group(1).strip() if duration_match else ""
            exp["role"]            = role_match.group(1).strip() if role_match else ""
            exp["location"]        = loc_match.group(1).strip() if loc_match else ""
            exp["employment_type"] = type_match.group(1).strip() if type_match else ""
            exp["points"]          = [p.strip() for p in points if p.strip()]
            experiences.append(exp)
    return experiences


def projects_to_json_type_structure(projects_text):
    project_blocks = re.split(r'\n(?=-\s)', projects_text.strip())
    project_blocks = [block.strip() for block in project_blocks if block.strip()]
    
    projects_list = []
    for block in project_blocks:
        project = {}
        name_match = re.search(r'-\s*(.+?)\s*\|', block)
        duration_match = re.search(r'\|\s*(.+?)\s*\|', block)
        flat_block = block.replace('\n', ' ')
        points = re.findall(r'–\s*(.+?)(?=\s*–|$)', flat_block)
        
        if name_match:
            project["name"] = name_match.group(1).strip()
            project["subtitle"] = "Personal Project"
            duration_raw = duration_match.group(1).strip() if duration_match else ""
            project["duration"] = "" if "No Date" in duration_raw else duration_raw
            project["link"] = ""
            project["points"] = [p.strip() for p in points if p.strip()]
            projects_list.append(project)
    return projects_list


def courses_to_json(courses_text):
    courses_dict = {}
    pattern = r'-\s*(.+?):\s*\[(.*?)\]'
    matches = re.findall(pattern, courses_text)
    
    for category, skills_str in matches:
        category = category.strip()
        skills = [skill.strip() for skill in re.split(r',\s*', skills_str) if skill.strip()]
        courses_dict[category] = skills
    return {"courses": courses_dict}


def pors_to_json(pors_text):
    positions = []
    lines = re.split(r'[•\-]\s*', pors_text.strip())
    lines = [line.strip() for line in lines if line.strip()]
    
    for line in lines:
        # Match: Title, Organisation   Duration
        match = re.search(r'(.+?),\s*(.+?)\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+?)$', line.strip())
        if match:
            positions.append({
                "title":        match.group(1).strip(),
                "organisation": match.group(2).strip(),
                "duration":     match.group(3).strip()
            })
    return {"positions": positions}

def achievements_to_json(userID):
    rows = get_achievements(user_id=userID)
    lines = []
    for row in rows:
        lines.append(
            f"• {row['title']}: {row['description']} ({row['date']})"
        )
    achievements_text = "\n".join(lines)


    achievements_list = []
    lines = re.split(r'[•-]\s*', achievements_text.strip())
    lines = [line.strip() for line in lines if line.strip()]
    
    for line in lines:
        match = re.search(r'(.+?):\s*(.+?)\s*\((.+?)\)$', line.strip())
        if match:
            achievements_list.append({
                "title": match.group(1).strip(),
                "description": match.group(2).strip(),
                "date": match.group(3).strip()
            })
    return {"achievements": achievements_list}

def education_to_json(userID):
    rows = get_education(user_id=userID)
    education_list = []
    for row in rows:
        education_list.append({
            "degree": row['degree'],
            "field_of_study": row['field_of_study'],
            "institution": row['institution'],
            "start_date": row.get('start_date', ''),
            "end_date": row['end_date'],
            "grade": row.get('grade', '')
        })
    return {"education": education_list}

def personal_info_to_json(userID):
    user = get_personal_info(user_id=userID)
    if user:
        return {
            "personal": {
                "name": get_name(userID),   # also fix: was using module-level `name` variable
                "phone": user['phone'],
                "emaila": user['email'],    # ← was "email"
                "github": user['github'],
                "website": user['portfolio'],
                "linkedin": user['linkedin']
            }
        }
    else:
        return {"personal": {}}

# MAIN BUILDER FUNCTION

def build_resume_json(user_id, experiences_text, projects_text, skills_text, courses_text, pors_text):
    resume = {}
    resume["personal"] = personal_info_to_json(userID=user_id)["personal"]
    resume.update(education_to_json(userID=user_id))
    resume["experience"] = experiences_to_json(experiences_text)
    resume["projects"]   = projects_to_json_type_structure(projects_text)
    resume["skills"]     = skill_to_json_type_structure(skills_text)
    resume.update(courses_to_json(courses_text))
    resume.update(pors_to_json(pors_text))
    resume.update(achievements_to_json(userID=user_id))
    return resume


# Just for exapmle, you can replace the text with actual input from user or files

if __name__ == "__main__":
    # Paste your actual text here
    experiences_text = """- Arihant Capital Markets | May 2024 - Jul 2024
  Data Science Intern, Indore, India | Internship
  – Developed a retrieval-augmented generation system for academic paper summarization using Machine Learning and NLP techniques
  – Implemented a FAISS-based vector store and experimented with chunking and embedding strategies using Sentence Transformers
  – Analysed and preprocessed a dataset of 12,000 research abstracts using Python and Pandas for model training and evaluation"""

    projects_text = """- AI Resume Tailor | Jan 2026 - Present | Github
  Personal Project
  – Built an end-to-end AI-powered resume tailoring platform...
  – Implemented FAISS-based semantic matching...
  – Designed a multi-user profile memory system..."""

    skills_text = """- Languages: Python, SQL, C++
- AI ML: TensorFlow, XGBoost, Scikit-learn
- NLP: LangChain, Sentence Transformers
- Gen AI: Ollama, Groq API, Llama 3.2
- Data & Analytics: Pandas, NumPy, Matplotlib"""

    courses_text = """- Machine Learning & AI: [Machine Learning, Deep Learning, Natural Language Processing]
- Data Science Foundations: [Probability and Statistics, Linear Algebra]
- Database Management: [Database Management Systems]"""

    pors_text = """• Kaggle Campus Ambassador, Kaggle / NIT Bhopal Jan 2024 - Present
• AI/ML Club Lead, NIT Bhopal Aug 2023 - Present"""

    # Build final JSON
    final_json = build_resume_json(
        user_id=2,
        experiences_text=experiences_text,
        projects_text=projects_text,
        skills_text=skills_text,
        courses_text=courses_text,
        pors_text=pors_text
    )

    # Save to file
    with open("resume_data.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)

    print("Resume JSON successfully created and saved as 'resume_data.json'")