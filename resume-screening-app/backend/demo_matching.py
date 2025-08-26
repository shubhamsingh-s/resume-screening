#!/usr/bin/env python3
"""
Demo script to showcase the resume-job matching functionality
"""

import json
from services.resume_service import ResumeService
from services.job_service import JobService

def demonstrate_matching():
    """Demonstrate the matching functionality with sample data"""
    
    print("🎯 Resume-Job Matching Demonstration")
    print("=" * 50)
    
    # Initialize services
    resume_service = ResumeService()
    job_service = JobService()
    
    # Sample resume text
    resume_text = """
    Software Developer with 5+ years of experience
    Skills: Python, React, JavaScript, AWS, SQL, Machine Learning
    Experience: Built scalable web applications using React and Python
    Education: Bachelor's in Computer Science
    Certifications: AWS Certified Developer
    """
    
    # Sample job description
    job_description = """
    Senior Software Developer Position
    Required Skills: Python, React, JavaScript, AWS, Docker, Kubernetes
    Nice to have: Machine Learning, Cloud Architecture
    Experience: 3+ years in software development
    Responsibilities: Build and maintain web applications, implement CI/CD pipelines
    """
    
    print("📄 Sample Resume:")
    print(resume_text.strip())
    print("\n💼 Sample Job Description:")
    print(job_description.strip())
    print("\n" + "=" * 50)
    
    # Analyze resume
    print("\n🔍 Analyzing Resume...")
    resume_analysis = resume_service.analyze_resume_text(resume_text)
    resume_skills = resume_analysis['skills']
    print(f"✅ Extracted {len(resume_skills)} skills from resume:")
    for skill in resume_skills:
        print(f"   - {skill}")
    
    # Extract job skills
    print("\n🔍 Extracting Job Requirements...")
    job_skills = job_service.extract_skills(job_description)
    print(f"✅ Extracted {len(job_skills)} skills from job description:")
    for skill in job_skills:
        print(f"   - {skill}")
    
    # Calculate match
    print("\n🤝 Calculating Match...")
    match_score = job_service.calculate_job_match(resume_skills, job_skills)
    
    # Find matched and missing skills
    resume_skills_set = set(skill.lower() for skill in resume_skills)
    job_skills_set = set(skill.lower() for skill in job_skills)
    
    matched_skills = list(resume_skills_set.intersection(job_skills_set))
    missing_skills = list(job_skills_set - resume_skills_set)
    
    print(f"\n🎯 Match Results:")
    print(f"   Match Score: {match_score}%")
    print(f"   Resume Skills: {len(resume_skills)}")
    print(f"   Job Requirements: {len(job_skills)}")
    
    print(f"\n✅ Matched Skills ({len(matched_skills)}):")
    for skill in matched_skills:
        print(f"   ✓ {skill.title()}")
    
    print(f"\n❌ Missing Skills ({len(missing_skills)}):")
    for skill in missing_skills:
        print(f"   ✗ {skill.title()}")
    
    print("\n" + "=" * 50)
    print("💡 Interpretation:")
    if match_score >= 70:
        print("   🎉 Excellent match! Strong candidate for the position.")
    elif match_score >= 50:
        print("   👍 Good match. Candidate has most required skills.")
    elif match_score >= 30:
        print("   🤔 Moderate match. Some key skills are missing.")
    else:
        print("   ⚠️  Weak match. Significant skill gaps.")
    
    print("\n" + "=" * 50)
    print("🚀 Ready for production use!")

if __name__ == "__main__":
    demonstrate_matching()
