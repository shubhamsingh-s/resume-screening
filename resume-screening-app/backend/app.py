from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from services.resume_service import ResumeService
from services.job_service import JobService
from services.gemini_service import GeminiService

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
resume_service = ResumeService()
job_service = JobService()
gemini_service = GeminiService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Root route - redirect to login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Remove login route

# Home route - dashboard
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# API Routes - Updated to match requirements
@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text first
            text = resume_service.extract_text(filepath)
            # Use Gemini AI for enhanced analysis
            ai_analysis = gemini_service.analyze_resume_with_ai(text)
            # Combine with basic analysis
            basic_analysis = resume_service.analyze_resume(filepath)
            
            # Merge results
            analysis = {
                'skills': list(set(basic_analysis.get('skills', []) + ai_analysis.get('skills', []))),
                'strengths': ai_analysis.get('strengths', []),
                'weaknesses': ai_analysis.get('weaknesses', []),
                'experience': basic_analysis.get('experience', ''),
                'education': basic_analysis.get('education', ''),
                'score': basic_analysis.get('score', 0),
                'experience_summary': ai_analysis.get('experience_summary', ''),
                'education_summary': ai_analysis.get('education_summary', ''),
                'overall_score': ai_analysis.get('overall_score', 0)
            }
            
            return jsonify(analysis)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/job_skills', methods=['POST'])
def job_skills():
    data = request.get_json()
    job_description = data.get('job_description', '')
    
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400
    
    try:
        # Use Gemini AI for enhanced skills extraction
        skills = gemini_service.extract_skills_with_ai(job_description)
        # Fallback to basic extraction if AI returns empty
        if not skills:
            skills = job_service.extract_skills(job_description)
        
        return jsonify({'skills': skills})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs():
    if 'file' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Analyze resume to get skills
            analysis = resume_service.analyze_resume(filepath)
            user_skills = analysis.get('skills', [])
            
            if not user_skills:
                return jsonify({'error': 'No skills found in resume'}), 400
            
            # Get job recommendations based on skills
            recommendations = job_service.recommend_jobs(user_skills)
            
            return jsonify({'recommendations': recommendations})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/match_resume_job', methods=['POST'])
def match_resume_job():
    """Match resume with job description and return skills comparison"""
    # Check if resume file is provided
    if 'resume_file' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    # Check if job description is provided
    job_description = request.form.get('job_description', '')
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400
    
    file = request.files['resume_file']
    if file.filename == '':
        return jsonify({'error': 'No resume file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract skills from resume
            resume_analysis = resume_service.analyze_resume(filepath)
            resume_skills = resume_analysis.get('skills', [])
            
            # Extract skills from job description
            job_skills = job_service.extract_skills(job_description)
            
            if not resume_skills:
                return jsonify({'error': 'No skills found in resume'}), 400
            
            if not job_skills:
                return jsonify({'error': 'No skills found in job description'}), 400
            
            # Calculate match score
            match_score = job_service.calculate_job_match(resume_skills, job_skills)
            
            # Find matched and missing skills
            resume_skills_set = set(skill.lower() for skill in resume_skills)
            job_skills_set = set(skill.lower() for skill in job_skills)
            
            matched_skills = list(resume_skills_set.intersection(job_skills_set))
            missing_skills = list(job_skills_set - resume_skills_set)
            
            return jsonify({
                'match_score': match_score,
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'resume_skills_count': len(resume_skills),
                'job_skills_count': len(job_skills)
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Resume Screening API is running'})

# ML Status endpoint
@app.route('/api/ml/status')
def ml_status():
    try:
        # Check if ML models are trained
        from services.ml_model_service import MLModelService
        ml_service = MLModelService()
        
        status = {
            'ml_trained': ml_service.trained,
            'unique_skills_count': len(ml_service.skills_vocabulary) if hasattr(ml_service, 'skills_vocabulary') else 0,
            'models_available': ['tfidf'] if ml_service.trained else []
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Favicon route to prevent 404
@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
