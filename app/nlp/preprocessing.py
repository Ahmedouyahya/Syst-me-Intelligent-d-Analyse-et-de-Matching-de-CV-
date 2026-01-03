import spacy
import re
import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from typing import List, Dict, Any

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Load Spacy model
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = spacy.blank("fr")

def load_keywords():
    """Loads skills keywords from JSON file."""
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'competences_keywords.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

KEYWORDS = load_keywords()

def clean_text(text: str) -> str:
    """Cleans text by removing special characters and extra spaces."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s@.-]', '', text)
    return text.strip()

def extract_emails(text: str) -> List[str]:
    """Extracts emails using regex."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(email_pattern, text)))

def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extracts skills based on the loaded JSON dictionary.
    """
    found_skills = {
        "languages": [],
        "frameworks": [],
        "tools": [],
        "soft_skills": []
    }
    
    lower_text = text.lower()
    
    for category, skills in KEYWORDS.items():
        for skill in skills:
            # Regex for whole word matching
            if re.search(r'\b' + re.escape(skill) + r'\b', lower_text):
                found_skills[category].append(skill)
                
    return found_skills

def extract_education_level(text: str) -> List[str]:
    """
    Extracts education levels based on keywords.
    """
    education_keywords = [
        "bac", "baccalauréat", "licence", "bachelor", "master", "mastère", 
        "ingénieur", "doctorat", "phd", "mba", "dut", "bts", "deug"
    ]
    found_education = []
    lower_text = text.lower()
    for keyword in education_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', lower_text):
            found_education.append(keyword)
    return list(set(found_education))

def preprocess_cv(text: str) -> Dict[str, Any]:
    """
    Performs full preprocessing and extraction on CV text.
    """
    cleaned_text = clean_text(text)
    emails = extract_emails(text)
    skills = extract_skills(cleaned_text)
    education = extract_education_level(cleaned_text)
    
    # Basic entity extraction with Spacy
    doc = nlp(cleaned_text)
    entities = {
        "ORG": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
        "PERSON": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        "GPE": [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    }

    return {
        "cleaned_text": cleaned_text,
        "emails": emails,
        "skills": skills,
        "education": education,
        "entities": entities
    }

def preprocess_job_description(text: str) -> Dict[str, Any]:
    """
    Analyzes job description to extract requirements.
    """
    cleaned_text = clean_text(text)
    skills = extract_skills(cleaned_text)
    education = extract_education_level(cleaned_text)
    
    return {
        "cleaned_text": cleaned_text,
        "required_skills": skills,
        "required_education": education
    }
