import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, Briefcase, ArrowRight, X, Bell, Sun, Moon, Sparkles, Target, Users, BarChart3, CheckCircle, Clock, TrendingUp } from 'lucide-react'

const Dashboard: React.FC = () => {
  const navigate = useNavigate()
  const [darkMode, setDarkMode] = useState(false)
  const [showNotification, setShowNotification] = useState(true)
  const [currentFeature, setCurrentFeature] = useState(0)

  const features = [
    {
      title: 'Resume Analysis',
      description: 'Upload and analyze your resume with AI-powered insights and get detailed skills extraction',
      icon: Upload,
      route: '/analyze_resume',
      color: 'from-blue-500 to-purple-600',
      stats: 'AI-Powered Analysis'
    },
    {
      title: 'Job Skills Extraction',
      description: 'Extract key skills from job descriptions automatically with advanced NLP techniques',
      icon: FileText,
      route: '/job_skills',
      color: 'from-green-500 to-teal-600',
      stats: 'Smart Extraction'
    },
    {
      title: 'Job Matching',
      description: 'Get personalized job recommendations based on your profile and skills match analysis',
      icon: Briefcase,
      route: '/recommend_jobs',
      color: 'from-orange-500 to-red-600',
      stats: 'Intelligent Matching'
    }
  ]

  const stats = [
    { icon: CheckCircle, label: 'Resumes Analyzed', value: '1K+', color: 'text-green-400' },
    { icon: Users, label: 'Happy Users', value: '500+', color: 'text-blue-400' },
    { icon: BarChart3, label: 'Success Rate', value: '95%', color: 'text-purple-400' },
    { icon: Clock, label: 'Avg. Analysis Time', value: '<30s', color: 'text-orange-400' }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % features.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900' : 'gradient-bg'}`}>
      {/* Notification Bar */}
      {showNotification && (
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-4 relative">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-4 h-4" />
              <span className="text-sm font-medium">
                🎉 New! AI-powered resume analysis with 95% accuracy
              </span>
            </div>
            <button
              onClick={() => setShowNotification(false)}
              className="p-1 hover:bg-white/10 rounded transition-colors"
              title="Close notification"
              aria-label="Close notification"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="p-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
              <Target className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">ResumeScreener</h1>
              <p className="text-white/60 text-sm">AI-Powered Resume Analysis</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleDarkMode}
              className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
              title="Toggle dark mode"
              aria-label="Toggle dark mode"
            >
              {darkMode ? (
                <Sun className="w-5 h-5 text-yellow-400" />
              ) : (
                <Moon className="w-5 h-5 text-gray-300" />
              )}
            </button>
            <button 
              className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors relative"
              title="Notifications"
              aria-label="View notifications"
            >
              <Bell className="w-5 h-5 text-white" />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
            </button>
          </div>
        </div>
      </header>

      <div className="p-8">
        <div className="max-w-7xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-white/10 px-4 py-2 rounded-full mb-6">
              <TrendingUp className="w-4 h-4 text-green-400" />
              <span className="text-sm text-white/80">Trusted by 500+ professionals</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 gradient-text">
              Transform Your Job Search
              <br />
              with AI-Powered Insights
            </h1>
            
            <p className="text-xl text-white/70 mb-8 max-w-3xl mx-auto">
              Get instant resume analysis, skills extraction, and personalized job recommendations 
              powered by advanced machine learning and natural language processing.
            </p>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
              {stats.map((stat, index) => (
                <div key={index} className="glassmorphism p-4 text-center">
                  <stat.icon className={`w-8 h-8 mx-auto mb-2 ${stat.color}`} />
                  <div className="text-2xl font-bold text-white">{stat.value}</div>
                  <div className="text-sm text-white/60">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Features Grid */}
          <div className="mb-16">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-white mb-4">Powerful Features</h2>
              <p className="text-white/70">Everything you need to optimize your job search process</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className={`glassmorphism p-8 hover:scale-105 transition-all duration-300 cursor-pointer group ${
                    index === currentFeature ? 'ring-2 ring-purple-500' : ''
                  }`}
                  onClick={() => navigate(feature.route)}
                  onMouseEnter={() => setCurrentFeature(index)}
                >
                  <div className={`w-20 h-20 rounded-2xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                    <feature.icon className="w-10 h-10 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                  <p className="text-white/70 mb-4 leading-relaxed">{feature.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-purple-400 bg-purple-400/10 px-3 py-1 rounded-full">
                      {feature.stats}
                    </span>
                    <div className="flex items-center text-purple-400 group-hover:translate-x-1 transition-transform">
                      <span className="text-sm font-medium">Explore</span>
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* CTA Section */}
          <div className="text-center">
            <div className="glassmorphism p-12 max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
              <p className="text-white/70 mb-8 text-lg">
                Join thousands of professionals who have transformed their job search with our AI-powered platform
              </p>
              <button
                onClick={() => navigate(features[0].route)}
                className="btn-primary text-lg px-8 py-4"
              >
                Start Analyzing Your Resume
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
