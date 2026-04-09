export default function StudentCard({ state }) {
  const isSetupComplete = state.student_name && state.target_role;
  
  return (
    <div className="bg-dark-card rounded-3xl p-6 shadow-2xl border border-slate-700/50 flex-1 flex flex-col relative overflow-hidden">
      
      {/* Decorative blobs */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-32 h-32 rounded-full bg-primary-500/10 blur-2xl pointer-events-none"></div>
      
      <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
        <svg className="w-5 h-5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        Current Profile
      </h2>

      {isSetupComplete ? (
        <div className="flex flex-col gap-5 flex-1 relative z-10">
          <div className="group">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Student Name</span>
            <div className="text-lg text-slate-200 font-medium group-hover:text-white transition-colors">{state.student_name}</div>
          </div>
          
          <div className="group">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Target Role</span>
            <div className="inline-flex items-center px-3 py-1 rounded-full bg-primary-500/10 text-primary-400 text-sm font-medium border border-primary-500/20 group-hover:border-primary-500/50 transition-colors">
              {state.target_role}
            </div>
          </div>

          {state.location && (
            <div className="group">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Location</span>
              <div className="text-sm text-slate-200 font-medium group-hover:text-white transition-colors">{state.location}</div>
            </div>
          )}

          <div className="group">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Core Skills</span>
            <p className="text-slate-300 text-sm leading-relaxed">{state.core_skills || "Analyzing..."}</p>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center text-center p-4 relative z-10">
          <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
          </div>
          <p className="text-slate-400 text-sm">Tell me about yourself in the chat to build your profile.</p>
        </div>
      )}

      {/* Mode Badge at the bottom */}
      <div className="mt-auto pt-6 border-t border-slate-700/50 relative z-10">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-2">Mode</span>
        <div className="flex items-center gap-2">
          {state.interview_type ? (
            <div className="flex items-center gap-2">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-primary-500"></span>
              </span>
              <span className="text-slate-200 font-medium">{state.interview_type} Interview</span>
            </div>
          ) : (
             <div className="flex items-center gap-2">
               <span className="w-3 h-3 rounded-full bg-slate-600"></span>
               <span className="text-slate-400">Classifying...</span>
             </div>
          )}
        </div>
      </div>
    </div>
  );
}
