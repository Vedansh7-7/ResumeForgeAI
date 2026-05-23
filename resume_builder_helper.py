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

def experiences_to_json(experiences_text):
    """
    Parses multiple experiences and returns a list of dictionaries.
    """
    # Split into separate experience blocks
    blocks = re.split(r'(?=\n-\s)', experiences_text.strip())
    blocks = [block.strip() for block in blocks if block.strip() and block.startswith('-')]
    
    experiences = []
    
    for block in blocks:
        exp = {}
        
        # Name
        name_match = re.search(r'-\s*(.+?)\s*\|', block)
        if name_match:
            exp["name"] = name_match.group(1).strip()
        
        # Duration
        duration_match = re.search(r'\|\s*(.+?)\s*(?:\n|$)', block)
        if duration_match:
            exp["duration"] = duration_match.group(1).strip()
        
        # Role
        role_match = re.search(r'\n\s*(.+?),\s*.+?\s*\|', block)
        if role_match:
            exp["role"] = role_match.group(1).strip()
        
        # Location
        loc_match = re.search(r',\s*(.+?)\s*\|\s*\w+', block)
        if loc_match:
            exp["location"] = loc_match.group(1).strip()
        
        # Type
        type_match = re.search(r'\|\s*(\w+)\s*$', block, re.MULTILINE)
        if type_match:
            exp["type"] = type_match.group(1).strip()
        
        # Bullet Points
        points = re.findall(r'–\s*(.+?)(?=\n\s*–|\n\n|\Z)', block, re.DOTALL | re.MULTILINE)
        exp["points"] = [p.strip() for p in points if p.strip()]
        
        experiences.append(exp)
    
    return experiences

def projects_to_json_type_structure(projects_text):

    # Split projects based on lines starting with '- '
    project_blocks = re.split(r'(?=\n-\s)', projects_text.strip())
    project_blocks = [block.strip() for block in project_blocks if block.strip()]
    
    projects_list = []
    
    for block in project_blocks:
        project = {}
        
        # Extract Name
        name_match = re.search(r'-\s*(.+?)\s*\|', block)
        if name_match:
            project["name"] = name_match.group(1).strip()
        
        # Extract Duration
        duration_match = re.search(r'\|\s*(.+?)\s*\|', block)
        if duration_match:
            project["duration"] = duration_match.group(1).strip()
        
        # Extract Bullet Points
        points = re.findall(r'–\s*(.+?)(?=\n–|\n\n|$)', block, re.DOTALL)
        project["points"] = [point.strip() for point in points if point.strip()]
        
        projects_list.append(project)
    
    return projects_list

def courses_to_json(courses_text):
    """
    Parses courses text and returns the desired structure.
    """
    courses_dict = {}
    
    # Match each line: - Category: [Item1, Item2, Item3]
    pattern = r'-\s*(.+?):\s*\[(.*?)\]'
    
    matches = re.findall(pattern, courses_text)
    
    for category, skills_str in matches:
        category = category.strip()
        # Split by comma and clean each item
        skills = [skill.strip() for skill in re.split(r',\s*', skills_str) if skill.strip()]
        courses_dict[category] = skills
    
    return {"courses": courses_dict}