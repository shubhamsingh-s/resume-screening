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

def test_job_skills():
    url = "http://localhost:5000/job_skills"
    data = {'job_description': 'Looking for a Python developer with experience in Flask and Django.'}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Job Skills Test Passed")
        print("Response:", response.json())
    else:
        print("Job Skills Test Failed")
        print("Status Code:", response.status_code)
        print("Response:", response.json())

def test_recommend_jobs():
    url = "http://localhost:5000/recommend_jobs"
    files = {'file': open('test_resume_0.txt', 'rb')}  # Replace with a valid resume file path

    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        print("Recommend Jobs Test Passed")
        print("Response:", response.json())
    else:
        print("Recommend Jobs Test Failed")
        print("Status Code:", response.status_code)
        print("Response:", response.json())

def test_match_resume_job():
    url = "http://localhost:5000/match_resume_job"
    files = {'resume_file': open('test_resume_0.txt', 'rb')}  # Replace with a valid resume file path
    data = {'job_description': 'Looking for a Python developer with experience in Flask and Django.'}
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        print("Match Resume Job Test Passed")
        print("Response:", response.json())
    else:
        print("Match Resume Job Test Failed")
        print("Status Code:", response.status_code)
        print("Response:", response.json())

def test_batch_analyze_resumes():
    url = "http://localhost:5000/batch_analyze_resumes"
    files = [
        ('files', open('test_resume_0.txt', 'rb')),  # Replace with valid resume file paths
        ('files', open('test_resume_1.txt', 'rb'))
    ]
    
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        print("Batch Analyze Resumes Test Passed")
        print("Response:", response.json())
    else:
        print("Batch Analyze Resumes Test Failed")
        print("Status Code:", response.status_code)
        print("Response:", response.json())

if __name__ == "__main__":
    test_analyze_resume()
    test_job_skills()
    test_recommend_jobs()
    test_match_resume_job()
    test_batch_analyze_resumes()
