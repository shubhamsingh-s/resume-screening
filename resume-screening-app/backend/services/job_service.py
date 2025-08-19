import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

class JobService:
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
        
    def extract_skills(self, job_description):
        """Extract skills from job description"""
        text_lower = job_description.lower()
        found_skills = []
        
        for skill in self.skills_keywords:
            if skill.lower() in text_lower:
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
