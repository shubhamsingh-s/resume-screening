#!/usr/bin/env python3
"""
Integration test script for the complete resume screening system
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🧪 Testing Health Endpoint")
    print("=" * 40)
    try:
        response = requests.get('http://localhost:5000/api/health')
        result = response.json()
        print(f"✅ Status: {result['status']}")
        print(f"✅ Message: {result['message']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ml_status():
    """Test the ML status endpoint"""
    print("\n🧪 Testing ML Status Endpoint")
    print("=" * 40)
    try:
        response = requests.get('http://localhost:5000/api/ml/status')
        result = response.json()
        print(f"✅ ML Trained: {result['ml_trained']}")
        print(f"✅ Unique Skills: {result['unique_skills_count']}")
        print(f"✅ Models Available: {result['models_available']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_job_skills_extraction():
    """Test job skills extraction"""
    print("\n🧪 Testing Job Skills Extraction")
    print("=" * 40)
    job_description = """
    We are looking for a Senior Python Developer with experience in:
    - Python programming
    - Django framework
    - REST APIs
    - PostgreSQL database
    - AWS cloud services
    - Docker containerization
    """
    
    try:
        response = requests.post(
            'http://localhost:5000/job_skills',
            json={'job_description': job_description}
        )
        result = response.json()
        print(f"✅ Extracted Skills: {result['skills']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_resume_job_matching():
    """Test resume-job matching functionality"""
    print("\n🧪 Testing Resume-Job Matching")
    print("=" * 40)
    
    # Create a simple test resume file
    test_resume = """
    John Doe - Senior Python Developer
    Skills: Python, Django, Flask, REST APIs, PostgreSQL, AWS, Docker
    Experience: 5+ years in software development
    Education: Bachelor's in Computer Science
    """
    
    with open('test_resume.txt', 'w', encoding='utf-8') as f:
        f.write(test_resume)
    
    job_description = "Looking for Python developer with Django experience"
    
    try:
        with open('test_resume.txt', 'rb') as f:
            response = requests.post(
                'http://localhost:5000/match_resume_job',
                files={'resume_file': ('test_resume.txt', f, 'text/plain')},
                data={'job_description': job_description}
            )
        
        result = response.json()
        print(f"✅ Match Score: {result['match_score']}%")
        print(f"✅ Matched Skills: {result['matched_skills']}")
        print(f"✅ Missing Skills: {result['missing_skills']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Clean up
        import os
        if os.path.exists('test_resume.txt'):
            os.remove('test_resume.txt')

def test_batch_processing():
    """Test batch resume processing"""
    print("\n🧪 Testing Batch Resume Processing")
    print("=" * 40)
    
    # Create test resumes
    test_resumes = []
    for i in range(3):
        content = f"""
        Developer {i+1}
        Skills: Python, JavaScript, React, Node.js
        Experience: {2+i} years
        Education: Computer Science Degree
        """
        filename = f'test_batch_{i+1}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        test_resumes.append(filename)
    
    try:
        files = []
        for filename in test_resumes:
            with open(filename, 'rb') as f:
                files.append(('files', (filename, f, 'text/plain')))
        
        response = requests.post(
            'http://localhost:5000/batch_analyze_resumes',
            files=files
        )
        
        result = response.json()
        print(f"✅ Total Resumes Processed: {result['total_resumes']}")
        print(f"✅ Status: {result['status']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Clean up
        import os
        for filename in test_resumes:
            if os.path.exists(filename):
                os.remove(filename)

def main():
    """Run all integration tests"""
    print("🚀 Starting Integration Tests for Resume Screening System")
    print("=" * 60)
    
    tests = [
        test_health_endpoint,
        test_ml_status,
        test_job_skills_extraction,
        test_resume_job_matching,
        test_batch_processing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed! System is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the system configuration.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
