from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculates cosine similarity between two texts using TF-IDF.
    """
    if not text1 or not text2:
        return 0.0
        
    vectorizer = TfidfVectorizer(stop_words='english') # Should ideally use French stop words if content is French
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(score)
    except ValueError:
        return 0.0

def flatten_skills(skills_dict: Dict[str, List[str]]) -> List[str]:
    """Flattens the skills dictionary into a single list."""
    all_skills = []
    for category in skills_dict:
        all_skills.extend(skills_dict[category])
    return list(set(all_skills))

def calculate_skill_score(cv_skills: Dict[str, List[str]], job_skills: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Calculates score based on matching skills.
    """
    cv_flat = flatten_skills(cv_skills)
    job_flat = flatten_skills(job_skills)
    
    if not job_flat:
        return {"score": 0, "matches": [], "missing": []}
        
    cv_set = set(cv_flat)
    job_set = set(job_flat)
    
    matches = list(cv_set.intersection(job_set))
    missing = list(job_set - cv_set)
    
    score = len(matches) / len(job_set) if job_set else 0
    
    return {
        "score": score,
        "matches": matches,
        "missing": missing
    }

def calculate_education_score(cv_edu: List[str], job_edu: List[str]) -> float:
    """
    Calculates score based on matching education levels.
    """
    if not job_edu:
        return 1.0 # If no education specified, assume match
        
    cv_set = set(cv_edu)
    job_set = set(job_edu)
    
    matches = list(cv_set.intersection(job_set))
    
    # Simple logic: if any required education is present, score is 1.0, else 0.0
    # Can be improved with hierarchy (e.g. Master > Licence)
    return 1.0 if matches else 0.0

def match_profile(cv_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combines different metrics to produce a final compatibility score.
    Formula: Score = 0.5 * Skills + 0.3 * Experience + 0.2 * Education
    """
    # 1. Skill Match (S_comp)
    skill_metrics = calculate_skill_score(cv_data['skills'], job_data['required_skills'])
    s_comp = skill_metrics['score']
    
    # 2. Experience Match (S_exp)
    # We use Text Similarity as a proxy for Experience context match
    s_exp = calculate_similarity(cv_data['cleaned_text'], job_data['cleaned_text'])
    
    # 3. Education Match (S_form)
    s_form = calculate_education_score(cv_data.get('education', []), job_data.get('required_education', []))
    
    # Weighted Average
    final_score = (s_comp * 0.5) + (s_exp * 0.3) + (s_form * 0.2)
    
    return {
        "total_score": round(final_score * 100, 2),
        "text_similarity": round(s_exp * 100, 2), # Renamed for UI consistency, represents S_exp proxy
        "skill_score": round(s_comp * 100, 2),
        "education_score": round(s_form * 100, 2),
        "matching_skills": skill_metrics['matches'],
        "missing_skills": skill_metrics['missing']
    }
