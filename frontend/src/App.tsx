import React, { useState } from 'react';

interface AnalysisResult {
  success: boolean;
  data: any;
  saved_to: string;
}

function App() {
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsLoading(true);
    setResults(null); // Clear previous results
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic }),
      });
      
      const data = await response.json();
      console.log('Results:', data);
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to analyze topic');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-600 via-slate-500 to-blue-400 flex flex-col items-center justify-center px-4 py-8">
      {/* Main Content */}
      <div className="text-center mb-12">
        <h1 className="text-6xl font-bold text-white mb-8 drop-shadow-lg">
          Political Debate Analyzer
        </h1>
        
        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter a political topic..."
            className="px-6 py-3 rounded-lg bg-white text-gray-800 placeholder-gray-500 shadow-lg focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 w-64 sm:w-auto"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !topic.trim()}
            className="px-6 py-3 rounded-lg bg-slate-500 bg-opacity-70 text-white shadow-lg hover:bg-opacity-90 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>
      </div>

      {/* Results Display */}
      {results && (
        <div className="w-full max-w-6xl bg-white bg-opacity-95 rounded-3xl shadow-2xl p-8 backdrop-blur-sm mb-8">
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Analysis Results</h2>
            <p className="text-gray-600">Saved to: <code className="text-sm bg-gray-100 px-2 py-1 rounded">{results.saved_to}</code></p>
          </div>
          
          <div className="bg-gray-50 rounded-xl p-6 overflow-auto max-h-[600px]">
            <pre className="text-sm text-gray-800 whitespace-pre-wrap break-words">
              {JSON.stringify(results.data, null, 2)}
            </pre>
          </div>
        </div>
      )}

      {/* Placeholder Content Grid - Show when no results */}
      {!results && !isLoading && (
        <div className="w-full max-w-6xl bg-white bg-opacity-95 rounded-3xl shadow-2xl p-8 backdrop-blur-sm">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Placeholder Cards */}
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="space-y-4">
                <div className="h-12 bg-gray-200 rounded-lg"></div>
                <div className="h-40 bg-gray-100 rounded-lg"></div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="w-full max-w-6xl bg-white bg-opacity-95 rounded-3xl shadow-2xl p-8 backdrop-blur-sm">
          <div className="flex flex-col items-center justify-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-slate-600 mb-4"></div>
            <p className="text-gray-600 text-lg">Analyzing debate perspectives...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
