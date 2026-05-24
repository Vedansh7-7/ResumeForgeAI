import subprocess
import sys
import os
from parse import parsePdf

def main_pipeline(path, user_id, user_name):

    # ── Stage 1: Parse JD PDF ──────────────────────────────────────────────
    result = parsePdf(path)
    if result != r"Extracted into ./processing_files/output.txt":
        print("PDF parsing failed.")
        return

    # ── Stage 2: Extract sections ──────────────────────────────────────────
    subprocess.run(['python', 'section_extractor.py'], check=True)

    # ── Stage 3: Normalise sections ────────────────────────────────────────
    subprocess.run(['python', 'normalize_sections.py'], check=True)

    # ── Stage 4: Generate section content via LLM ─────────────────────────
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

    # ── Stage 6: Render PDF ────────────────────────────────────────────────
    from generate_resume import generate
    pdf_path = generate()
    print(f"Resume generated: {pdf_path}")
    return pdf_path