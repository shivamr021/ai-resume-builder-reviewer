from reviewer.resume_parser import extract_text_from_pdf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from insights.utils import clean_resume_text
from sentence_transformers import SentenceTransformer, util

# Generic fallback keywords
GENERIC_KEYWORDS = [
    "python", "django", "streamlit", "html", "css", "javascript", "machine learning",
    "data analysis", "sql", "github", "flask", "react", "project", "team", "problem solving"
]

# Preload SBERT model once
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_ats_score(resume_text, job_description=None):
    resume_text_clean = clean_resume_text(resume_text)

    if job_description:
        jd_clean = clean_resume_text(job_description)
        resume_embedding = sbert_model.encode(resume_text_clean, convert_to_tensor=True)
        jd_embedding = sbert_model.encode(jd_clean, convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(resume_embedding, jd_embedding).item()
        score = round(similarity_score * 100, 2)

        return {
            "score": score,
            "fallback_mode": False,
            "matched": [],
            "missing": []
        }
    else:
        matched_keywords = [kw for kw in GENERIC_KEYWORDS if kw in resume_text_clean]
        richness_score = len(matched_keywords) / len(GENERIC_KEYWORDS) * 100

        return {
            "score": round(richness_score, 2),
            "fallback_mode": True,
            "resume_keywords": matched_keywords
        }
