"""
generate_resume.py
------------------
Renders resume JSON → .tex → PDF using Jinja2 + pdflatex.

Usage:
    python generate_resume.py
    python generate_resume.py --json path/to/schema.json --out output/
"""

import os
import json
import shutil
import argparse
import subprocess
from jinja2 import Environment, FileSystemLoader


# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR  = os.path.join(BASE_DIR, "templates")
TEMPLATE_FILE = "resume_template.tex"
DEFAULT_JSON  = os.path.join(BASE_DIR, "resume_data.json")
OUTPUT_DIR    = os.path.join(BASE_DIR, "output")


# ── Jinja2 Environment ────────────────────────────────────────────────────────
# Custom delimiters so Jinja doesn't clash with LaTeX {{ }} and {% %}
def get_jinja_env():
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        block_start_string    = '((*',
        block_end_string      = '*))',
        variable_start_string = '(((',
        variable_end_string   = ')))',
        comment_start_string  = '((#',
        comment_end_string    = '#))',
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        return text
    replacements = [
        ('&',  r'\&'),
        ('%',  r'\%'),
        ('$',  r'\$'),
        ('#',  r'\#'),
        ('_',  r'\_'),
        ('~',  r'\textasciitilde{}'),
        ('^',  r'\textasciicircum{}'),
    ]
    for char, escaped in replacements:
        text = text.replace(char, escaped)
    return text

def escape_data(obj):
    if isinstance(obj, str):
        return escape_latex(obj)
    elif isinstance(obj, list):
        return [escape_data(i) for i in obj]
    elif isinstance(obj, dict):
        return {escape_latex(k): escape_data(v) for k, v in obj.items()}  # ← escape keys too
    return obj


# ── Render ────────────────────────────────────────────────────────────────────

def render_tex(data: dict, output_tex_path: str):
    """Render the Jinja2 template with data and write .tex file."""
    env      = get_jinja_env()
    template = env.get_template(TEMPLATE_FILE)
    rendered = template.render(**escape_data(data))

    with open(output_tex_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✓ .tex file written: {output_tex_path}")


# ── Compile ───────────────────────────────────────────────────────────────────

def compile_pdf(tex_path: str, output_dir: str) -> str:
    """
    Compile .tex to PDF using pdflatex.
    Returns the path of the generated PDF.
    """
    if not shutil.which("pdflatex"):
        raise EnvironmentError(
            "pdflatex not found. Install MiKTeX (Windows) or TeX Live (Linux/Mac).\n"
            "Windows: https://miktex.org/download\n"
            "Linux:   sudo apt install texlive-latex-recommended texlive-fonts-recommended"
        )

    result = subprocess.run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            f"-output-directory={output_dir}",
            tex_path,
        ],
        capture_output=True,
        text=True,
    )

    pdf_path = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(tex_path))[0] + ".pdf"
    )

    if result.returncode != 0:
        log_path = pdf_path.replace(".pdf", ".log")
        print(f"\n[LaTeX ERROR] pdflatex failed. Check log: {log_path}")
        print(result.stdout[-2000:])   # last 2000 chars of output
        raise RuntimeError("pdflatex compilation failed.")

    print(f"✓ PDF compiled:  {pdf_path}")
    return pdf_path


# ── Main ──────────────────────────────────────────────────────────────────────

def generate(json_path: str = DEFAULT_JSON, output_dir: str = OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)

    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    user_name = data.get("personal", {}).get("name", "resume").replace(" ", "_")
    tex_path  = os.path.join(output_dir, f"{user_name}_resume.tex")

    # Render .tex
    render_tex(data, tex_path)

    # Compile PDF
    pdf_path = compile_pdf(tex_path, output_dir)

    return pdf_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render resume JSON to PDF")
    parser.add_argument("--json", default=DEFAULT_JSON, help="Path to resume JSON schema")
    parser.add_argument("--out",  default=OUTPUT_DIR,   help="Output directory")
    args = parser.parse_args()

    pdf = generate(json_path=args.json, output_dir=args.out)
    print(f"\nDone → {pdf}")