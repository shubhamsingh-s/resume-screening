import os
import PyPDF2
from docx import Document
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
from services.ml_model_service import ml_model_service

class ResumeService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        # Use the comprehensive skills database from job_dataset
        from data.job_dataset import SKILLS_DATABASE
        self.skills_keywords = [skill.lower() for skill in SKILLS_DATABASE]
        
    def analyze_resume(self, filepath, use_ml_enhancement=True):
        """Analyze resume and extract key information with optional ML enhancement"""
        try:
            # Extract text from resume
            text = self.extract_text(filepath)
            
            # Extract skills using traditional method
            skills = self.extract_skills(text)
            
            # Enhance with ML if available
            if use_ml_enhancement and ml_model_service.trained:
                ml_skills = ml_model_service.extract_skills_ml(text)
                # Combine and deduplicate skills
                all_skills = list(set(skills + ml_skills))
                skills = all_skills
            
            # Extract experience
            experience = self.extract_experience(text)
            
            # Extract education
            education = self.extract_education(text)
            
            # Calculate match score based on skills count
            match_score = min(100, len(skills) * 5)  # Adjusted scoring
            
            result = {
                'skills': skills,
                'experience': experience,
                'education': education,
                'score': match_score,
                'skills_count': len(skills),
                'text_preview': text[:500] + '...' if len(text) > 500 else text,
                'analysis_method': 'hybrid_ai_ml' if use_ml_enhancement and ml_model_service.trained else 'traditional'
            }
            
            # Add ML-specific data if used
            if use_ml_enhancement and ml_model_service.trained:
                result['ml_enhanced'] = True
                result['ml_extracted_skills_count'] = len(ml_skills) if 'ml_skills' in locals() else 0
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def extract_text(self, filepath):
        """Extract text from PDF, DOCX, or TXT file"""
        file_extension = os.path.splitext(filepath)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(filepath)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(filepath)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(filepath)
        else:
            raise ValueError("Unsupported file format")
    
    def extract_text_from_pdf(self, filepath):
        """Extract text from PDF file"""
        text = ""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def extract_text_from_docx(self, filepath):
        """Extract text from DOCX file"""
        doc = Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def extract_text_from_txt(self, filepath):
        """Extract text from TXT file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skills_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))
    
    def extract_experience(self, text):
        """Extract experience information"""
        # Simple regex to find years of experience
        experience_patterns = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\s*\+\s*years?',
            r'experience:\s*(\d+)\s*years?'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return f"{match.group(1)} years"
        
        return "Experience not specified"
    
    def extract_education(self, text):
        """Extract education information"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'associate',
            'b.s.', 'm.s.', 'b.a.', 'm.a.', 'mba'
        ]
        
        text_lower = text.lower()
        for edu in education_keywords:
            if edu in text_lower:
                return edu.title() + "'s Degree"
        
        return "Education not specified"
    
    def batch_analyze_resumes(self, filepaths: list, use_ml_enhancement=True) -> list:
        """Analyze multiple resumes in batch"""
        results = []
        for filepath in filepaths:
            try:
                result = self.analyze_resume(filepath, use_ml_enhancement)
                result['filename'] = os.path.basename(filepath)
                results.append(result)
            except Exception as e:
                results.append({
                    'filename': os.path.basename(filepath),
                    'error': str(e),
                    'status': 'failed'
                })
        return results
    
    def analyze_resume_text(self, text: str, use_ml_enhancement=True) -> dict:
        """Analyze resume text directly (for testing and batch processing)"""
        try:
            # Extract skills using traditional method
            skills = self.extract_skills(text)
            
            # Enhance with ML if available
            if use_ml_enhancement and ml_model_service.trained:
                ml_skills = ml_model_service.extract_skills_ml(text)
                # Combine and deduplicate skills
                all_skills = list(set(skills + ml_skills))
                skills = all_skills
            
            # Extract experience
            experience = self.extract_experience(text)
            
            # Extract education
            education = self.extract_education(text)
            
            # Calculate match score based on skills count
            match_score = min(100, len(skills) * 5)
            
            result = {
                'skills': skills,
                'experience': experience,
                'education': education,
                'score': match_score,
                'skills_count': len(skills),
                'text_preview': text[:500] + '...' if len(text) > 500 else text,
                'analysis_method': 'hybrid_ai_ml' if use_ml_enhancement and ml_model_service.trained else 'traditional'
            }
            
            # Add ML-specific data if used
            if use_ml_enhancement and ml_model_service.trained:
                result['ml_enhanced'] = True
                result['ml_extracted_skills_count'] = len(ml_skills) if 'ml_skills' in locals() else 0
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
