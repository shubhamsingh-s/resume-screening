"""
ML Model Service for Resume Screening System
Integrates traditional ML models with the existing AI system
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from typing import List, Dict, Any
import os
import numpy as np

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
        
        # Train ML classifiers for each skill (multi-label classification)
        self.skill_classifiers = {}
        X = self.tfidf_vectorizer.transform(texts)
        
        for skill in self.skills_vocabulary:
            # Create binary labels for this skill
            y = np.array([1 if skill in skills else 0 for skills in skills_lists])
            
            if sum(y) > 1:  # Only train if we have positive examples
                # Split data for training
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                # Train Naive Bayes classifier
                clf = MultinomialNB()
                clf.fit(X_train, y_train)
                
                # Evaluate
                y_pred = clf.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                if accuracy > 0.6:  # Only keep reasonably accurate classifiers
                    self.skill_classifiers[skill] = clf
                    print(f"  Trained classifier for '{skill}' (accuracy: {accuracy:.2f})")
        
        print(f"Trained {len(self.skill_classifiers)} skill classifiers")
        self.trained = True
        
        # Save the trained models using joblib
        import joblib
        joblib.dump(self.tfidf_vectorizer, 'tfidf_vectorizer.joblib')
        joblib.dump(self.skill_classifiers, 'skill_classifiers.joblib')
        joblib.dump(self.skills_vocabulary, 'skills_vocabulary.joblib')
        print("Models saved successfully.")
        return True
    
    def extract_skills_ml(self, text: str, top_n: int = 15) -> List[str]:
        """Extract skills using ML approach with trained classifiers"""
        if not self.trained or not hasattr(self, 'skill_classifiers'):
            return []
        
        # Vectorize the text
        text_vector = self.tfidf_vectorizer.transform([text])
        
        # Use ML classifiers to predict skills
        ml_skills = []
        confidence_scores = []
        
        for skill, classifier in self.skill_classifiers.items():
            try:
                # Get prediction probability
                proba = classifier.predict_proba(text_vector)[0]
                confidence = proba[1]  # Probability of positive class
                
                if confidence > 0.3:  # Confidence threshold
                    ml_skills.append(skill)
                    confidence_scores.append(confidence)
            except:
                # Fallback to keyword matching if classifier fails
                if skill.lower() in text.lower():
                    ml_skills.append(skill)
                    confidence_scores.append(0.5)  # Default confidence
        
        # Sort by confidence and return top skills
        if ml_skills:
            sorted_skills = [skill for _, skill in sorted(zip(confidence_scores, ml_skills), reverse=True)]
            return sorted_skills[:top_n]
        
        # Fallback to keyword matching if no ML predictions
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_vocabulary:
            skill_lower = skill.lower()
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
