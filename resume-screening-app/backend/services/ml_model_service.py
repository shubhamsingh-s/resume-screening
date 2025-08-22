"""
ML Model Service for Resume Screening System
Integrates traditional ML models with the existing AI system
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import os

class MLModelService:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.skills_matrix = None
        self.job_skills_matrix = None
        self.trained = False
        
    def load_training_data(self, training_data_path: str = "processed_resumes/training_data.json"):
        """Load training data from processed resumes"""
        try:
            with open(training_data_path, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
            return training_data
        except FileNotFoundError:
            print(f"Training data not found at {training_data_path}")
            return []
    
    def train_models(self, training_data: List[Dict[str, Any]]):
        """Train ML models on the processed resume data"""
        if not training_data:
            print("No training data available")
            return False
        
        # Extract texts and skills for training
        texts = [item['text'] for item in training_data]
        skills_lists = [item['skills'] for item in training_data]
        
        # Train TF-IDF vectorizer
        self.tfidf_vectorizer.fit(texts)
        
        # Create skills vocabulary for matching
        all_skills = set()
        for skills in skills_lists:
            all_skills.update(skills)
        
        self.skills_vocabulary = list(all_skills)
        print(f"Trained models with {len(texts)} resumes and {len(self.skills_vocabulary)} unique skills")
        self.trained = True
        return True
    
    def extract_skills_ml(self, text: str, top_n: int = 10) -> List[str]:
        """Extract skills using ML approach"""
        if not self.trained:
            return []
        
        # Vectorize the text
        text_vector = self.tfidf_vectorizer.transform([text])
        
        # For simplicity, we'll use a keyword-based approach enhanced with ML
        # In a real system, this would use a trained classifier
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_vocabulary:
            skill_lower = skill.lower()
            # Use both exact match and partial match with ML confidence
            if (skill_lower in text_lower or 
                f" {skill_lower} " in text_lower or
                text_lower.startswith(skill_lower) or
                text_lower.endswith(skill_lower)):
                found_skills.append(skill)
        
        return found_skills[:top_n]
    
    def calculate_skill_match_score(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate match score between resume skills and job requirements"""
        if not job_skills:
            return 0.0
        
        resume_skills_set = set(resume_skills)
        job_skills_set = set(job_skills)
        
        # Calculate Jaccard similarity
        intersection = len(resume_skills_set.intersection(job_skills_set))
        union = len(resume_skills_set.union(job_skills_set))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def enhance_with_ml(self, analysis_result: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
        """Enhance AI analysis with ML results"""
        if not self.trained:
            return analysis_result
        
        # Extract skills using ML
        ml_skills = self.extract_skills_ml(resume_text)
        
        # Enhance the analysis result
        enhanced_result = analysis_result.copy()
        
        # Combine AI and ML extracted skills (remove duplicates)
        all_skills = list(set(analysis_result.get('extracted_skills', []) + ml_skills))
        enhanced_result['extracted_skills'] = all_skills
        enhanced_result['skills_extraction_method'] = 'hybrid_ai_ml'
        enhanced_result['ml_extracted_skills'] = ml_skills
        
        # Recalculate match scores with enhanced skills
        if 'job_recommendations' in enhanced_result:
            for job_rec in enhanced_result['job_recommendations']:
                job_skills = job_rec.get('required_skills', [])
                match_score = self.calculate_skill_match_score(all_skills, job_skills)
                job_rec['match_score'] = match_score
                job_rec['match_percentage'] = round(match_score * 100, 2)
        
        return enhanced_result
    
    def batch_process_resumes(self, resume_texts: List[str]) -> List[Dict[str, Any]]:
        """Process multiple resumes in batch"""
        if not self.trained:
            return []
        
        results = []
        for text in resume_texts:
            ml_skills = self.extract_skills_ml(text)
            results.append({
                'ml_extracted_skills': ml_skills,
                'skills_count': len(ml_skills)
            })
        
        return results

# Singleton instance
ml_model_service = MLModelService()

def initialize_ml_models():
    """Initialize ML models with training data"""
    training_data = ml_model_service.load_training_data()
    if training_data:
        success = ml_model_service.train_models(training_data)
        if success:
            print("ML models initialized successfully")
        else:
            print("Failed to train ML models")
    else:
        print("No training data available for ML models")

# Initialize on import
initialize_ml_models()
