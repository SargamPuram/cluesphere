import { useState } from 'react';
import axios from 'axios';
import UploadForm from '../components/UploadForm';
import MetadataResultCard from '../components/MetadataResultCard';

export default function Metadata() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (file) => {
    setIsLoading(true);
    setResults(null); // Clear previous results
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/metadata', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Wrap your data into results so ResultsCard can display it
      setResults({
        data: response.data, // IMPORTANT: data is nested here
        ciaExplanation:
          'Metadata analysis supports **Confidentiality** and **Integrity** by revealing hidden file attributes, potential authors, timestamps, and data leakage risks.',
      });
    } catch (error) {
      console.error('Metadata analysis error:', error);
      setResults({
        data: { error: error.response?.data?.error || 'Metadata analysis failed' },
        ciaExplanation: 'Error occurred during metadata analysis.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="border-b border-gray-200 pb-5">
          <h1 className="text-2xl font-bold text-gray-900">File Metadata Analysis</h1>
          <p className="mt-2 text-gray-600">
            Upload a file to extract its metadata, such as size, type, and hidden attributes (EXIF, PDF Info).
          </p>
        </div>

        <UploadForm onSubmit={handleSubmit} techniqueName="Metadata" />

        {isLoading && (
          <div className="mt-4 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600">Analyzing metadata...</p>
          </div>
        )}

        <MetadataResultCard results={results} />
      </div>
    </div>
  );
}