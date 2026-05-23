import re


def skill_to_json_type_structure(skill_text):
    skill_dict = {}
    

    pattern = r'-\s*(.+?):\s*(.+)'
    
    for match in re.finditer(pattern, skill_text):
        category = match.group(1).strip()
        skills_str = match.group(2).strip()

        skills = [skill.strip() for skill in re.split(r',\s*', skills_str)]
        
        skill_dict[category] = skills
    
    return skill_dict

def experience_to_json_type_structure(experience_text):
    result = {}
    
    # Extract Company Name
    company_match = re.search(r'-\s*(.+?)\s*\|', experience_text)
    if company_match:
        result["name"] = company_match.group(1).strip()
    
    # Extract Duration
    duration_match = re.search(r'\|\s*(.+?)\n', experience_text)
    if duration_match:
        result["duration"] = duration_match.group(1).strip()
    
    # Extract Role/Title
    role_match = re.search(r'\n\s*(.+?),\s*.+?\|\s*(\w+)', experience_text)
    if role_match:
        result["role"] = role_match.group(1).strip()
        result["type"] = role_match.group(2).strip()
    
    # Extract Location
    location_match = re.search(r',\s*(.+?)\s*\|\s*\w+', experience_text)
    if location_match:
        result["location"] = location_match.group(1).strip()
    
    # Extract Bullet Points
    points = re.findall(r'–\s*(.+)', experience_text)
    result["points"] = [point.strip() for point in points]
    
    return result

def project_to_json_type_structure(project_text):
    result = {}
    
    # Extract Project Name
    name_match = re.search(r'-\s*(.+?)\s*\|', project_text)
    if name_match:
        result["name"] = name_match.group(1).strip()
    
    # Extract Duration
    duration_match = re.search(r'\|\s*(.+?)\s*\|', project_text)
    if duration_match:
        result["duration"] = duration_match.group(1).strip()
    else:
        # Fallback if only one pipe is present
        duration_match2 = re.search(r'\|\s*(.+?)\n', project_text)
        if duration_match2:
            result["duration"] = duration_match2.group(1).strip()
    
    # Extract Bullet Points
    points = re.findall(r'–\s*(.+?)(?=\n–|\n\n|$)', project_text, re.DOTALL)
    result["points"] = [point.strip() for point in points if point.strip()]
    
    return result

text = """- Sentiment Analysis Engine | No Date Range | Github
  Personal Project
  – Built an NLP-based sentiment classifier for product reviews using TF-IDF vectorization and logistic regression, achieving 89% accuracy
  – Preprocessed 50,000 Amazon review records and handled class imbalance using SMOTE
  – Developed data visualizations of sentiment distribution and model performance using Matplotlib and Seaborn"""

output = project_to_json_type_structure(text)
print(output)