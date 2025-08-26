#!/usr/bin/env python3
"""
Performance test script for batch resume processing functionality
"""

import requests
import os

def create_test_resumes(num_resumes):
    """Create a specified number of test resume files"""
    for i in range(num_resumes):
        filename = f'test_resume_{i + 1}.docx'
        content = f"""
        Software Developer {i + 1}
        Skills: Python, JavaScript, React, Node.js, AWS
        Experience: {5 + (i % 5)} years
        Education: Bachelor's in Computer Science
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

def test_large_batch_resume_processing(num_resumes):
    """Test the batch resume processing endpoint with a large number of resumes"""
    print("🧪 Testing Large Batch Resume Processing")
    print("=" * 50)
    
    create_test_resumes(num_resumes)
    
    files = []
    for i in range(num_resumes):
        filename = f'test_resume_{i + 1}.docx'
        files.append(('files', (filename, open(filename, 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')))
    
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
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    finally:
        # Clean up test files
        for i in range(num_resumes):
            filename = f'test_resume_{i + 1}.docx'
            if os.path.exists(filename):
                os.remove(filename)
        print("\n🧹 Cleaned up test files")

if __name__ == "__main__":
    test_large_batch_resume_processing(50)
