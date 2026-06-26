import React, { useState } from 'react';
import { Dna, Globe } from 'lucide-react';
import UploadForm from './components/UploadForm';
import ResultsDashboard from './components/ResultsDashboard';
import { uploadVCF, analyzeVCF, downloadReport } from './services/api';

function App() {
  const [currentView, setCurrentView] = useState('upload');
  const [jobId, setJobId] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setCurrentView('analyzing');
    setError(null);

    try {
      const uploadResponse = await uploadVCF(file);
      setJobId(uploadResponse.job_id);

      const analysisResults = await analyzeVCF(uploadResponse.job_id);
      setResults(analysisResults);
      setCurrentView('results');
    } catch (err) {
      setError(err.message);
      setCurrentView('upload');
    }
  };

  const handleDownloadReport = () => {
  if (jobId) {
    downloadReport(jobId);
  }
};

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Dna className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">SeqLens</h1>
              <p className="text-xs text-gray-500">Genomic Variant Annotator</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" 
               className="text-gray-500 hover:text-gray-700 transition-colors">
              <Globe className="w-5 h-5" />
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {currentView === 'upload' && (
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Analyze Your Genomic Variants
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto mb-8">
              Upload VCF files to get AI-powered pathogenicity predictions, 
              ACMG classifications, and professional PDF reports.
            </p>
            <UploadForm onUpload={handleUpload} isUploading={false} />
          </div>
        )}

        {currentView === 'analyzing' && (
          <div className="text-center py-20">
            <div className="inline-flex flex-col items-center gap-4">
              <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
              <h3 className="text-xl font-semibold text-gray-900">Analyzing Variants...</h3>
              <p className="text-gray-500">This may take a few moments</p>
            </div>
          </div>
        )}

        {currentView === 'results' && results && (
          <ResultsDashboard 
            results={results} 
            onDownloadReport={handleDownloadReport}
          />
        )}

        {error && (
          <div className="max-w-2xl mx-auto mt-8 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-center">
            {error}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-500">
          <p>SeqLens © 2024 | Built with FastAPI + React | For research purposes only</p>
        </div>
      </footer>
    </div>
  );
}

export default App;