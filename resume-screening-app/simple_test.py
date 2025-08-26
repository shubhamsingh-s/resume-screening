import requests

# Test health endpoint
try:
    response = requests.get("http://localhost:5000/api/health")
    print(f"Health endpoint status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error testing health endpoint: {e}")

# Test ML status endpoint
try:
    response = requests.get("http://localhost:5000/api/ml/status")
    print(f"ML status endpoint status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error testing ML status endpoint: {e}")
