import requests
import json

def test_resume_job_matching():
    """Test the resume-job matching functionality"""
    
    # Test data - sample resume text and job description
    resume_text = """
    John Doe
    Software Developer
    
    Experience:
    - 5+ years of experience in Python development
    - Strong knowledge of React and JavaScript
    - Experience with machine learning and data analysis
    - Worked on cloud platforms like AWS and Azure
    
    Skills: Python, React, JavaScript, Machine Learning, AWS, Azure, SQL
    
    Education: Bachelor's in Computer Science
    """
    
    job_description = """
    We are looking for a Senior Software Developer with strong experience in:
    - Python programming
    - React framework
    - JavaScript development
    - Cloud platforms (AWS preferred)
    - Machine learning concepts
    
    Requirements:
    - 3+ years of professional experience
    - Strong problem-solving skills
    - Experience with agile development methodologies
    """
    
    # Create a temporary text file for the resume
    with open('test_resume.txt', 'w', encoding='utf-8') as f:
        f.write(resume_text)
    
    try:
        # Test the match_resume_job endpoint
        url = 'http://localhost:5000/match_resume_job'
        
        # Prepare the form data
        files = {
            'resume_file': ('test_resume.txt', open('test_resume.txt', 'rb'), 'text/plain')
        }
        data = {
            'job_description': job_description
        }
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Matching test successful!")
            print(f"Match Score: {result['match_score']}%")
            print(f"Matched Skills: {result['matched_skills']}")
            print(f"Missing Skills: {result['missing_skills']}")
            print(f"Resume Skills Count: {result['resume_skills_count']}")
            print(f"Job Skills Count: {result['job_skills_count']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
    
    finally:
        # Clean up
        import os
        if os.path.exists('test_resume.txt'):
            os.remove('test_resume.txt')

def test_ml_status():
    """Test ML model status"""
    try:
        response = requests.get('http://localhost:5000/api/ml/status')
        if response.status_code == 200:
            status = response.json()
            print("✅ ML Status:")
            print(f"ML Trained: {status['ml_trained']}")
            print(f"Unique Skills Count: {status['unique_skills_count']}")
            print(f"Models Available: {status['models_available']}")
        else:
            print(f"❌ ML Status Error: {response.status_code}")
    except Exception as e:
        print(f"❌ ML Status Exception: {e}")

if __name__ == "__main__":
    print("Testing Resume-Job Matching System...")
    print("=" * 50)
    
    test_ml_status()
    print("\n" + "=" * 50)
    test_resume_job_matching()
