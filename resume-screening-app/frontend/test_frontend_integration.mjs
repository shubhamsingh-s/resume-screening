import axios from 'axios';
import fs from 'fs';

async function testFrontendIntegration() {
    const resumeFilePath = 'test_resume_0.txt'; // Replace with a valid resume file path
    const jobDescription = 'Looking for a Python developer with experience in Flask and Django.';

    try {
        // Test analyze resume
        const analyzeResponse = await axios.post('http://localhost:5000/analyze_resume', {
            file: fs.createReadStream(resumeFilePath)
        });
        console.log("Analyze Resume Response:", analyzeResponse.data);

        // Test job skills
        const jobSkillsResponse = await axios.post('http://localhost:5000/job_skills', {
            job_description: jobDescription
        });
        console.log("Job Skills Response:", jobSkillsResponse.data);

        // Test recommend jobs
        const recommendJobsResponse = await axios.post('http://localhost:5000/recommend_jobs', {
            file: fs.createReadStream(resumeFilePath)
        });
        console.log("Recommend Jobs Response:", recommendJobsResponse.data);

        // Test match resume job
        const matchResponse = await axios.post('http://localhost:5000/match_resume_job', {
            resume_file: fs.createReadStream(resumeFilePath),
            job_description: jobDescription
        });
        console.log("Match Resume Job Response:", matchResponse.data);

    } catch (error) {
        console.error("Error during frontend integration test:", error.response ? error.response.data : error.message);
    }
}

testFrontendIntegration();
