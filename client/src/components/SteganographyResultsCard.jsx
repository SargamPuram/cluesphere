export default function SteganographyResultsCard({ results, error }) {
    if (!results && !error) return null;
  
    if (error) {
      return (
        <div className="mt-6 bg-red-50 shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-red-800">Analysis Failed</h3>
          <p className="text-red-700 mt-2">{error}</p>
        </div>
      );
    }
  
    return (
      <div className="mt-6 bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Analysis Results</h3>
  
        <div className="mb-4 p-3 bg-blue-50 rounded">
          <p className="text-blue-700 font-semibold">{results.message}</p>
        </div>
  
        {results.hidden_text && (
          <div className="mb-6">
            <h4 className="font-medium text-gray-700 mb-2">Extracted Text</h4>
            <pre className="bg-gray-800 text-green-300 p-4 rounded text-sm overflow-x-auto">
              {results.hidden_text}
            </pre>
          </div>
        )}
  
        {results.cia_analysis && (
          <div className="bg-blue-50 p-4 rounded">
            <h4 className="font-medium text-blue-800 mb-2">CIA Model Explanation</h4>
            <p className="text-sm text-blue-700"><strong>Confidentiality:</strong> {results.cia_analysis.confidentiality}</p>
            <p className="text-sm text-blue-700 mt-1"><strong>Integrity:</strong> {results.cia_analysis.integrity}</p>
            <p className="text-sm text-blue-700 mt-1"><strong>Availability:</strong> {results.cia_analysis.availability}</p>
          </div>
        )}
      </div>
    );
  }