export default function ResultsCard({ results }) {
    if (!results) return null
  
    return (
      <div className="mt-6 bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Analysis Results</h3>
  
        <div className="mb-4">
          <h4 className="font-medium text-gray-700 mb-2">Findings:</h4>
          <div className="bg-gray-50 p-4 rounded">
            <pre className="text-sm text-gray-600">
              {JSON.stringify(results.data, null, 2)}
            </pre>
          </div>
        </div>
  
        <div className="bg-blue-50 p-4 rounded">
          <h4 className="font-medium text-blue-800 mb-2">CIA Model Explanation:</h4>
          <p className="text-blue-700">{results.ciaExplanation}</p>
        </div>
      </div>
    )
  }