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


# ─── Your Project Usage ───────────────────────────────────────

sections = {
    "skills":     ("Python, ML, SQL, pandas",           "Python, deep learning, numpy"),
    "experience": ("3 years data engineering",           "2 years ML engineer"),
    "education":  ("B.Tech Computer Science",            "B.Tech Information Technology"),
    "projects":   ("Built recommendation system",        "Built image classifier"),
}

weights = {
    "skills":     0.40,
    "experience": 0.30,
    "education":  0.15,
    "projects":   0.15,
}

results = {}
for section, (jd_text, user_text) in sections.items():
    score = get_match_score(jd_text, user_text)
    results[section] = score
    print(f"{section.capitalize():<12} Match: {score}%")

overall = sum(results[s] * weights[s] for s in results)
print(f"\nOverall Match Score: {round(overall, 2)}%")