import { useState } from 'react';
import StudentCard from './components/StudentCard';
import ChatInterface from './components/ChatInterface';

function App() {
  const [studentState, setStudentState] = useState({
    student_name: null,
    target_role: null,
    core_skills: null,
    interview_type: null,
  });

  return (
    <div className="min-h-screen bg-dark-bg text-slate-100 font-sans selection:bg-primary-500 selection:text-white flex items-center justify-center p-4">
      
      {/* Main Container */}
      <div className="max-w-6xl w-full grid grid-cols-1 md:grid-cols-12 gap-6 h-[90vh]">
        
        {/* Left Sidebar - 4 cols */}
        <div className="md:col-span-4 h-full flex flex-col gap-6">
          {/* Header */}
          <div className="bg-dark-card rounded-3xl p-6 shadow-2xl border border-slate-700/50 flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 bg-gradient-to-tr from-primary-600 to-primary-400 rounded-2xl flex items-center justify-center shadow-lg shadow-primary-500/30 mb-4 transform rotate-3">
              <svg className="w-8 h-8 text-white -rotate-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <h1 className="text-2xl font-bold tracking-tight mb-1 text-white">PathEdge</h1>
            <p className="text-slate-400 text-sm">Your AI Career Coach</p>
          </div>

          {/* Student Profiler / Card */}
          <StudentCard state={studentState} />
        </div>

        {/* Right Section - 8 cols (Chat Interface) */}
        <div className="md:col-span-8 h-full bg-dark-card rounded-3xl shadow-2xl overflow-hidden border border-slate-700/50 flex flex-col">
          <ChatInterface onStateChange={setStudentState} currentState={studentState} />
        </div>
        
      </div>
    </div>
  );
}

export default App;
