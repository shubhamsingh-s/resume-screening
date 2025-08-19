from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from services.resume_service import ResumeService
from services.job_service import JobService

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Root route - redirect to login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (replace with proper auth in production)
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

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

# API Routes
@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
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
            analysis = resume_service.analyze_resume(filepath)
            return jsonify(analysis)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/extract-skills', methods=['POST'])
def extract_skills():
    data = request.get_json()
    job_description = data.get('job_description', '')
    
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400
    
    try:
        skills = job_service.extract_skills(job_description)
        return jsonify({'skills': skills})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend-jobs', methods=['POST'])
def recommend_jobs():
    data = request.get_json()
    user_skills = data.get('skills', [])
    
    if not user_skills:
        return jsonify({'error': 'No skills provided'}), 400
    
    try:
        recommendations = job_service.recommend_jobs(user_skills)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Resume Screening API is running'})

# Favicon route to prevent 404
@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
