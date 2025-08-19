import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, Briefcase, ArrowRight } from 'lucide-react'

const Dashboard: React.FC = () => {
  const navigate = useNavigate()

  const features = [
    {
      title: 'Resume Analysis',
      description: 'Upload and analyze your resume with AI-powered insights',
      icon: Upload,
      route: '/analyze_resume',
      color: 'from-blue-500 to-purple-600'
    },
    {
      title: 'Job Skills Extraction',
      description: 'Extract key skills from job descriptions automatically',
      icon: FileText,
      route: '/job_skills',
      color: 'from-green-500 to-teal-600'
    },
    {
      title: 'Job Matching',
      description: 'Get personalized job recommendations based on your profile',
      icon: Briefcase,
      route: '/recommend_jobs',
      color: 'from-orange-500 to-red-600'
    }
  ]

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-2">Resume Screening Dashboard</h1>
        <p className="text-white/70 mb-8">Choose a feature to get started</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="glassmorphism p-6 hover:scale-105 transition-transform cursor-pointer"
              onClick={() => navigate(feature.route)}
            >
              <div className={`w-16 h-16 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4`}>
                <feature.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-white/70 mb-4">{feature.description}</p>
              <div className="flex items-center text-purple-400">
                <span className="text-sm font-medium">Get Started</span>
                <ArrowRight className="w-4 h-4 ml-2" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
