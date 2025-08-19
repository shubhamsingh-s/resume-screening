# Resume Screening Application

A modern AI-powered resume screening application with React frontend and Flask backend.

## Features
- **Frontend**: React + TypeScript + TailwindCSS + shadcn/ui + lucide-react
- **Backend**: Flask + Python + AI endpoints
- **Features**: Resume upload/analysis, job description skills extraction, job matching
- **UI**: Glassmorphism login page, 3-card dashboard
- **Routes**: /login, /analyze_resume, /job_skills, /recommend_jobs

## Project Structure
```
resume-screening-app/
├── frontend/          # React application
├── backend/           # Flask API
├── backend/services/  # Backend services
├── backend/requirements.txt
├── backend/app.py
├── backend/.env.example
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip
- npm

### Installation

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### API Endpoints
- POST /api/upload-resume - Upload and analyze resume
- POST /api/extract-skills - Extract skills from job description
- POST /api/recommend-jobs - Get job recommendations
- GET /api/health - Health check

### Features
- Resume upload and analysis with AI-powered insights
- Job description skills extraction
- Personalized job recommendations
- Glassmorphism UI design
- Responsive 3-card dashboard layout

### Tech Stack
- **Frontend**: React + TypeScript + TailwindCSS + shadcn/ui + lucide-react
- **Backend**: Flask + Python + AI endpoints
- **Features**: Resume upload/analysis, job description skills extraction, job matching
- **UI**: Glassmorphism login page, 3-card dashboard
- **Routes**: /login, /analyze_resume, /job_skills, /recommend_jobs

### Getting Started
1. Install dependencies:
   ```bash
   # Frontend
   cd frontend && npm install
   
   # Backend
   cd backend && pip install -r requirements.txt
   ```
2. Start the backend:
   ```bash
   cd backend && python app.py
   ```
3. Start the frontend:
   ```bash
   cd frontend && npm run dev
   ```
4. Access the application at http://localhost:3000

### Environment Variables
Create a `.env` file based on `.env.example` and configure as needed.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### License
MIT License
