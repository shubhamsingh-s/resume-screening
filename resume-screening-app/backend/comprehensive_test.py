#!/usr/bin/env python3
"""
Comprehensive test script for Resume Screening App
Tests all API endpoints, error handling, and performance
"""

import requests
import json
import time
import os

class ComprehensiveTester:
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
    
    def test_ml_status(self):
        """Test ML model status endpoint"""
        response = requests.get(f"{self.base_url}/api/ml/status")
        response.raise_for_status()
        data = response.json()
        
        assert data['ml_trained'] == True, "ML model should be trained"
        assert data['unique_skills_count'] > 0, "Should have skills vocabulary"
        
        return data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.base_url}/api/health")
        response.raise_for_status()
        data = response.json()
        
        assert data['status'] == 'healthy', "API should be healthy"
        return data
    
    def test_job_skills_extraction(self):
        """Test job skills extraction endpoint"""
        job_description = """
        Senior Python Developer with React experience.
        Required: Python, Django, React, JavaScript, AWS, Docker.
        Nice to have: Machine Learning, Kubernetes, CI/CD.
        """
        
        response = requests.post(
            f"{self.base_url}/job_skills",
            json={'job_description': job_description}
        )
        response.raise_for_status()
        data = response.json()
        
        assert 'skills' in data, "Should return skills list"
        assert len(data['skills']) > 0, "Should extract some skills"
        
        return data
    
    def test_resume_analysis(self):
        """Test resume analysis endpoint"""
        # Create a test resume file
        resume_text = """
        Software Developer - 5 years experience
        Skills: Python, JavaScript, React, Node.js, AWS, SQL
        Experience: Built web applications, implemented APIs
        Education: Bachelor's in Computer Science
        """
        
        with open('test_resume.txt', 'w', encoding='utf-8') as f:
            f.write(resume_text)
        
        try:
            with open('test_resume.txt', 'rb') as f:
                response = requests.post(
                    f"{self.base_url}/analyze_resume",
                    files={'file': ('test_resume.txt', f, 'text/plain')}
                )
            
            response.raise_for_status()
            data = response.json()
            
            assert 'skills' in data, "Should return skills list"
            assert 'score' in data, "Should return match score"
            
            return data
            
        finally:
            if os.path.exists('test_resume.txt'):
                os.remove('test_resume.txt')
    
    def test_resume_job_matching(self):
        """Test main resume-job matching endpoint"""
        # Create test files
        resume_text = """
        Full Stack Developer
        Skills: Python, React, JavaScript, Node.js, MongoDB, AWS
        Experience: 4 years building web applications
        """
        
        job_description = """
        Looking for Full Stack Developer with:
        - Python and JavaScript experience
        - React framework knowledge
        - AWS cloud services
        - Database skills (MongoDB or SQL)
        """
        
        with open('test_resume_match.txt', 'w', encoding='utf-8') as f:
            f.write(resume_text)
        
        try:
            with open('test_resume_match.txt', 'rb') as f:
                response = requests.post(
                    f"{self.base_url}/match_resume_job",
                    files={'resume_file': ('test_resume_match.txt', f, 'text/plain')},
                    data={'job_description': job_description}
                )
            
            response.raise_for_status()
            data = response.json()
            
            assert 'match_score' in data, "Should return match score"
            assert 'matched_skills' in data, "Should return matched skills"
            assert 'missing_skills' in data, "Should return missing skills"
            
            return data
            
        finally:
            if os.path.exists('test_resume_match.txt'):
                os.remove('test_resume_match.txt')
    
    def test_error_handling(self):
        """Test error scenarios"""
        # Test invalid file type
        with open('test_invalid.exe', 'wb') as f:
            f.write(b'\x00' * 100)  # Create a dummy binary file
        
        try:
            with open('test_invalid.exe', 'rb') as f:
                response = requests.post(
                    f"{self.base_url}/match_resume_job",
                    files={'resume_file': ('test_invalid.exe', f, 'application/octet-stream')},
                    data={'job_description': 'test job description'}
                )
            
            # Should return 400 error
            assert response.status_code == 400, "Should reject invalid file types"
            
        finally:
            if os.path.exists('test_invalid.exe'):
                os.remove('test_invalid.exe')
        
        # Test empty job description
        response = requests.post(
            f"{self.base_url}/job_skills",
            json={'job_description': ''}
        )
        assert response.status_code == 400, "Should reject empty job description"
        
        return "All error handling tests passed"
    
    def test_performance(self):
        """Test performance with multiple requests"""
        test_cases = [
            {
                'resume': "Python Developer with Django experience",
                'job': "Python Developer needed with Django framework"
            },
            {
                'resume': "React Frontend Developer with JavaScript",
                'job': "Frontend Developer with React and JavaScript"
            },
            {
                'resume': "DevOps Engineer AWS Docker Kubernetes",
                'job': "DevOps position with cloud and container experience"
            }
        ]
        
        times = []
        for i, test_case in enumerate(test_cases):
            start_time = time.time()
            
            # Create temporary file
            with open(f'test_perf_{i}.txt', 'w') as f:
                f.write(test_case['resume'])
            
            try:
                with open(f'test_perf_{i}.txt', 'rb') as f:
                    response = requests.post(
                        f"{self.base_url}/match_resume_job",
                        files={'resume_file': (f'test_perf_{i}.txt', f, 'text/plain')},
                        data={'job_description': test_case['job']}
                    )
                response.raise_for_status()
                
            finally:
                if os.path.exists(f'test_perf_{i}.txt'):
                    os.remove(f'test_perf_{i}.txt')
            
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        return f"Average response time: {avg_time:.2f}s ({len(times)} requests)"
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Comprehensive Testing")
        print("=" * 60)
        
        tests = [
            ("ML Status Check", self.test_ml_status),
            ("Health Check", self.test_health_check),
            ("Job Skills Extraction", self.test_job_skills_extraction),
            ("Resume Analysis", self.test_resume_analysis),
            ("Resume-Job Matching", self.test_resume_job_matching),
            ("Error Handling", self.test_error_handling),
            ("Performance Testing", self.test_performance)
        ]
        
        passed = 0
        total = len(tests)
        
        for name, test_func in tests:
            if self.run_test(name, test_func):
                passed += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        for result in self.test_results:
            print(f"{result['status']} - {result['name']} ({result['duration']})")
        
        print(f"\n📈 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is ready for production.")
        else:
            print("⚠️  Some tests failed. Review the errors above.")
        
        return passed == total

if __name__ == "__main__":
    tester = ComprehensiveTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)
