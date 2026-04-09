import { useState, useRef, useEffect } from 'react';

export default function ChatInterface({ onStateChange, currentState }) {
  const [messages, setMessages] = useState([
    { role: 'ai', text: "Welcome to PathEdge! What role are you targeting and where are you located? We can do a Technical, HR, Resume Review, or I can generate a Job Prediction report based on your skills and local market!" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);



  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');
    const newMessages = [...messages, { role: 'user', text: userMessage }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const apiUrl = import.meta.env.PROD ? '/api/chat' : 'http://localhost:8000/api/chat';

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          message_history: messages.map(m => ({ role: m.role, text: m.text })),
          session_state: currentState
        })
      });

      if (!response.ok) throw new Error('API Error');

      const data = await response.json();

      setMessages(prev => [...prev, { role: 'ai', text: data.response }]);

      if (data.state) {
        onStateChange(data.state);
      }

      if (data.is_finished) {
        setMessages(prev => [...prev, { role: 'ai', text: "Session Completed. Your feedback has been logged to the database." }]);
      }

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { role: 'ai', text: "Sorry, there was an error connecting to the server. Please ensure the backend is running." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0a0f1c] relative z-0">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${msg.role === 'user'
                ? 'bg-primary-600 text-white rounded-br-sm'
                : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-sm'
              }`}>
              {msg.role === 'ai' && (
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-5 h-5 rounded bg-primary-500/20 flex items-center justify-center">
                    <svg className="w-3 h-3 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                  </div>
                  <span className="text-xs font-semibold text-slate-400">PathEdge AI</span>
                </div>
              )}
              <div className="prose prose-invert prose-sm max-w-none">
                {msg.text.split('\n').map((line, j) => (
                  <p key={j} className="mb-2 last:mb-0">{line}</p>
                ))}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 border border-slate-700 rounded-2xl p-4 rounded-bl-sm flex gap-2 items-center">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce delay-100"></div>
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce delay-200"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-4 bg-slate-900 border-t border-slate-800">
        <form onSubmit={handleSubmit} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            placeholder="Type your message..."
            className="w-full bg-slate-800 border border-slate-700 text-slate-200 rounded-xl pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent placeholder-slate-500 transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
          </button>
        </form>
        <div className="text-center mt-2">
          <span className="text-[10px] text-slate-500">Press Enter to send. Say &quot;stop&quot; to end the interview.</span>
        </div>
      </div>
    </div>
  );
}
