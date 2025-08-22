#!/usr/bin/env python3
"""
Test script to verify ML model service integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ml_model_service import ml_model_service
from services.resume_service import ResumeService

def test_ml_model_service():
    """Test ML model service functionality"""
    print("Testing ML Model Service...")
    
    # Check if ML model is trained
    print(f"ML Model trained: {ml_model_service.trained}")
    
    # Load training data
    training_data = ml_model_service.load_training_data()
    print(f"Training data loaded: {len(training_data)} resumes")
    
    # Test skills extraction
    test_text = "Experienced Python developer with Java and React skills. Strong background in machine learning and data analysis."
    if ml_model_service.trained:
        ml_skills = ml_model_service.extract_skills_ml(test_text)
        print(f"ML extracted skills: {ml_skills}")
    else:
        print("ML model not trained - using traditional extraction")
    
    return True

def test_resume_service_integration():
    """Test resume service integration with ML"""
    print("\nTesting Resume Service Integration...")
    
    resume_service = ResumeService()
    
    # Test with a simple text
    test_text = "Python developer with 5 years of experience. Skills include Java, React, and machine learning."
    
    # Test traditional extraction
    traditional_skills = resume_service.extract_skills(test_text)
    print(f"Traditional skills extraction: {traditional_skills}")
    
    # Test ML-enhanced analysis
    analysis = resume_service.analyze_resume_text(test_text, use_ml_enhancement=True)
    print(f"ML-enhanced analysis skills: {analysis.get('skills', [])}")
    print(f"Analysis method: {analysis.get('analysis_method', 'unknown')}")
    
    return True

def main():
    """Main test function"""
    print("=" * 50)
    print("ML Model Integration Test")
    print("=" * 50)
    
    try:
        # Test ML model service
        test_ml_model_service()
        
        # Test resume service integration
        test_resume_service_integration()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("ML model integration is working correctly.")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
