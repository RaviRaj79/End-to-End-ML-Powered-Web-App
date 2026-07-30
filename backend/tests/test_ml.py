from app.ml import analyze_match, extract_skills, normalize

def test_normalize_removes_extra_space(): assert normalize(" Python   React ") == "python react"
def test_extracts_known_skills(): assert set(extract_skills("Python, React and Docker")) == {"python", "react", "docker"}
def test_does_not_match_partial_words(): assert "sql" not in extract_skills("nosql database")
def test_exact_skill_match_scores_high(): assert analyze_match("Python React Docker SQL", "Python React Docker SQL")["score"] >= 90
def test_missing_skills_are_identified(): assert "docker" in analyze_match("Python", "Python Docker")["missing_skills"]
def test_matched_skills_are_identified(): assert "python" in analyze_match("Python", "Python Docker")["matched_skills"]
def test_has_recommendations(): assert analyze_match("Java", "Python Docker")["recommendations"]
def test_score_is_bounded(): assert 0 <= analyze_match("hello world", "different content")["score"] <= 100
