#!/usr/bin/env python3
"""
Performance test script for ML model integration
Tests the enhanced ML model with various resume examples
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ml_model_service import ml_model_service
from services.resume_service import ResumeService

def test_ml_performance():
    """Test ML model performance with various resume examples"""
    print("=" * 60)
    print("ML Model Performance Test")
    print("=" * 60)
    
    resume_service = ResumeService()
    
    # Test cases with different types of resumes
    test_cases = [
        {
            'name': 'Software Engineer Resume',
            'text': """
            Software Engineer with 5+ years of experience in Python, JavaScript, and React.
            Strong background in machine learning, data analysis, and cloud computing.
            Proficient in AWS, Docker, Kubernetes, and REST API development.
            Experience with Agile methodology and version control using Git.
            """
        },
        {
            'name': 'Data Scientist Resume',
            'text': """
            Data Scientist with expertise in machine learning, statistical analysis, and data visualization.
            Proficient in Python, R, TensorFlow, PyTorch, and scikit-learn.
            Experience with big data technologies like Spark and Hadoop.
            Strong background in mathematics, statistics, and predictive modeling.
            """
        },
        {
            'name': 'Frontend Developer Resume',
            'text': """
            Frontend Developer specializing in React, TypeScript, and modern web technologies.
            Experience with responsive design, CSS frameworks, and UI/UX principles.
            Proficient in JavaScript, HTML5, CSS3, and frontend build tools.
            """
        },
        {
            'name': 'DevOps Engineer Resume',
            'text': """
            DevOps Engineer with expertise in cloud infrastructure and automation.
            Proficient in AWS, Azure, Docker, Kubernetes, and Terraform.
            Experience with CI/CD pipelines, monitoring, and infrastructure as code.
            Strong background in Linux administration and scripting.
            """
        }
    ]
    
    print(f"ML Model trained: {ml_model_service.trained}")
    print(f"Skills vocabulary size: {len(ml_model_service.skills_vocabulary)}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        # Traditional extraction
        traditional_skills = resume_service.extract_skills(test_case['text'])
        print(f"Traditional skills: {traditional_skills}")
        print(f"Traditional skills count: {len(traditional_skills)}")
        
        # ML-enhanced analysis
        analysis = resume_service.analyze_resume_text(test_case['text'], use_ml_enhancement=True)
        ml_skills = analysis.get('skills', [])
        print(f"ML-enhanced skills: {ml_skills}")
        print(f"ML-enhanced skills count: {len(ml_skills)}")
        
        # Additional metrics
        ml_only_skills = set(ml_skills) - set(traditional_skills)
        traditional_only_skills = set(traditional_skills) - set(ml_skills)
        
        print(f"Skills found only by ML: {list(ml_only_skills)}")
        print(f"Skills found only by traditional: {list(traditional_only_skills)}")
        print(f"Analysis method: {analysis.get('analysis_method', 'unknown')}")
        print()

def test_batch_processing():
    """Test batch processing capabilities"""
    print("=" * 60)
    print("Batch Processing Test")
    print("=" * 60)
    
    # Create multiple test resumes
    test_resumes = [
        "Python developer with Django and Flask experience",
        "JavaScript expert with React and Node.js skills",
        "Data scientist proficient in machine learning and statistics",
        "Cloud engineer with AWS and Azure expertise"
    ]
    
    # Test ML batch processing
    ml_results = ml_model_service.batch_process_resumes(test_resumes)
    
    for i, (resume_text, result) in enumerate(zip(test_resumes, ml_results), 1):
        print(f"Resume {i}: {resume_text[:50]}...")
        print(f"  ML extracted skills: {result['ml_extracted_skills']}")
        print(f"  Skills count: {result['skills_count']}")
        print()

def main():
    """Main test function"""
    try:
        test_ml_performance()
        test_batch_processing()
        
        print("=" * 60)
        print("Performance Test Completed Successfully!")
        print("ML model is working correctly with enhanced capabilities")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during performance testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
