import subprocess
import sys
import os
from parse import parsePdf

def main_pipeline(path, user_id, user_name, progress_box=None):

    # ── Stage 1: Parse JD PDF ──────────────────────────────────────────────
    if progress_box:
        progress_box.info("Stage 1/6: Parsing JD PDF...")

    result = parsePdf(path)
    if result != "Extracted into ./processing_files/output.txt":
        print("PDF parsing failed.")
        return

    # ── Stage 2: Extract sections ──────────────────────────────────────────
    if progress_box:
        progress_box.info("Stage 2/6: Extracting sections...")
    subprocess.run(['uv', 'run', 'section_extractor.py'], check=True)

    # ── Stage 3: Normalise sections ────────────────────────────────────────
    if progress_box:
        progress_box.info("Stage 3/6: Normalising sections...")
    subprocess.run(['uv', 'run', 'normalize_sections.py'], check=True)

    # ── Stage 4: Generate section content via LLM ─────────────────────────
    if progress_box:
        progress_box.info("Stage 4/6: Generating section content via LLM...")
    from resume_builder import (
        clean_skills_JD, clean_skills_user,
        clean_exp_JD, clean_exp_user,
        clean_projects_JD, clean_projects_user,
        clean_courses_JD, clean_courses_user,
        clean_positions_JD, clean_positions_user,
    )
    from sections_content_builder.skills     import get_skills_section
    from sections_content_builder.experience import get_experience_section
    from sections_content_builder.projects   import get_projects_section
    from sections_content_builder.courses    import get_courses_section
    from sections_content_builder.positions  import get_positions_section

    skills_text    = get_skills_section(clean_skills_JD(), clean_skills_user(user_id)) or ""
    jd_exp, jd_gen = clean_exp_JD()
    exp_text       = get_experience_section(jd_exp, clean_exp_user(user_id), general_text=jd_gen) or ""
    jd_proj, jd_gen = clean_projects_JD()
    proj_text      = get_projects_section(jd_proj, clean_projects_user(user_id), general_text=jd_gen) or ""
    jd_crs, jd_gen = clean_courses_JD()
    courses_text   = get_courses_section(jd_crs, clean_courses_user(user_id), general_text=jd_gen) or ""
    jd_pos, jd_gen = clean_positions_JD()
    pos_text       = get_positions_section(jd_pos, clean_positions_user(user_id), general_text=jd_gen) or ""

    # ── Stage 5: Build JSON schema ─────────────────────────────────────────
    if progress_box:
        progress_box.info("Stage 5/6: Building JSON schema...")
    from resume_builder_helper import build_resume_json
    import json

    final_json = build_resume_json(
        user_id=user_id,
        experiences_text=exp_text,
        projects_text=proj_text,
        skills_text=skills_text,
        courses_text=courses_text,
        pors_text=pos_text,
    )

    with open("resume_data.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)

    print("JSON schema built.")

# ── Stage 5.5: Compute JD-Profile Match Score ──────────────────────────
    if progress_box:
        progress_box.info("Stage 5.5/6: Computing JD match score...")

    from Similarity_machine.faiss_matcher import get_overall_match
    import json

    with open("processing_files/normalized_jd_sections.json", "r", encoding="utf-8") as f:
        jd_data = json.load(f)

    # Extract user text directly from the built JSON
    user_skills_text = " ".join(
        skill
        for skill_list in final_json.get("skills", {}).values()
        for skill in skill_list
    )

    user_exp_text = " ".join(
        point
        for exp in final_json.get("experience", [])
        for point in exp.get("points", [])
    )

    user_proj_text = " ".join(
        point
        for proj in final_json.get("projects", [])
        for point in proj.get("points", [])
    )

    user_courses_text = " ".join(
        course
        for course_list in final_json.get("courses", {}).values()
        for course in course_list
    )

    sections = {
        "skills":     (jd_data.get("technical_skills", ""), user_skills_text),
        "experience": (jd_data.get("experience", ""),       user_exp_text),
        "projects":   (jd_data.get("technical_skills", ""), user_proj_text),
        "courses":    (jd_data.get("technical_skills", ""), user_courses_text or user_skills_text),
    }

    weights = {
        "skills":     0.40,
        "experience": 0.30,
        "projects":   0.20,
        "courses":    0.10,
    }

    match_scores = get_overall_match(sections, weights)
    print(f"Match scores: {match_scores}")

# ── Stage 6: Render PDF ────────────────────────────────────────────────
    if progress_box:
        progress_box.info("Stage 6/6: Rendering PDF...")

    from generate_resume import generate

    output_dir = os.path.join(
        "user",
        user_name.replace(" ", "_"),
        "outputs"
    )

    os.makedirs(output_dir, exist_ok=True)

    pdf_path = generate(
        json_path="resume_data.json",
        output_dir=output_dir
    )

    print(f"Resume generated: {pdf_path}")

    return pdf_path, match_scores, jd_data, final_json