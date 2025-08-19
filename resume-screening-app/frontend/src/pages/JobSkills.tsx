import React, { useState } from 'react'
import { FileText, Search, List } from 'lucide-react'

const JobSkills: React.FC = () => {
  const [jobDescription, setJobDescription] = useState('')
  const [skills, setSkills] = useState<string[]>([])
  const [extracting, setExtracting] = useState(false)

  const handleExtractSkills = () => {
    if (jobDescription.trim()) {
      setExtracting(true)
      
      // Simulate skills extraction
      setTimeout(() => {
        const extractedSkills = [
          'React', 'Python', 'Machine Learning', 'Data Analysis',
          'JavaScript', 'SQL', 'AWS', 'Docker', 'Git', 'Agile'
        ]
        setSkills(extractedSkills)
        setExtracting(false)
      }, 1500)
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Job Skills Extraction</h1>
        
        <div className="glassmorphism p-6 rounded-2xl mb-8">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
            <FileText className="w-6 h-6 mr-2" />
            Enter Job Description
          </h2>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste your job description here..."
            className="w-full h-32 px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <button
            onClick={handleExtractSkills}
            disabled={extracting || !jobDescription.trim()}
            className="mt-4 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white font-bold py-2 px-4 rounded-lg transition-colors"
          >
            {extracting ? 'Extracting...' : 'Extract Skills'}
          </button>
        </div>

        {extracting && (
          <div className="glassmorphism p-6 rounded-2xl text-center">
            <Search className="w-8 h-8 text-white/50 mx-auto mb-4 animate-pulse" />
            <p className="text-white">Extracting skills from job description...</p>
          </div>
        )}

        {skills.length > 0 && (
          <div className="glassmorphism p-6 rounded-2xl">
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <List className="w-6 h-6 mr-2" />
              Extracted Skills
            </h3>
            <div className="flex flex-wrap gap-2">
              {skills.map((skill, index) => (
                <span key={index} className="bg-green-600 text-white px-3 py-1 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default JobSkills
