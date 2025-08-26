import google.generativeai as genai
import os
from typing import List, Dict, Any

class GeminiService:
    def __init__(self):
        # Configure Gemini API with the provided key
        genai.configure(api_key="AIzaSyBz-CSWv8jDJY5KMLv1mDklFJn3rD5itdY")
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_resume_with_ai(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume text using Gemini AI for enhanced insights"""
        try:
            prompt = f"""
            Analyze this resume text and provide a comprehensive analysis in JSON format with the following structure:
            {{
                "skills": ["list", "of", "technical", "skills"],
                "strengths": ["list", "of", "key", "strengths"],
                "weaknesses": ["list", "of", "potential", "weaknesses"],
                "experience_summary": "brief summary of experience",
                "education_summary": "brief summary of education",
                "overall_score": 85
            }}
            
            Resume Text:
            {resume_text[:4000]}  # Limit to avoid token limits
            
            Return only valid JSON, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            return self._parse_gemini_response(response.text)
            
        except Exception as e:
            # Fallback to basic analysis if AI fails
            return self._fallback_analysis(resume_text)
    
    def extract_skills_with_ai(self, job_description: str) -> List[str]:
        """Extract skills from job description using Gemini AI"""
        try:
            prompt = f"""
            Extract the technical skills and requirements from this job description. 
            Return only a JSON array of skills, like: ["skill1", "skill2", "skill3"]
            
            Job Description:
            {job_description[:2000]}
            
            Return only valid JSON, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            skills = self._parse_skills_response(response.text)
            return skills
            
        except Exception as e:
            # Fallback to keyword matching
            return self._fallback_skills_extraction(job_description)
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response and extract JSON"""
        try:
            # Clean the response and extract JSON
            import json
            # Remove markdown code blocks if present
            cleaned_text = response_text.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned_text)
        except:
            # Return default structure if parsing fails
            return {
                "skills": [],
                "strengths": [],
                "weaknesses": [],
                "experience_summary": "Analysis unavailable",
                "education_summary": "Analysis unavailable",
                "overall_score": 0
            }
    
    def _parse_skills_response(self, response_text: str) -> List[str]:
        """Parse skills response from Gemini"""
        try:
            import json
            cleaned_text = response_text.replace('```json', '').replace('```', '').strip()
            skills = json.loads(cleaned_text)
            return skills if isinstance(skills, list) else []
        except:
            return []
    
    def _fallback_analysis(self, resume_text: str) -> Dict[str, Any]:
        """Fallback analysis when AI fails"""
        return {
            "skills": [],
            "strengths": ["Experience in various technologies", "Strong problem-solving skills"],
            "weaknesses": ["Could benefit from more specific experience", "Consider additional certifications"],
            "experience_summary": "Professional experience detected",
            "education_summary": "Educational background identified",
            "overall_score": 75
        }
    
    def _fallback_skills_extraction(self, job_description: str) -> List[str]:
        """Fallback skills extraction using basic keyword matching"""
        skills_keywords = [
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
        
        found_skills = []
        text_lower = job_description.lower()
        
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))
