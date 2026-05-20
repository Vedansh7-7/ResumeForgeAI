"""
New user     → fill profile section by section
Returning user → sidebar menu, view / add / edit / delete per section
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user.db.db_queries import (
    get_personal_info, save_personal_info,
    get_education,     add_education,     delete_education,    update_education,
    get_experience,    add_experience,    delete_experience,   update_experience,
    get_projects,      add_project,       delete_project,      update_project,
    get_skills,        add_skill,         delete_skill,
    get_courses,       add_course,        delete_course,
    get_positions,     add_position,      delete_position,
    get_achievements,  add_achievement,   delete_achievement,
)

st.set_page_config(page_title="Profile", layout="centered")

# ── Guard ─────────────────────────────────────────────────────────────────────
if "user_id" not in st.session_state:
    st.switch_page("pages/1_login.py")

user_id   = st.session_state["user_id"]
user_name = st.session_state["user_name"]
is_new    = st.session_state.get("is_new", False)

st.title(f"Hello, {user_name}")
st.write("---")


# ══════════════════════════════════════════════════════════════════════════════
# NEW USER — section by section
# ══════════════════════════════════════════════════════════════════════════════

SECTIONS = [
    "Personal Info",
    "Education",
    "Experience",
    "Projects",
    "Technical Skills",
    "Key Courses",
    "Positions of Responsibility",
    "Achievements",
]

if is_new:
    section_idx = st.session_state.get("section", 0)

    # Progress bar
    st.progress((section_idx) / len(SECTIONS), text=f"Section {section_idx + 1} of {len(SECTIONS)}: {SECTIONS[section_idx]}")
    st.subheader(SECTIONS[section_idx])
    st.write(" ")

    # ── 0: Personal Info ──────────────────────────────────────────────────────
    if section_idx == 0:
        with st.form("personal_info_form"):
            email     = st.text_input("Email")
            phone     = st.text_input("Phone")
            city      = st.text_input("City")
            linkedin  = st.text_input("LinkedIn URL")
            github    = st.text_input("GitHub URL")
            portfolio = st.text_input("Portfolio URL (optional)")
            submitted = st.form_submit_button("Save & Next", use_container_width=True)

        if submitted:
            save_personal_info(user_id, {
                "email": email, "phone": phone, "city": city,
                "linkedin": linkedin, "github": github, "portfolio": portfolio,
            })
            st.session_state["section"] = 1
            st.rerun()

    # ── 1: Education ──────────────────────────────────────────────────────────
    elif section_idx == 1:
        entries = get_education(user_id)
        if entries:
            for e in entries:
                st.write(f"- **{e['degree']}** in {e['field_of_study']} — {e['institution']} ({e['end_date']})")

        with st.form("edu_form", clear_on_submit=True):
            institution    = st.text_input("Institution *")
            degree         = st.text_input("Degree *  (e.g. B.Tech, M.Sc)")
            field_of_study = st.text_input("Field of Study")
            col1, col2     = st.columns(2)
            start_date     = col1.text_input("Start  (e.g. Aug 2020)")
            end_date       = col2.text_input("End  (e.g. May 2024)")
            grade          = st.text_input("Grade / CGPA")
            add_btn        = st.form_submit_button("Add Entry")

        if add_btn:
            if institution and degree:
                add_education(user_id, {
                    "institution": institution, "degree": degree,
                    "field_of_study": field_of_study, "start_date": start_date,
                    "end_date": end_date, "grade": grade,
                })
                st.success("Added.")
                st.rerun()
            else:
                st.warning("Institution and Degree are required.")

        if st.button("Next →", use_container_width=True):
            st.session_state["section"] = 2
            st.rerun()

    # ── 2: Experience ─────────────────────────────────────────────────────────
    elif section_idx == 2:
        entries = get_experience(user_id)
        if entries:
            for e in entries:
                st.write(f"- **{e['role']}** at {e['company']} ({e['start_date']} – {e['end_date']})")

        with st.form("exp_form", clear_on_submit=True):
            company     = st.text_input("Company *")
            role        = st.text_input("Role / Title *")
            location    = st.text_input("Location")
            col1, col2  = st.columns(2)
            start_date  = col1.text_input("Start")
            end_date    = col2.text_input("End  (or 'Present')")
            description = st.text_area("Description")
            add_btn     = st.form_submit_button("Add Entry")

        if add_btn:
            if company and role:
                add_experience(user_id, {
                    "company": company, "role": role, "location": location,
                    "start_date": start_date, "end_date": end_date, "description": description,
                })
                st.success("Added.")
                st.rerun()
            else:
                st.warning("Company and Role are required.")

        if st.button("Next →", use_container_width=True):
            st.session_state["section"] = 3
            st.rerun()

    # ── 3: Projects ───────────────────────────────────────────────────────────
    elif section_idx == 3:
        entries = get_projects(user_id)
        if entries:
            for e in entries:
                st.write(f"- **{e['name']}**  |  {e['tech_stack']}")

        with st.form("proj_form", clear_on_submit=True):
            name        = st.text_input("Project Name *")
            tech_stack  = st.text_input("Tech Stack  (comma separated)")
            description = st.text_area("Description")
            link        = st.text_input("Link (GitHub / Live)")
            add_btn     = st.form_submit_button("Add Entry")

        if add_btn:
            if name:
                add_project(user_id, {
                    "name": name, "tech_stack": tech_stack,
                    "description": description, "link": link,
                })
                st.success("Added.")
                st.rerun()
            else:
                st.warning("Project name is required.")

        if st.button("Next →", use_container_width=True):
            st.session_state["section"] = 4
            st.rerun()

    # ── 4: Technical Skills ───────────────────────────────────────────────────
    elif section_idx == 4:
        entries = get_skills(user_id)
        if entries:
            for e in entries:
                st.write(f"- {e['skill_name']}  [{e['category']}]")

        with st.form("skill_form", clear_on_submit=True):
            skill_name = st.text_input("Skill *  (e.g. Python)")
            category   = st.text_input("Category  (e.g. Languages, Frameworks)")
            add_btn    = st.form_submit_button("Add Skill")

        if add_btn:
            if skill_name:
                add_skill(user_id, {"skill_name": skill_name, "category": category})
                st.success("Added.")
                st.rerun()
            else:
                st.warning("Skill name is required.")

        if st.button("Next →", use_container_width=True):
            st.session_state["section"] = 5
            st.rerun()

    # ── 5: Key Courses ────────────────────────────────────────────────────────
    elif section_idx == 5:
        entries = get_courses(user_id)
        if entries:
            for e in entries:
                st.write(f"- **{e['course_name']}**: {e['description']}")

        with st.form("course_form", clear_on_submit=True):
            course_name = st.text_input("Course Name *")
            description = st.text_area("Description")
            add_btn     = st.form_submit_button("Add Course")

        if add_btn:
            if course_name:
                add_course(user_id, {"course_name": course_name, "description": description})
                st.success("Added.")
                st.rerun()
            else:
                st.warning("Course name is required.")

        if st.button("Next →", use_container_width=True):
            st.session_state["section"] = 6
            st.rerun()

    # ── 6: Positions of Responsibility ────────────────────────────────────────
    elif section_idx == 6:
        entries = get_positions(user_id)
        if entries:
            for e in entries:
                st.write(f"- **{e['title']}** at {e['organisation']} ({e['start_date']} – {e['end_date']})")

        with st.form("pos_form", clear_on_submit=True):
            title        = st.text_input("Title *  (e.g. Club President)")
            organisation = st.text_input("Organisation *")
            col1, col2   = st.columns(2)
            start_date   = col1.text_input("Start")
            end_date     = col2.text_input("End")
            description  = st.text_area("Description")
            add_btn      = st.form_submit_button("Add Entry")

        if add_btn:
            if title and organisation:
                add_position(user_id, {
                    "title": title, "organisation": organisation,
                    "start_date": start_date, "end_date": end_date,
                    "description": description,
                })
                st.success("Added.")
                st.rerun()
            else:
                st.warning("Title and Organisation are required.")

        if st.button("Next →", use_container_width=True):
            st.session_state["section"] = 7
            st.rerun()

    # ── 7: Achievements ───────────────────────────────────────────────────────
    elif section_idx == 7:
        entries = get_achievements(user_id)
        if entries:
            for e in entries:
                st.write(f"- **{e['title']}**  {e['date'] or ''}")

        with st.form("ach_form", clear_on_submit=True):
            title       = st.text_input("Title *  (e.g. Won HackIndia 2023)")
            description = st.text_area("Description  (optional)")
            date        = st.text_input("Date  (e.g. Oct 2023)")
            add_btn     = st.form_submit_button("Add Achievement")

        if add_btn:
            if title:
                add_achievement(user_id, {
                    "title": title, "description": description, "date": date,
                })
                st.success("Added.")
                st.rerun()
            else:
                st.warning("Title is required.")

        if st.button("Finish & Go to Upload →", use_container_width=True):
            st.session_state["is_new"] = False
            st.switch_page("pages/3_upload.py")


# ══════════════════════════════════════════════════════════════════════════════
# RETURNING USER — sidebar menu, full CRUD per section
# ══════════════════════════════════════════════════════════════════════════════

else:
    section = st.sidebar.radio("Section", SECTIONS)
    st.sidebar.write("---")
    if st.sidebar.button("Upload JD → Build Resume"):
        st.switch_page("pages/3_upload.py")

    # ── Personal Info ─────────────────────────────────────────────────────────
    if section == "Personal Info":
        st.subheader("Personal Info")
        existing = get_personal_info(user_id) or {}
        with st.form("pi_edit"):
            email     = st.text_input("Email",     value=existing.get("email", ""))
            phone     = st.text_input("Phone",     value=existing.get("phone", ""))
            city      = st.text_input("City",      value=existing.get("city", ""))
            linkedin  = st.text_input("LinkedIn",  value=existing.get("linkedin", ""))
            github    = st.text_input("GitHub",    value=existing.get("github", ""))
            portfolio = st.text_input("Portfolio", value=existing.get("portfolio", ""))
            if st.form_submit_button("Save", use_container_width=True):
                save_personal_info(user_id, {
                    "email": email, "phone": phone, "city": city,
                    "linkedin": linkedin, "github": github, "portfolio": portfolio,
                })
                st.success("Saved.")

    # ── Education ─────────────────────────────────────────────────────────────
    elif section == "Education":
        st.subheader("Education")
        entries = get_education(user_id)

        for e in entries:
            with st.expander(f"{e['degree']} — {e['institution']}"):
                with st.form(f"edu_edit_{e['id']}"):
                    institution    = st.text_input("Institution",    value=e["institution"])
                    degree         = st.text_input("Degree",         value=e["degree"])
                    field_of_study = st.text_input("Field",          value=e["field_of_study"] or "")
                    col1, col2     = st.columns(2)
                    start_date     = col1.text_input("Start", value=e["start_date"] or "")
                    end_date       = col2.text_input("End",   value=e["end_date"] or "")
                    grade          = st.text_input("Grade",          value=e["grade"] or "")
                    c1, c2         = st.columns(2)
                    if c1.form_submit_button("Save"):
                        update_education(e["id"], {
                            "institution": institution, "degree": degree,
                            "field_of_study": field_of_study, "start_date": start_date,
                            "end_date": end_date, "grade": grade,
                        })
                        st.success("Updated.")
                        st.rerun()
                    if c2.form_submit_button("Delete", type="secondary"):
                        delete_education(e["id"])
                        st.rerun()

        st.write("---")
        st.write("**Add new**")
        with st.form("edu_add", clear_on_submit=True):
            institution    = st.text_input("Institution *")
            degree         = st.text_input("Degree *")
            field_of_study = st.text_input("Field of Study")
            col1, col2     = st.columns(2)
            start_date     = col1.text_input("Start")
            end_date       = col2.text_input("End")
            grade          = st.text_input("Grade")
            if st.form_submit_button("Add", use_container_width=True):
                if institution and degree:
                    add_education(user_id, {
                        "institution": institution, "degree": degree,
                        "field_of_study": field_of_study, "start_date": start_date,
                        "end_date": end_date, "grade": grade,
                    })
                    st.success("Added.")
                    st.rerun()

    # ── Experience ────────────────────────────────────────────────────────────
    elif section == "Experience":
        st.subheader("Experience")
        entries = get_experience(user_id)

        for e in entries:
            with st.expander(f"{e['role']} at {e['company']}"):
                with st.form(f"exp_edit_{e['id']}"):
                    company     = st.text_input("Company",  value=e["company"])
                    role        = st.text_input("Role",     value=e["role"])
                    location    = st.text_input("Location", value=e["location"] or "")
                    col1, col2  = st.columns(2)
                    start_date  = col1.text_input("Start",  value=e["start_date"] or "")
                    end_date    = col2.text_input("End",    value=e["end_date"] or "")
                    description = st.text_area("Description", value=e["description"] or "")
                    c1, c2      = st.columns(2)
                    if c1.form_submit_button("Save"):
                        update_experience(e["id"], {
                            "company": company, "role": role, "location": location,
                            "start_date": start_date, "end_date": end_date,
                            "description": description,
                        })
                        st.success("Updated.")
                        st.rerun()
                    if c2.form_submit_button("Delete", type="secondary"):
                        delete_experience(e["id"])
                        st.rerun()

        st.write("---")
        st.write("**Add new**")
        with st.form("exp_add", clear_on_submit=True):
            company     = st.text_input("Company *")
            role        = st.text_input("Role *")
            location    = st.text_input("Location")
            col1, col2  = st.columns(2)
            start_date  = col1.text_input("Start")
            end_date    = col2.text_input("End")
            description = st.text_area("Description")
            if st.form_submit_button("Add", use_container_width=True):
                if company and role:
                    add_experience(user_id, {
                        "company": company, "role": role, "location": location,
                        "start_date": start_date, "end_date": end_date,
                        "description": description,
                    })
                    st.success("Added.")
                    st.rerun()

    # ── Projects ──────────────────────────────────────────────────────────────
    elif section == "Projects":
        st.subheader("Projects")
        entries = get_projects(user_id)

        for e in entries:
            with st.expander(e["name"]):
                with st.form(f"proj_edit_{e['id']}"):
                    name        = st.text_input("Name",       value=e["name"])
                    tech_stack  = st.text_input("Tech Stack", value=e["tech_stack"] or "")
                    description = st.text_area("Description", value=e["description"] or "")
                    link        = st.text_input("Link",       value=e["link"] or "")
                    c1, c2      = st.columns(2)
                    if c1.form_submit_button("Save"):
                        update_project(e["id"], {
                            "name": name, "tech_stack": tech_stack,
                            "description": description, "link": link,
                        })
                        st.success("Updated.")
                        st.rerun()
                    if c2.form_submit_button("Delete", type="secondary"):
                        delete_project(e["id"])
                        st.rerun()

        st.write("---")
        st.write("**Add new**")
        with st.form("proj_add", clear_on_submit=True):
            name        = st.text_input("Project Name *")
            tech_stack  = st.text_input("Tech Stack")
            description = st.text_area("Description")
            link        = st.text_input("Link")
            if st.form_submit_button("Add", use_container_width=True):
                if name:
                    add_project(user_id, {
                        "name": name, "tech_stack": tech_stack,
                        "description": description, "link": link,
                    })
                    st.success("Added.")
                    st.rerun()

    # ── Technical Skills ──────────────────────────────────────────────────────
    elif section == "Technical Skills":
        st.subheader("Technical Skills")
        entries = get_skills(user_id)

        if entries:
            for e in entries:
                col1, col2 = st.columns([5, 1])
                col1.write(f"**{e['skill_name']}**  —  {e['category'] or 'Uncategorised'}")
                if col2.button("Delete", key=f"del_skill_{e['id']}"):
                    delete_skill(e["id"])
                    st.rerun()

        st.write("---")
        with st.form("skill_add", clear_on_submit=True):
            skill_name = st.text_input("Skill *")
            category   = st.text_input("Category  (e.g. Languages, Tools)")
            if st.form_submit_button("Add", use_container_width=True):
                if skill_name:
                    add_skill(user_id, {"skill_name": skill_name, "category": category})
                    st.success("Added.")
                    st.rerun()

    # ── Key Courses ───────────────────────────────────────────────────────────
    elif section == "Key Courses":
        st.subheader("Key Courses")
        entries = get_courses(user_id)

        if entries:
            for e in entries:
                col1, col2 = st.columns([5, 1])
                col1.write(f"**{e['course_name']}** — {e['description'] or ''}")
                if col2.button("Delete", key=f"del_course_{e['id']}"):
                    delete_course(e["id"])
                    st.rerun()

        st.write("---")
        with st.form("course_add", clear_on_submit=True):
            course_name = st.text_input("Course Name *")
            description = st.text_area("Description")
            if st.form_submit_button("Add", use_container_width=True):
                if course_name:
                    add_course(user_id, {"course_name": course_name, "description": description})
                    st.success("Added.")
                    st.rerun()

    # ── Positions ─────────────────────────────────────────────────────────────
    elif section == "Positions of Responsibility":
        st.subheader("Positions of Responsibility")
        entries = get_positions(user_id)

        if entries:
            for e in entries:
                col1, col2 = st.columns([5, 1])
                col1.write(f"**{e['title']}** at {e['organisation']}")
                if col2.button("Delete", key=f"del_pos_{e['id']}"):
                    delete_position(e["id"])
                    st.rerun()

        st.write("---")
        with st.form("pos_add", clear_on_submit=True):
            title        = st.text_input("Title *")
            organisation = st.text_input("Organisation *")
            col1, col2   = st.columns(2)
            start_date   = col1.text_input("Start")
            end_date     = col2.text_input("End")
            description  = st.text_area("Description")
            if st.form_submit_button("Add", use_container_width=True):
                if title and organisation:
                    add_position(user_id, {
                        "title": title, "organisation": organisation,
                        "start_date": start_date, "end_date": end_date,
                        "description": description,
                    })
                    st.success("Added.")
                    st.rerun()

    # ── Achievements ──────────────────────────────────────────────────────────
    elif section == "Achievements":
        st.subheader("Achievements")
        entries = get_achievements(user_id)

        if entries:
            for e in entries:
                col1, col2 = st.columns([5, 1])
                col1.write(f"**{e['title']}**  {e['date'] or ''}")
                if col2.button("Delete", key=f"del_ach_{e['id']}"):
                    delete_achievement(e["id"])
                    st.rerun()

        st.write("---")
        with st.form("ach_add", clear_on_submit=True):
            title       = st.text_input("Title *")
            description = st.text_area("Description")
            date        = st.text_input("Date")
            if st.form_submit_button("Add", use_container_width=True):
                if title:
                    add_achievement(user_id, {
                        "title": title, "description": description, "date": date,
                    })
                    st.success("Added.")
                    st.rerun()