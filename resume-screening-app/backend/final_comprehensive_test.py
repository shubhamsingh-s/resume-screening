#!/usr/bin/env python3
"""
Final comprehensive test for the complete Resume Screening System
Tests all endpoints including the new batch processing feature
"""

import requests
import json
import time

class FinalComprehensiveTest:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        
    def run_test(self, name, test_func):
        """Run a test and record results"""
        print(f"\n🧪 Testing: {name}")
        print("=" * 60)
        
        start_time = time.time()
        try:
            result = test_func()
            end_time = time.time()
            duration = end_time - start_time
            
            self.test_results.append({
                'name': name,
                'status': '✅ PASSED',
                'duration': f"{duration:.2f}s",
                'details': result
            })
            print(f"✅ PASSED - {duration:.2f}s")
            return True
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            self.test_results.append({
                'name': name,
                'status': '❌ FAILED',
                'duration': f"{duration:.2f}s",
                'error': str(e)
            })
            print(f"❌ FAILED - {e}")
            return False
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.base_url}/api/health")
        response.raise_for_status()
        data = response.json()
        assert data['status'] == 'healthy'
        return data
    
    def test_ml_status(self):
        """Test ML model status"""
        response = requests.get(f"{self.base_url}/api/ml/status")
        response.raise_for_status()
        data = response.json()
        assert 'ml_trained' in data
        return data
    
    def test_single_resume_matching(self):
        """Test single resume-job matching"""
        resume_text = "Python Developer with React and AWS experience"
        job_description = "Looking for Python developer with React and cloud experience"
        
        # Create test file
        with open('test_single.txt', 'w') as f:
            f.write(resume_text)
        
        with open('test_single.txt', 'rb') as f:
            response = requests.post(
                f"{self.base_url}/match_resume_job",
                files={'resume_file': ('test_single.txt', f, 'text/plain')},
                data={'job_description': job_description}
            )
        
        response.raise_for_status()
        data = response.json()
        assert 'match_score' in data
        assert 'matched_skills' in data
        return data
    
    def test_batch_resume_processing(self):
        """Test batch resume processing"""
        # Create multiple test resumes
        resumes = [
            "Software Developer with Python and JavaScript",
            "Data Scientist with Machine Learning and SQL",
            "DevOps Engineer with AWS and Docker"
        ]
        
        files = []
        for i, resume in enumerate(resumes):
            filename = f'test_batch_{i}.txt'
            with open(filename, 'w') as f:
                f.write(resume)
            files.append(('files', (filename, open(filename, 'rb'), 'text/plain')))
        
        try:
            response = requests.post(
                f"{self.base_url}/batch_analyze_resumes",
                files=files
            )
            
            response.raise_for_status()
            data = response.json()
            assert 'total_resumes' in data
            assert 'results' in data
            assert len(data['results']) == len(resumes)
            return data
            
        finally:
            # Clean up
            for i in range(len(resumes)):
                import os
                if os.path.exists(f'test_batch_{i}.txt'):
                    os.remove(f'test_batch_{i}.txt')
    
    def test_job_skills_extraction(self):
        """Test job skills extraction"""
        job_description = "Python developer needed with Django, React, and AWS experience"
        response = requests.post(
            f"{self.base_url}/job_skills",
            json={'job_description': job_description}
        )
        response.raise_for_status()
        data = response.json()
        assert 'skills' in data
        return data
    
    def test_error_handling(self):
        """Test error scenarios"""
        # Test invalid file type
        with open('test_invalid.exe', 'wb') as f:
            f.write(b'\x00' * 100)
        
        with open('test_invalid.exe', 'rb') as f:
            response = requests.post(
                f"{self.base_url}/match_resume_job",
                files={'resume_file': ('test_invalid.exe', f, 'application/octet-stream')},
                data={'job_description': 'test job'}
            )
        
        assert response.status_code == 400, "Should reject invalid file types"
        
        # Test empty batch request
        response = requests.post(f"{self.base_url}/batch_analyze_resumes")
        assert response.status_code == 400, "Should reject empty batch requests"
        
        return "All error handling tests passed"
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 FINAL COMPREHENSIVE TESTING - Resume Screening System")
        print("=" * 80)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("ML Status", self.test_ml_status),
            ("Single Resume Matching", self.test_single_resume_matching),
            ("Batch Resume Processing", self.test_batch_resume_processing),
            ("Job Skills Extraction", self.test_job_skills_extraction),
            ("Error Handling", self.test_error_handling)
        ]
        
        passed = 0
        total = len(tests)
        
        for name, test_func in tests:
            if self.run_test(name, test_func):
                passed += 1
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 FINAL TEST SUMMARY")
        print("=" * 80)
        
        for result in self.test_results:
            print(f"{result['status']} - {result['name']} ({result['duration']})")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is production-ready.")
            print("\n✨ FEATURES VERIFIED:")
            print("   ✅ Single resume-job matching")
            print("   ✅ Batch resume processing (multiple files)")
            print("   ✅ ML model integration")
            print("   ✅ Error handling")
            print("   ✅ Health monitoring")
            print("   ✅ Skills extraction")
        else:
            print("⚠️  Some tests failed. Review the errors above.")
        
        return passed == total

if __name__ == "__main__":
    tester = FinalComprehensiveTest()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)
