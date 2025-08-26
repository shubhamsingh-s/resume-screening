# Quick Start Guide - Resume Screening App

## 🚀 Get Started in 3 Steps

### 1. Start the Backend Server
```bash
cd resume-screening-app/backend
python app.py
```
The server will start on `http://localhost:5000`

### 2. Start the Frontend (Optional - if you want web interface)
```bash
cd resume-screening-app/frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`

### 3. Test the Matching System

#### Option A: Use Web Interface
1. Open `http://localhost:5173` in your browser
2. Navigate to "Resume & Job Matching"
3. Upload a resume file (PDF or DOCX)
4. Paste a job description
5. Click "Match Resume with Job"
6. View the match results with scores and skills analysis

#### Option B: Use API Directly
```bash
# Test with curl
curl -X POST http://localhost:5000/match_resume_job \
  -F "resume_file=@path/to/your/resume.pdf" \
  -F "job_description=Your job description text here"
```

#### Option C: Run Demo Script
```bash
cd resume-screening-app/backend
python demo_matching.py
```

## 📋 What You'll See

When you run the matching, you'll get:
- ✅ **Match Score Percentage** (0-100%)
- ✅ **Matched Skills** (skills present in both resume and job)
- ✅ **Missing Skills** (skills required but not in resume)
- ✅ **Skills Count** comparison

## 🎯 Example Results

A typical match result looks like:
```
Match Score: 75%
Matched Skills: Python, React, JavaScript, AWS
Missing Skills: Docker, Kubernetes
Resume Skills: 6 | Job Requirements: 6
```

## 🔧 Troubleshooting

### Common Issues:
1. **ML Model Not Training**: Check if training data exists in `backend/processed_resumes/`
2. **File Upload Issues**: Ensure files are PDF or DOCX format
3. **Server Not Starting**: Check if port 5000 is available

### Quick Fixes:
- Restart the backend server if changes were made
- Check console for error messages
- Verify all dependencies are installed (`pip install -r requirements.txt`)

## 📞 Support

The system includes:
- ✅ Trained ML model with 56 unique skills
- ✅ Working API endpoints
- ✅ Functional frontend interface
- ✅ Sample test scripts

Your resume screening system is now ready to use! 🎉
