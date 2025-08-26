import { Route, Routes } from 'react-router-dom'; 
import Navigation from './components/ui/Navigation'; 
import Dashboard from './pages/Dashboard'; 
import ResumeAnalysis from './pages/ResumeAnalysis'; 
import JobSkills from './pages/JobSkills'; 
import JobRecommendations from './pages/JobRecommendations'; 
import { AuthProvider } from './contexts/AuthContext';

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analyze_resume" element={<ResumeAnalysis />} />
          <Route path="/job_skills" element={<JobSkills />} />
          <Route path="/recommend_jobs" element={<JobRecommendations />} />
        </Routes>
      </div>
    </AuthProvider>
  )
}

export default App;
