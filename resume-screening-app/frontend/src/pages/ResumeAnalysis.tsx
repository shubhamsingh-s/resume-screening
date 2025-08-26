 import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface MatchResult {
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  resume_skills_count: number;
  job_skills_count: number;
}

const ResumeAnalysis: React.FC = () => {
  useAuth();
  const [activeTab, setActiveTab] = useState<'resume' | 'job'>('resume');
  const [resumeFiles, setResumeFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [matchResult, setMatchResult] = useState<MatchResult | null>(null);
  const [error, setError] = useState<string>('');

    const handleResumeUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        console.log("File upload event triggered");
        console.log("Uploaded files:", event.target.files);
        if (event.target.files) {
            const filesArray = Array.from(event.target.files);
            console.log("Files array:", filesArray);
            const validFiles = filesArray.filter(file => 
                file.type === 'application/pdf' || 
                file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            );
            console.log("Valid files:", validFiles);

            if (validFiles.length > 0) {
                setResumeFiles(validFiles);
                setError('');
            } else {
                setError('Please upload PDF or DOCX files');
            }
        }
    };

  const handleJobDescriptionChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setJobDescription(event.target.value);
    setError('');
  };

    const handleMatchResumeJob = async () => {
        console.log("Resume Files:", resumeFiles);
        console.log("Job Description:", jobDescription);
    if (resumeFiles.length === 0) {
      setError('Please upload at least one resume file');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Please provide a job description');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    resumeFiles.forEach(file => {
      formData.append('resume_files', file);
    });
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://localhost:5000/batch_analyze_resumes', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to match resumes with job');
      }

      const result: MatchResult = await response.json();
      setMatchResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 70) return 'bg-green-100';
    if (score >= 40) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Resume & Job Matching</h1>
      
      {/* Main Card Container */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 mb-6">
          <button
            className={`px-6 py-3 font-medium text-sm ${
              activeTab === 'resume'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('resume')}
          >
            Upload Resume
          </button>
          <button
            className={`px-6 py-3 font-medium text-sm ${
              activeTab === 'job'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('job')}
          >
            Job Description
          </button>
        </div>

        {/* Tab Content */}
        <div className="mb-6">
          {activeTab === 'resume' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Upload your resumes (PDF or DOCX)
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleResumeUpload}
                  className="hidden"
                  id="resume-upload"
                  multiple
                />
                <label
                  htmlFor="resume-upload"
                  className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Choose File
                </label>
                {resumeFiles.length > 0 && (
                  <p className="mt-3 text-sm text-gray-600">
                    Selected: {resumeFiles.map(file => file.name).join(', ')}
                  </p>
                )}
                <p className="mt-2 text-xs text-gray-500">
                  Supported formats: PDF, DOCX
                </p>
              </div>
            </div>
          )}

          {activeTab === 'job' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Paste Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={handleJobDescriptionChange}
                placeholder="Paste the job description here..."
                rows={8}
                className="w-full border border-gray-300 rounded-md p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              />
              <p className="text-xs text-gray-500 mt-2">
                {jobDescription.length} characters
              </p>
            </div>
          )}
        </div>

        {/* Action Button */}
        <div className="flex justify-center">
          <button
            onClick={handleMatchResumeJob}
            disabled={isLoading || resumeFiles.length === 0 || !jobDescription.trim()}
            className={`px-8 py-3 rounded-md font-medium ${
              isLoading || resumeFiles.length === 0 || !jobDescription.trim()
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            } text-white transition-colors`}
          >
            {isLoading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Analyzing...
              </div>
            ) : (
              'Match Resumes with Job'
            )}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md">
            {error}
          </div>
        )}
      </div>

      {/* Results Display */}
      {matchResult && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Matching Results</h2>
          
          {/* Match Score */}
          <div className="text-center mb-8">
            <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getScoreBgColor(matchResult.match_score)} mb-4`}>
              <span className={`text-3xl font-bold ${getScoreColor(matchResult.match_score)}`}>
                {matchResult.match_score}%
              </span>
            </div>
            <p className="text-lg font-medium text-gray-700">Match Score</p>
            <p className="text-sm text-gray-500">
              {matchResult.resume_skills_count} skills in resume • {matchResult.job_skills_count} skills in job
            </p>
          </div>

          {/* Skills Comparison */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Matched Skills */}
            <div>
              <h3 className="text-lg font-semibold text-green-600 mb-4">✅ Matched Skills</h3>
              {matchResult.matched_skills.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {matchResult.matched_skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">No skills matched</p>
              )}
            </div>

            {/* Missing Skills */}
            <div>
              <h3 className="text-lg font-semibold text-red-600 mb-4">❌ Missing Skills</h3>
              {matchResult.missing_skills.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {matchResult.missing_skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">All required skills are present!</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeAnalysis;
