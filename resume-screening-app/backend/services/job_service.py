import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import os
import sys

# Add the data directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from job_dataset import JOB_DATASET, SKILLS_DATABASE, get_job_by_title, get_skills_for_job

class JobService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skills_keywords = [skill.lower() for skill in SKILLS_DATABASE]
        
    def extract_skills(self, job_description):
        """Extract skills from job description using enhanced matching"""
        text_lower = job_description.lower()
        found_skills = []
        
        # First, check if this matches any predefined job description
        for job_key, job_data in JOB_DATASET.items():
            job_desc_lower = job_data['description'].lower()
            # Simple similarity check - if significant overlap, use predefined skills
            common_words = set(text_lower.split()) & set(job_desc_lower.split())
            if len(common_words) > 10:  # Threshold for similarity
                found_skills.extend(job_data['required_skills'])
                break
        
        # If no predefined job matched, use keyword extraction
        if not found_skills:
            for skill in self.skills_keywords:
                # Use regex for better matching (whole word matching)
                if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                    found_skills.append(skill.title())
        
        # Remove duplicates and sort
        return sorted(list(set(found_skills)))
    
    def recommend_jobs(self, user_skills):
        """Recommend jobs based on user skills"""
        # Mock job database
        mock_jobs = [
            {
                'title': 'Senior React Developer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'salary': '$120k - $150k',
                'required_skills': ['React', 'JavaScript', 'TypeScript', 'Node.js'],
                'description': 'Looking for an experienced React developer to join our team.'
            },
            {
                'title': 'Full Stack Engineer',
                'company': 'StartupXYZ',
                'location': 'Remote',
                'salary': '$100k - $130k',
                'required_skills': ['Python', 'React', 'AWS', 'Docker'],
                'description': 'Join our growing startup as a full-stack engineer.'
            },
            {
                'title': 'Machine Learning Engineer',
                'company': 'AI Solutions',
                'location': 'New York, NY',
                'salary': '$130k - $160k',
                'required_skills': ['Python', 'Machine Learning', 'TensorFlow', 'NLP'],
                'description': 'Work on cutting-edge AI projects with our ML team.'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'CloudTech',
                'location': 'Austin, TX',
                'salary': '$110k - $140k',
                'required_skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
                'description': 'Manage and optimize our cloud infrastructure.'
            },
            {
                'title': 'Data Scientist',
                'company': 'DataCorp',
                'location': 'Boston, MA',
                'salary': '$125k - $155k',
                'required_skills': ['Python', 'Machine Learning', 'Pandas', 'SQL'],
                'description': 'Analyze complex datasets and build predictive models.'
            }
        ]
        
        recommendations = []
        user_skills_set = set(skill.lower() for skill in user_skills)
        
        for job in mock_jobs:
            job_skills_set = set(skill.lower() for skill in job['required_skills'])
            
            # Calculate match percentage
            matched_skills = user_skills_set.intersection(job_skills_set)
            match_percentage = int((len(matched_skills) / len(job_skills_set)) * 100)
            
            if match_percentage > 50:  # Only include jobs with >50% match
                recommendations.append({
                    'title': job['title'],
                    'company': job['company'],
                    'location': job['location'],
                    'salary': job['salary'],
                    'match': match_percentage,
                    'skills': job['required_skills'],
                    'description': job['description']
                })
        
        # Sort by match percentage (descending)
        recommendations.sort(key=lambda x: x['match'], reverse=True)
        
        return recommendations
    
    def calculate_job_match(self, user_skills, job_skills):
        """Calculate match percentage between user skills and job requirements"""
        user_skills_set = set(skill.lower() for skill in user_skills)
        job_skills_set = set(skill.lower() for skill in job_skills)
        
        matched_skills = user_skills_set.intersection(job_skills_set)
        match_percentage = int((len(matched_skills) / len(job_skills_set)) * 100)
        
        return match_percentage
