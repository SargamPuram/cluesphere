import { useState } from 'react';
import axios from 'axios';
import UploadForm from '../components/UploadForm';
import LogResultsCard from '../components/LogResultsCard'; // <-- CHANGE THIS

export default function LogAnalysis() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (file) => {
    setIsLoading(true);
    setResults(null);
    setError('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/log-analysis', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResults(response.data); // <-- Store the whole response
    } catch (err) {
      setError(err.response?.data?.error || "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="border-b border-gray-200 pb-5">
          <h1 className="text-2xl font-bold text-gray-900">Log Analysis with AI Reporting</h1>
          <p className="mt-2 text-gray-600">
            Upload a log file to analyze for suspicious activities and generate an AI-powered incident summary.
          </p>
        </div>

        <UploadForm onSubmit={handleSubmit} techniqueName="Log" />

        {isLoading && (
          <div className="mt-4 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600">Analyzing and generating report...</p>
          </div>
        )}

        <LogResultsCard results={results} error={error} /> {/* <-- CHANGE THIS */}
      </div>
    </div>
  );
}