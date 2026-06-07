import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model ONCE (expensive operation, don't reload inside the function)
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_match_score(jd_text, user_text):
    """
    Takes JD section text and User profile section text.
    Returns a match percentage (0 to 100).
    """

    # Safety check
    if not jd_text or not user_text:
        return 0.0

    # Step 1: Convert text to vectors
    jd_vec   = model.encode([jd_text]).astype('float32')
    user_vec = model.encode([user_text]).astype('float32')

    # Step 2: Normalize (so IP = cosine similarity)
    faiss.normalize_L2(jd_vec)
    faiss.normalize_L2(user_vec)

    # Step 3: Build index and add JD vector
    index = faiss.IndexFlatIP(jd_vec.shape[1])
    index.add(jd_vec)

    # Step 4: Search
    D, I = index.search(user_vec, k=1)

    # Step 5: Convert to percentage
    return round(float(D[0][0]) * 100, 2)


def get_overall_match(sections: dict, weights: dict) -> dict:
    """
    sections: {"skills": ("jd text", "user text"), "experience": (...), ...}
    weights:  {"skills": 0.40, "experience": 0.30, ...}

    Returns a dict with section scores and overall score.
    """
    results = {}

    for section, (jd_text, user_text) in sections.items():
        score = get_match_score(jd_text, user_text)
        results[section] = score
        print(f"{section.capitalize():<12} Match: {score}%")

    overall = sum(results[s] * weights[s] for s in results)
    overall = round(overall, 2)

    results["overall"] = overall
    print(f"\nOverall Match Score: {overall}%")

    return results

def get_skill_gap(jd_skills_text: str, user_skills_dict: dict) -> list:
    """
    Returns list of JD keywords the user doesn't have.
    """
    # Flatten user skills into a single lowercase set
    user_skills = set(
        skill.lower()
        for skills in user_skills_dict.values()
        for skill in skills
    )

    # Split JD skills text into individual keywords
    jd_keywords = [kw.strip().lower() for kw in jd_skills_text.split()]

    # Find keywords not covered by user skills
    missing = []
    for kw in jd_keywords:
        if len(kw) < 3:          # skip noise like "a", "or", "in"
            continue
        if not any(kw in skill or skill in kw for skill in user_skills):
            if kw not in missing:
                missing.append(kw)

    return missing

# ─── Example ───────────────────────────────────────

# sections = {
#     "skills":     ("Python, ML, SQL, pandas",        "Python, deep learning, numpy"),
#     "experience": ("3 years data engineering",        "2 years ML engineer"),
#     "education":  ("B.Tech Computer Science",         "B.Tech Information Technology"),
#     "projects":   ("Built recommendation system",     "Built image classifier"),
# }

# weights = {
#     "skills":     0.40,
#     "experience": 0.30,
#     "education":  0.15,
#     "projects":   0.15,
# }

# # ─── Call the function ────────────────────────────────────────
# output = get_overall_match(sections, weights)

# # output is a dict, example output:
# # {
# #   "skills":     78.4,
# #   "experience": 65.1,
# #   "education":  90.2,
# #   "projects":   55.7,
# #   "overall":    74.3
# # }