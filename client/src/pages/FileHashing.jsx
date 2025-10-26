import { useState } from 'react';
import axios from 'axios';
import UploadForm from '../components/UploadForm';
import FileResultsCard from '../components/FileResultsCard';

export default function FileHashing() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [mode, setMode] = useState('verify');  // 'verify' or 'store'

  const handleSubmit = async (file) => {
    setIsLoading(true);
    setResults(null); // Clear previous results
    const formData = new FormData();
    formData.append('file', file);

    const endpoint = mode === 'store' ? '/analyze-and-store' : '/file-hashing';

    try {
      // --- THIS IS THE UPDATED LINE (HARDCODED) ---
      const response = await axios.post(`https://cluesphere.onrender.com${endpoint}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Unified CIA explanation based on the technique
      const ciaExplanation = "File Hashing relates to **Integrity** (verifying file authenticity), **Confidentiality** (identifying known malicious files), and **Availability** (ensuring critical system files are untampered).";

      setResults({
        data: response.data,
        ciaExplanation: ciaExplanation
      });
    } catch (error) {
      console.error("Analysis error:", error);
      setResults({
        data: { error: error.response?.data?.error || "Analysis failed due to a network or server issue." },
        ciaExplanation: "Error occurred during analysis"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="border-b border-gray-200 pb-5">
          <h1 className="text-2xl font-bold text-gray-900">Advanced File Hashing & Analysis</h1>
          <p className="mt-2 text-gray-600">
            Upload a file to compute its cryptographic hash. Choose mode: Store as known good or verify against database.
          </p>
        </div>

        {/* Mode Selection */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Analysis Mode</label>
          <div className="mt-2 flex space-x-4">
            <label className="flex items-center">
              <input type="radio" name="analysis_mode" checked={mode === 'verify'} onChange={() => setMode('verify')} className="mr-2 text-blue-600 border-gray-300 focus:ring-blue-500" />
              Verify File (Check against known hashes)
            </label>
            <label className="flex items-center">
              <input type="radio" name="analysis_mode" checked={mode === 'store'} onChange={() => setMode('store')} className="mr-2 text-blue-600 border-gray-300 focus:ring-blue-500" />
              Store as Known Good
            </label>
          </div>
        </div>

        <UploadForm onSubmit={handleSubmit} techniqueName="File" />

        {isLoading && (
          <div className="mt-4 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600">Processing file...</p>
          </div>
        )}

        <FileResultsCard results={results} />
      </div>
    </div>
  );
}