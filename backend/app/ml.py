import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python", "javascript", "typescript", "react", "node", "fastapi", "flask",
    "sql", "postgresql", "mongodb", "docker", "kubernetes", "aws", "azure",
    "git", "github actions", "ci/cd", "pandas", "numpy", "scikit-learn",
    "machine learning", "deep learning", "tensorflow", "pytorch", "tableau",
    "power bi", "rest api", "agile", "linux", "html", "css"
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def extract_skills(text: str) -> list[str]:
    normalized = normalize(text)
    return [skill for skill in SKILLS if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", normalized)]

def analyze_match(resume: str, job: str) -> dict:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([resume, job])
    semantic_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    resume_skills, job_skills = set(extract_skills(resume)), set(extract_skills(job))
    matched, missing = sorted(resume_skills & job_skills), sorted(job_skills - resume_skills)
    skill_score = len(matched) / len(job_skills) if job_skills else semantic_score
    score = round(min(100, (semantic_score * 45 + skill_score * 55) * 100))
    if score >= 75:
        fit_level = "Strong match"
    elif score >= 50:
        fit_level = "Promising match"
    else:
        fit_level = "Growth opportunity"
    recommendations = []
    if missing:
        recommendations.append("Add evidence of " + ", ".join(missing[:4]) + " where it truthfully reflects your experience.")
    if not matched:
        recommendations.append("Tailor your summary with relevant tools and measurable outcomes from the role.")
    recommendations.append("Mirror key terminology from the job description in your project and achievement bullets.")
    return {"score": score, "fit_level": fit_level, "matched_skills": matched, "missing_skills": missing, "recommendations": recommendations}
