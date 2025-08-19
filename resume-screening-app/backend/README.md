# Resume Screening Backend

## Getting Started

### Installation
1. Install Python 3.8+ and pip
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Backend
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. The server will be available at http://localhost:5000

### API Endpoints
- POST /api/upload-resume - Upload and analyze resume
- POST /api/extract-skills - Extract skills from job description
- POST /api/recommend-jobs - Get job recommendations
- GET /api/health - Health check

### Environment Variables
Create a `.env` file based on `.env.example` and configure as needed.
