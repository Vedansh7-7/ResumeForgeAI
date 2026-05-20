"""
All database operations in one place.
Every page imports from here — no raw SQL anywhere else.
"""

from user.db.db_connect import get_connection


# ── Users ─────────────────────────────────────────────────────────────────────

def get_user_by_name(name: str):
    """Returns user row as dict or None if not found."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(name: str) -> int:
    """Creates a new user and returns their new user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


# ── Personal Info ─────────────────────────────────────────────────────────────

def get_personal_info(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal_info WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def save_personal_info(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personal_info (user_id, email, phone, city, linkedin, github, portfolio)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            email     = VALUES(email),
            phone     = VALUES(phone),
            city      = VALUES(city),
            linkedin  = VALUES(linkedin),
            github    = VALUES(github),
            portfolio = VALUES(portfolio)
    """, (
        user_id,
        data.get("email"),
        data.get("phone"),
        data.get("city"),
        data.get("linkedin"),
        data.get("github"),
        data.get("portfolio"),
    ))
    conn.commit()
    conn.close()


# ── Education ─────────────────────────────────────────────────────────────────

def get_education(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM education WHERE user_id = %s ORDER BY end_date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_education(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO education
            (user_id, institution, degree, field_of_study, start_date, end_date, grade)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data["institution"], data["degree"], data.get("field_of_study"),
        data.get("start_date"), data.get("end_date"), data.get("grade"),
    ))
    conn.commit()
    conn.close()


def delete_education(entry_id: int):
    _delete_by_id("education", entry_id)


def update_education(entry_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE education SET
            institution    = %s,
            degree         = %s,
            field_of_study = %s,
            start_date     = %s,
            end_date       = %s,
            grade          = %s
        WHERE id = %s
    """, (
        data["institution"], data["degree"], data.get("field_of_study"),
        data.get("start_date"), data.get("end_date"), data.get("grade"),
        entry_id,
    ))
    conn.commit()
    conn.close()


# ── Experience ────────────────────────────────────────────────────────────────

def get_experience(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM experience WHERE user_id = %s ORDER BY start_date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_experience(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO experience
            (user_id, company, role, location, start_date, end_date, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data["company"], data["role"], data.get("location"),
        data.get("start_date"), data.get("end_date"), data.get("description"),
    ))
    conn.commit()
    conn.close()


def delete_experience(entry_id: int):
    _delete_by_id("experience", entry_id)


def update_experience(entry_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE experience SET
            company     = %s,
            role        = %s,
            location    = %s,
            start_date  = %s,
            end_date    = %s,
            description = %s
        WHERE id = %s
    """, (
        data["company"], data["role"], data.get("location"),
        data.get("start_date"), data.get("end_date"), data.get("description"),
        entry_id,
    ))
    conn.commit()
    conn.close()


# ── Projects ──────────────────────────────────────────────────────────────────

def get_projects(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects WHERE user_id = %s ORDER BY name", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_project(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO projects
            (user_id, name, tech_stack, description, link)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        user_id,
        data["name"], data.get("tech_stack"), data.get("description"), data.get("link"),
    ))
    conn.commit()
    conn.close()


def delete_project(entry_id: int):
    _delete_by_id("projects", entry_id)


def update_project(entry_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects SET
            name        = %s,
            tech_stack  = %s,
            description = %s,
            link        = %s
        WHERE id = %s
    """, (
        data["name"], data.get("tech_stack"),
        data.get("description"), data.get("link"),
        entry_id,
    ))
    conn.commit()
    conn.close()


# ── Technical Skills ──────────────────────────────────────────────────────────

def get_skills(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM technical_skills WHERE user_id = %s ORDER BY category, skill_name", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_skill(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO technical_skills (user_id, category, skill_name)
        VALUES (%s, %s, %s)
    """, (user_id, data.get("category"), data["skill_name"]))
    conn.commit()
    conn.close()


def delete_skill(entry_id: int):
    _delete_by_id("technical_skills", entry_id)


# ── Key Courses ───────────────────────────────────────────────────────────────

def get_courses(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM key_courses WHERE user_id = %s ORDER BY course_name", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_course(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO key_courses (user_id, course_name, description)
        VALUES (%s, %s, %s)
    """, (user_id, data["course_name"], data.get("description")))
    conn.commit()
    conn.close()


def delete_course(entry_id: int):
    _delete_by_id("key_courses", entry_id)


# ── Positions of Responsibility ───────────────────────────────────────────────

def get_positions(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM positions WHERE user_id = %s ORDER BY start_date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_position(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO positions
            (user_id, title, organisation, start_date, end_date, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data["title"], data["organisation"],
        data.get("start_date"), data.get("end_date"), data.get("description"),
    ))
    conn.commit()
    conn.close()


def delete_position(entry_id: int):
    _delete_by_id("positions", entry_id)


# ── Achievements ──────────────────────────────────────────────────────────────

def get_achievements(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM achievements WHERE user_id = %s ORDER BY date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_achievement(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO achievements (user_id, title, description, date)
        VALUES (%s, %s, %s, %s)
    """, (user_id, data["title"], data.get("description"), data.get("date")))
    conn.commit()
    conn.close()


def delete_achievement(entry_id: int):
    _delete_by_id("achievements", entry_id)


# ── Shared helper ─────────────────────────────────────────────────────────────

def _delete_by_id(table: str, entry_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id = %s", (entry_id,))
    conn.commit()
    conn.close()