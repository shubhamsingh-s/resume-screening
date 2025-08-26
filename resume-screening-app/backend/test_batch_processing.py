#!/usr/bin/env python3
"""
Test script for batch resume processing functionality
"""

import requests
import os

def test_batch_resume_processing():
    """Test the batch resume processing endpoint"""
    print("🧪 Testing Batch Resume Processing")
    print("=" * 50)
    
    # Create test resume files
    test_resumes = [
        {
            'filename': 'test_resume1.txt',
            'content': """
            Software Developer
            Skills: Python, JavaScript, React, Node.js, AWS
            Experience: 5 years
            Education: Bachelor's in Computer Science
            """
        },
        {
            'filename': 'test_resume2.txt',
            'content': """
            Data Scientist
            Skills: Python, Machine Learning, SQL, TensorFlow, Data Analysis
            Experience: 3 years
            Education: Master's in Data Science
            """
        },
        {
            'filename': 'test_resume3.txt',
            'content': """
            DevOps Engineer
            Skills: AWS, Docker, Kubernetes, CI/CD, Linux, Python
            Experience: 4 years
            Education: Bachelor's in IT
            """
        }
    ]
    
    # Create the test files
    files = []
    for resume in test_resumes:
        with open(resume['filename'], 'w', encoding='utf-8') as f:
            f.write(resume['content'])
        files.append(('files', (resume['filename'], open(resume['filename'], 'rb'), 'text/plain')))
    
    try:
        # Test the batch endpoint
        response = requests.post(
            'http://localhost:5000/batch_analyze_resumes',
            files=files
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Batch processing successful!")
            print(f"Total resumes processed: {result['total_resumes']}")
            print(f"Status: {result['status']}")
            
            print("\n📊 Individual Results:")
            for i, resume_result in enumerate(result['results']):
                print(f"\nResume {i + 1}:")
                if 'error' in resume_result:
                    print(f"   ❌ Error: {resume_result['error']}")
                else:
                    print(f"   ✅ Skills: {len(resume_result['skills'])}")
                    print(f"   📊 Score: {resume_result['score']}")
                    print(f"   🎓 Education: {resume_result['education']}")
                    print(f"   💼 Experience: {resume_result['experience']}")
                    print(f"   📝 Method: {resume_result['analysis_method']}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    finally:
        # Clean up test files
        for resume in test_resumes:
            if os.path.exists(resume['filename']):
                os.remove(resume['filename'])
        print("\n🧹 Cleaned up test files")

if __name__ == "__main__":
    test_batch_resume_processing()
