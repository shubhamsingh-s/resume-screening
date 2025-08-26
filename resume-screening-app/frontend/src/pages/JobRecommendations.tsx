import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Search, MapPin, DollarSign } from 'lucide-react'

const JobRecommendations: React.FC = () => {
  const { user } = useAuth();
  const [searching, setSearching] = useState(false)
  const [recommendations, setRecommendations] = useState<any[]>([])

  const handleSearchJobs = () => {
    setSearching(true)
    
    // Simulate job search
    setTimeout(() => {
      setRecommendations([
        {
          title: 'Senior React Developer',
          company: 'Tech Corp',
          location: 'San Francisco, CA',
          salary: '$120k - $150k',
          match: 95,
          skills: ['React', 'TypeScript', 'Node.js']
        },
        {
          title: 'Full Stack Engineer',
          company: 'StartupXYZ',
          location: 'Remote',
          salary: '$100k - $130k',
          match: 88,
          skills: ['Python', 'React', 'AWS']
        },
        {
          title: 'Machine Learning Engineer',
          company: 'AI Solutions',
          location: 'New York, NY',
          salary: '$130k - $160k',
          match: 82,
          skills: ['Python', 'ML', 'TensorFlow']
        }
      ])
      setSearching(false)
    }, 2000)
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Job Recommendations</h1>
        
        <div className="glassmorphism p-6 rounded-2xl mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Find Your Perfect Job</h2>
          <button
            onClick={handleSearchJobs}
            disabled={searching}
            className="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            {searching ? 'Searching...' : 'Get Recommendations'}
          </button>
        </div>

        {searching && (
          <div className="glassmorphism p-6 rounded-2xl text-center">
            <Search className="w-8 h-8 text-white/50 mx-auto mb-4 animate-pulse" />
            <p className="text-white">Finding personalized job recommendations...</p>
          </div>
        )}

        <div className="space-y-6">
          {recommendations.map((job, index) => (
            <div key={index} className="glassmorphism p-6 rounded-2xl">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-white">{job.title}</h3>
                  <p className="text-white/70">{job.company}</p>
                </div>
                <div className="text-right">
                  <div className="text-green-400 font-bold">{job.match}% Match</div>
                </div>
              </div>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-center text-white/70">
                  <MapPin className="w-4 h-4 mr-2" />
                  {job.location}
                </div>
                <div className="flex items-center text-white/70">
                  <DollarSign className="w-4 h-4 mr-2" />
                  {job.salary}
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2">
                {job.skills.map((skill: string, skillIndex: number) => (
                  <span key={skillIndex} className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm">
                    {skill}
                  </span>
                ))}
              </div>
              
              <button className="mt-4 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-colors">
                Apply Now
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default JobRecommendations
