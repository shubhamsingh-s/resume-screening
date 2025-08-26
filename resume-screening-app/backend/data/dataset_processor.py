"""
Dataset Processor for Resume Screening System
Processes resumes from the legacy Automated-Resume-Screening-System
"""

import os
import glob
import PyPDF2
import docx
import re
from typing import List, Dict, Any
import json
from pathlib import Path

class DatasetProcessor:
    def __init__(self):
        self.resumes_path = "../../Automated-Resume-Screening-System/Original_Resumes/"
        self.output_path = "processed_resumes/"
        self.skills_keywords = self._load_skills_keywords()
        
    def _load_skills_keywords(self) -> List[str]:
        """Load skills keywords from the existing database"""
        # Import from the correct module path - handle both direct execution and module import
        try:
            from data.job_dataset import SKILLS_DATABASE
        except ImportError:
            # When running directly, use relative import
            from job_dataset import SKILLS_DATABASE
        return [skill.lower() for skill in SKILLS_DATABASE]
    
    def extract_text_from_pdf(self, filepath: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF {filepath}: {e}")
        return text
    
    def extract_text_from_docx(self, filepath: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(filepath)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {filepath}: {e}")
        return text
    
    def extract_text_from_doc(self, filepath: str) -> str:
        """Extract text from DOC file (fallback to simple text extraction)"""
        # For .doc files, we'll use a simple approach since python-docx doesn't support .doc well
        try:
            # Try to read as text file first
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
                if len(text.strip()) > 100:  # If we got reasonable text
                    return text
        except:
            pass
        
        # Fallback: return filename as content for now
        return f"Content from {os.path.basename(filepath)}"
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using keyword matching"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skills_keywords:
            # Use regex for whole word matching
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill.title())
        
        return list(set(found_skills))
    
    def process_resume(self, filepath: str) -> Dict[str, Any]:
        """Process a single resume file"""
        filename = os.path.basename(filepath)
        file_extension = os.path.splitext(filename)[1].lower()
        
        # Extract text based on file type
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(filepath)
        elif file_extension == '.docx':
            text = self.extract_text_from_docx(filepath)
        elif file_extension == '.doc':
            text = self.extract_text_from_doc(filepath)
        else:
            text = f"Unsupported file type: {file_extension}"
        
        # Extract skills
        skills = self.extract_skills(text)
        
        return {
            'filename': filename,
            'file_type': file_extension,
            'text': text[:1000] + '...' if len(text) > 1000 else text,  # Limit text length
            'skills': skills,
            'skills_count': len(skills),
            'original_path': filepath
        }
    
    def process_all_resumes(self) -> List[Dict[str, Any]]:
        """Process all resumes in the dataset"""
        processed_resumes = []
        
        # Ensure output directory exists
        os.makedirs(self.output_path, exist_ok=True)
        
        # Find all resume files
        resume_files = []
        resume_files.extend(glob.glob(os.path.join(self.resumes_path, "**/*.pdf"), recursive=True))
        resume_files.extend(glob.glob(os.path.join(self.resumes_path, "**/*.docx"), recursive=True))
        resume_files.extend(glob.glob(os.path.join(self.resumes_path, "**/*.doc"), recursive=True))
        
        print(f"Found {len(resume_files)} resume files to process")
        
        # Process each file
        for i, filepath in enumerate(resume_files):
            print(f"Processing {i+1}/{len(resume_files)}: {os.path.basename(filepath)}")
            try:
                resume_data = self.process_resume(filepath)
                processed_resumes.append(resume_data)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
        
        # Save processed data
        output_file = os.path.join(self.output_path, "processed_resumes.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_resumes, f, indent=2, ensure_ascii=False)
        
        print(f"Processed {len(processed_resumes)} resumes. Saved to {output_file}")
        return processed_resumes
    
    def create_training_dataset(self, processed_resumes: List[Dict[str, Any]]):
        """Create training dataset for ML models"""
        training_data = []
        
        for resume in processed_resumes:
            training_data.append({
                'text': resume['text'],
                'skills': resume['skills'],
                'label': 1  # Positive example for skills presence
            })
        
        # Save training data
        training_file = os.path.join(self.output_path, "training_data.json")
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        print(f"Created training dataset with {len(training_data)} examples. Saved to {training_file}")
        return training_data

def main():
    """Main function to process the dataset"""
    processor = DatasetProcessor()
    
    print("Starting dataset processing...")
    processed_resumes = processor.process_all_resumes()
    
    print("Creating training dataset...")
    training_data = processor.create_training_dataset(processed_resumes)
    
    print("Dataset processing completed successfully!")
    
    # Print summary
    total_skills = sum(len(resume['skills']) for resume in processed_resumes)
    avg_skills = total_skills / len(processed_resumes) if processed_resumes else 0
    
    print(f"\nSummary:")
    print(f"Total resumes processed: {len(processed_resumes)}")
    print(f"Total skills identified: {total_skills}")
    print(f"Average skills per resume: {avg_skills:.2f}")
    
    # Show sample of skills found
    all_skills = set()
    for resume in processed_resumes:
        all_skills.update(resume['skills'])
    
    print(f"Unique skills found: {len(all_skills)}")
    print("Sample skills:", sorted(list(all_skills))[:10])

if __name__ == "__main__":
    main()
