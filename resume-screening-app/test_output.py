import requests
import sys

def test_endpoint(url, method='GET', data=None, headers=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test endpoints
test_endpoint("http://localhost:5000/api/health")
test_endpoint("http://localhost:5000/api/ml/status")
test_endpoint("http://localhost:5000/job_skills", 'POST', 
              {"job_description": "Looking for Python developer with Django experience"})
