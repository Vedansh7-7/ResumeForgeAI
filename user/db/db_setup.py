"""
db_setup.py

Run this ONCE to create the database and all tables.
After that, never run it again unless you want to reset everything.

Run with:
    python user/db/db_setup.py
"""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG_NO_DB = {
    "host":     os.getenv("DB_HOST"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}
DATABASE_NAME = "resume_platform"


# ── All CREATE TABLE statements ───────────────────────────────────────────────

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (name)
);
"""

CREATE_PERSONAL_INFO = """
CREATE TABLE IF NOT EXISTS personal_info (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    email       VARCHAR(200),
    phone       VARCHAR(30),
    city        VARCHAR(100),
    linkedin    VARCHAR(300),
    github      VARCHAR(300),
    portfolio   VARCHAR(300),

    UNIQUE (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_EDUCATION = """
CREATE TABLE IF NOT EXISTS education (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    institution     VARCHAR(200) NOT NULL,
    degree          VARCHAR(200) NOT NULL,
    field_of_study  VARCHAR(200),
    start_date      VARCHAR(50),
    end_date        VARCHAR(50),
    grade           VARCHAR(50),

    UNIQUE (user_id, institution, degree, field_of_study),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_EXPERIENCE = """
CREATE TABLE IF NOT EXISTS experience (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    company     VARCHAR(200) NOT NULL,
    role        VARCHAR(200) NOT NULL,
    location    VARCHAR(200),
    start_date  VARCHAR(50),
    end_date    VARCHAR(50),
    description TEXT,

    UNIQUE (user_id, company, role, start_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_PROJECTS = """
CREATE TABLE IF NOT EXISTS projects (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    name        VARCHAR(200) NOT NULL,
    tech_stack  VARCHAR(500),
    description TEXT,
    link        VARCHAR(300),

    UNIQUE (user_id, name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_TECHNICAL_SKILLS = """
CREATE TABLE IF NOT EXISTS technical_skills (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    category    VARCHAR(100),
    skill_name  VARCHAR(100) NOT NULL,

    UNIQUE (user_id, skill_name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_KEY_COURSES = """
CREATE TABLE IF NOT EXISTS key_courses (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    course_name VARCHAR(200) NOT NULL,
    description TEXT,

    UNIQUE (user_id, course_name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_POSITIONS = """
CREATE TABLE IF NOT EXISTS positions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    title           VARCHAR(200) NOT NULL,
    organisation    VARCHAR(200) NOT NULL,
    start_date      VARCHAR(50),
    end_date        VARCHAR(50),
    description     TEXT,

    UNIQUE (user_id, title, organisation, start_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_ACHIEVEMENTS = """
CREATE TABLE IF NOT EXISTS achievements (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    title       VARCHAR(300) NOT NULL,
    description TEXT,
    date        VARCHAR(50),

    UNIQUE (user_id, title),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

# ── Ordered list — users must come first because all others reference it ──────
ALL_TABLES = [
    ("users",             CREATE_USERS),
    ("personal_info",     CREATE_PERSONAL_INFO),
    ("education",         CREATE_EDUCATION),
    ("experience",        CREATE_EXPERIENCE),
    ("projects",          CREATE_PROJECTS),
    ("technical_skills",  CREATE_TECHNICAL_SKILLS),
    ("key_courses",       CREATE_KEY_COURSES),
    ("positions",         CREATE_POSITIONS),
    ("achievements",      CREATE_ACHIEVEMENTS),
]


def setup():
    try:
        # Step 1: connect without selecting a DB
        conn = mysql.connector.connect(**DB_CONFIG_NO_DB)
        cursor = conn.cursor()

        # Step 2: create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"✓ Database '{DATABASE_NAME}' ready")

        # Step 3: switch to it
        cursor.execute(f"USE {DATABASE_NAME}")

        # Step 4: create each table
        for table_name, sql in ALL_TABLES:
            cursor.execute(sql)
            print(f"✓ Table '{table_name}' ready")

        conn.commit()
        print("\n All done. Your database is set up and ready to use.")

    except Error as e:
        print(f"\n[ERROR] {e}")
        print("Make sure MySQL is running and your password is correct.")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    setup()