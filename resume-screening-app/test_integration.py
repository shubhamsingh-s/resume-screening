#!/usr/bin/env python3
"""
Integration test script for Resume Screening API
Tests all major endpoints to ensure proper functionality
"""

import requests
import json
import os

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health endpoint: PASSED")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health endpoint: ERROR - {e}")
        return False

def test_ml_status():
    """Test ML status endpoint"""
    print("Testing ML status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/ml/status")
        if response.status_code == 200:
            print("✅ ML status endpoint: PASSED")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ ML status endpoint: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ ML status endpoint: ERROR - {e}")
        return False

def test_job_skills_extraction():
    """Test job skills extraction endpoint"""
    print("Testing job skills extraction...")
    try:
        job_description = "Looking for a Python developer with experience in Django, Flask, and machine learning. Knowledge of AWS and Docker is a plus."
        
        response = requests.post(
            f"{BASE_URL}/job_skills",
            json={"job_description": job_description},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Job skills extraction: PASSED")
            print(f"   Extracted skills: {result.get('skills', [])}")
            return True
        else:
            print(f"❌ Job skills extraction: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Job skills extraction: ERROR - {e}")
        return False

def test_batch_analyze_resumes():
    """Test batch resume analysis endpoint"""
    print("Testing batch resume analysis...")
    try:
        # Create a simple test resume file
        test_resume_content = """
        John Doe
        Software Developer
        
        Skills: Python, JavaScript, React, Node.js, AWS
        Experience: 5 years as full-stack developer
        Education: Bachelor's in Computer Science
        """
        
        # Create test files
        test_files = []
        for i in range(3):
            filename = f"test_resume_{i}.txt"
            with open(filename, 'w') as f:
                f.write(test_resume_content)
            test_files.append(('files', (filename, open(filename, 'rb'), 'text/plain')))
        
        response = requests.post(
            f"{BASE_URL}/batch_analyze_resumes",
            files=test_files
        )
        
        # Clean up test files
        for filename in [f"test_resume_{i}.txt" for i in range(3)]:
            if os.path.exists(filename):
                os.remove(filename)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Batch resume analysis: PASSED")
            print(f"   Processed {result.get('total_resumes', 0)} resumes")
            return True
        else:
            print(f"❌ Batch resume analysis: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Batch resume analysis: ERROR - {e}")
        return False

def test_match_resume_job():
    """Test resume-job matching endpoint"""
    print("Testing resume-job matching...")
    try:
        # Create a test resume file
        test_resume_content = """
        John Doe
        Software Developer
        
        Skills: Python, JavaScript, React, Node.js, AWS, Docker
        Experience: 5 years as full-stack developer
        Education: Bachelor's in Computer Science
        """
        
        with open('test_resume.txt', 'w') as f:
            f.write(test_resume_content)
        
        job_description = "Looking for a full-stack developer with Python, JavaScript, React, and AWS experience. Docker knowledge is preferred."
        
        response = requests.post(
            f"{BASE_URL}/match_resume_job",
            files={'resume_file': ('test_resume.txt', open('test_resume.txt', 'rb'), 'text/plain')},
            data={'job_description': job_description}
        )
        
        # Clean up test file
        if os.path.exists('test_resume.txt'):
            os.remove('test_resume.txt')
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resume-job matching: PASSED")
            print(f"   Match score: {result.get('match_score', 0)}%")
            print(f"   Matched skills: {result.get('matched_skills', [])}")
            print(f"   Missing skills: {result.get('missing_skills', [])}")
            return True
        else:
            print(f"❌ Resume-job matching: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Resume-job matching: ERROR - {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting Resume Screening API Integration Tests")
    print("=" * 50)
    
    tests = [
        test_health_endpoint,
        test_ml_status,
        test_job_skills_extraction,
        test_batch_analyze_resumes,
        test_match_resume_job
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests PASSED!")
        return True
    else:
        print("❌ Some tests FAILED. Check the logs above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
