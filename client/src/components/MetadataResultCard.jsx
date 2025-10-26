// client/src/components/MetadataResultCard.jsx
export default function MetadataResultCard({ results }) {
  if (!results) return null;

  // FIX: Destructure data from results, then get metadata from data
  const { data, ciaExplanation } = results;
  
  if (data.error) {
    return (
      <div className="mt-6 bg-red-50 shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-red-800 mb-2">An Error Occurred</h3>
        <p className="text-red-700">{data.error}</p>
      </div>
    );
  }

  const metadata = data?.metadata || {}; // Safely get metadata

  return (
    <div className="mt-6 bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        File Metadata Results
      </h3>

      <div className="mb-4">
        <h4 className="font-medium text-gray-700 mb-2">Extracted Metadata:</h4>
        <div className="bg-gray-50 p-4 rounded overflow-auto max-h-96">
          <table className="w-full text-sm text-left text-gray-600">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 font-medium">Property</th>
                <th className="px-4 py-2 font-medium">Value</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(metadata).length > 0 ?
                Object.entries(metadata).map(([key, value]) => (
                  <tr key={key} className="border-b">
                    <td className="px-4 py-2">{key}</td>
                    <td className="px-4 py-2 break-all">
                      {Array.isArray(value) || typeof value === 'object'
                        ? JSON.stringify(value)
                        : value?.toString()}
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="2" className="px-4 py-2 text-center text-gray-500">
                      No significant metadata extracted or file type is unsupported.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </div>

      {ciaExplanation && (
        <div className="bg-blue-50 p-4 rounded">
          <h4 className="font-medium text-blue-800 mb-2">CIA Model Explanation:</h4>
          <p className="text-blue-700">{ciaExplanation}</p>
        </div>
      )}
    </div>
  );
}