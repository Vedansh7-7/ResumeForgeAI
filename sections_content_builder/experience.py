import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_experience_section(jd_experience_text: str, user_experience_text: str, general_text: str = "") -> str | None:
    if not jd_experience_text.strip():
        jd_experience_text = general_text if general_text.strip() else "Software development, problem solving, collaboration, building projects"

    system_prompt = load_prompt("experience_prompt.txt")
    client = Groq()

    user_message = f"""
=== JD EXPERIENCE REQUIREMENTS ===
{jd_experience_text}

=== CANDIDATE EXPERIENCE ===
{user_experience_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    if raw == "NO_MATCH" or raw.startswith("NO_MATCH"):
        return None

    return raw


if __name__ == "__main__":

    test_jd_experience = """
    Hands-on exposure to Machine Learning, Deep Learning, Generative AI, NLP,
    predictive analytics. Assist in building and training ML models.
    Perform data preprocessing, feature engineering, and model optimization.
    Analyze structured and unstructured datasets for insights.
    Work on NLP and Generative AI-related projects.
    """

    # Demo 1 — relevant experience (should generate bullet points)
    test_user_experience_1 = """
    Vikram Sarabhai Space Centre | Jan 2025 - Present
    Data Analysis and Management Intern, Space Physics Laboratory, VSSC, ISRO | Remote, Certificate
    I worked on analyzing and comparing multiple data processing pipelines for James Webb Space
    Telescope image data. My work involved installing and operating the Eureka pipeline as the base,
    then setting up Nemesis and ExoIris pipelines and comparing their outputs. I used Python and
    pandas for preprocessing the datasets and performed feature analysis to understand spectral
    differences across pipeline outputs. I also wrote scripts to automate batch processing and
    generate visualizations using Matplotlib.
    """

    # Demo 2 — partially relevant experience (should generate bullet points)
    test_user_experience_2 = """
    IIT Indore | Aug 2024 - Nov 2024
    Research Assistant, Department of Computer Science | On-campus
    I assisted a professor in a project on retrieval-augmented generation systems. The work involved
    reading recent papers on RAG architectures, setting up a FAISS-based vector store, and running
    experiments with different chunking and embedding strategies. I also helped preprocess a dataset
    of 10,000 academic abstracts using Python and wrote a small evaluation script to measure
    retrieval accuracy.
    """

    # Demo 3 — irrelevant experience (should return NO_MATCH)
    test_user_experience_3 = """
    Local NGO | Summer 2023
    Volunteer Coordinator | Indore, India
    I coordinated with local volunteers for a tree plantation drive across 5 villages. Managed
    scheduling, communication with team leads, and maintained attendance records in Excel. Helped
    organize a fundraising event that collected donations from over 200 people.
    """

    # print("--- TEST 1 (relevant) ---")
    r1 = get_experience_section(test_jd_experience, test_user_experience_1)
    print(r1 if r1 else "")

    # print("\n--- TEST 2 (partially relevant) ---")
    r2 = get_experience_section(test_jd_experience, test_user_experience_2)
    print(r2 if r2 else "")

    # print("\n--- TEST 3 (irrelevant) ---")
    r3 = get_experience_section(test_jd_experience, test_user_experience_3)
    print(r3 if r3 else "")