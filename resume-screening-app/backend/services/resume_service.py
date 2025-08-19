import os
import PyPDF2
from docx import Document
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

class ResumeService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skills_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
            'django', 'flask', 'spring', 'spring boot', 'mongodb', 'mysql', 'postgresql',
            'sql', 'nosql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'git', 'github', 'gitlab', 'ci/cd', 'machine learning', 'deep learning',
            'artificial intelligence', 'data science', 'data analysis', 'pandas', 'numpy',
            'scikit-learn', 'tensorflow', 'pytorch', 'nlp', 'computer vision', 'rest api',
            'graphql', 'microservices', 'agile', 'scrum', 'kanban', 'linux', 'unix',
            'html', 'css', 'sass', 'less', 'typescript', 'redux', 'vuex', 'next.js',
            'nuxt.js', 'gatsby', 'tailwind', 'bootstrap', 'material-ui', 'ant design'
        ]
        
    def analyze_resume(self, filepath):
        """Analyze resume and extract key information"""
        try:
            # Extract text from resume
            text = self.extract_text(filepath)
            
            # Extract skills
            skills = self.extract_skills(text)
            
            # Extract experience
            experience = self.extract_experience(text)
            
            # Extract education
            education = self.extract_education(text)
            
            # Calculate match score (mock implementation)
            match_score = min(100, len(skills) * 10)
            
            return {
                'skills': skills,
                'experience': experience,
                'education': education,
                'score': match_score,
                'text': text[:500] + '...' if len(text) > 500 else text
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def extract_text(self, filepath):
        """Extract text from PDF or DOCX file"""
        file_extension = os.path.splitext(filepath)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(filepath)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(filepath)
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
