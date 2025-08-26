import axios from 'axios';

async function testAPI() {
    try {
        // Test health endpoint
        const healthResponse = await axios.get('http://localhost:5000/api/health');
        console.log("Health Check:", healthResponse.data);

        // Test ML status endpoint
        const mlStatusResponse = await axios.get('http://localhost:5000/api/ml/status');
        console.log("ML Status:", mlStatusResponse.data);

        // Test job skills endpoint (no file upload needed)
        const jobSkillsResponse = await axios.post('http://localhost:5000/job_skills', {
            job_description: 'Looking for a Python developer with experience in Flask and Django.'
        });
        console.log("Job Skills:", jobSkillsResponse.data);

        console.log("All API endpoints are working correctly!");
        
    } catch (error) {
        console.error("Error during API test:", error.response ? error.response.data : error.message);
    }
}

testAPI();
