import requests

def test_analyze_resume():
    url = "http://localhost:5000/analyze_resume"
    files = {'file': open('test_resume_0.txt', 'rb')}  # Replace with a valid resume file path

    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        print("Analyze Resume Test Passed")
        print("Response:", response.json())
    else:
        print("Analyze Resume Test Failed")
        print("Status Code:", response.status_code)
        print("Response:", response.json())

if __name__ == "__main__":
    test_analyze_resume()
