export default function FileResultsCard({ results }) {
  if (!results) return null;

  const { data, ciaExplanation } = results;

  if (data.error) {
    return (
      <div className="mt-6 bg-red-50 shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-red-800 mb-2">An Error Occurred</h3>
        <p className="text-red-700">{data.error}</p>
      </div>
    );
  }

  const formatHash = (hash) => hash ? `${hash.substring(0, 6)}...${hash.substring(hash.length - 6)}` : '';

  return (
    <div className="mt-6 bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Analysis Results</h3>

      {/* Success / Store message */}
      {data.message && (
        <div className="mb-4 p-3 bg-blue-50 rounded">
          <p className="text-blue-700">{data.message}</p>
          {data._id && <p className="text-sm text-gray-600">Stored ID: {data._id}</p>}
          {data.stored_at && <p className="text-sm text-gray-600">Stored At: {data.stored_at}</p>}
        </div>
      )}

      {/* Basic File Info */}
      <div className="mb-6">
        <h4 className="font-medium text-gray-700 mb-2">Basic Information</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-sm font-medium text-gray-500">Filename</p>
            <p className="text-gray-900">{data.file_info?.original_filename}</p>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-sm font-medium text-gray-500">File Size</p>
            <p className="text-gray-900">{data.file_info?.size_kb} KB</p>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-sm font-medium text-gray-500">File Type</p>
            <p className="text-gray-900">{data.file_info?.mime_type}</p>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-sm font-medium text-gray-500">Entropy</p>
            <p className="text-gray-900">{data.entropy}</p>
          </div>
        </div>
      </div>

      {/* Cryptographic Hashes */}
      {data.hashes && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-700 mb-2">Cryptographic Hashes</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(data.hashes).map(([algorithm, hash]) => (
              <div key={algorithm} className="bg-gray-50 p-3 rounded">
                <p className="text-sm font-medium text-gray-500 capitalize">{algorithm}</p>
                <p className="text-gray-900 font-mono text-sm">{formatHash(hash)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Hash Check */}
      {data.hash_check && (
        <div className="mb-6 p-4 rounded-lg" 
             style={{ backgroundColor: data.hash_check.known_file ? '#D1FAE5' : '#FEF3C7' }}>
          <h4 className="font-medium mb-2" 
              style={{ color: data.hash_check.known_file ? '#065F46' : '#92400E' }}>
            Hash Check Status
          </h4>
          <p className="text-sm" 
             style={{ color: data.hash_check.known_file ? '#065F46' : '#92400E' }}>
            Known File: **{data.hash_check.known_file ? 'Yes (MATCHED)' : 'No (NEW/UNKNOWN)'}**
          </p>
          {data.hash_check.known_file ? (
            <>
              <p className="text-sm" 
                 style={{ color: data.hash_check.known_file ? '#065F46' : '#92400E' }}>
                Matched Filename: {data.hash_check.matched_filename}
              </p>
              <p className="text-sm" 
                 style={{ color: data.hash_check.known_file ? '#065F46' : '#92400E' }}>
                Matched Hash ({data.hash_check.hash_type}): {formatHash(data.hash_check.matched_hash)}
              </p>
            </>
          ) : (
            <p className="text-sm text-red-700 mt-1">{data.hash_check.message || "File hash not found in the database of known files."}</p>
          )}
        </div>
      )}

      {/* Metadata */}
      {data.metadata && Object.keys(data.metadata).length > 0 && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-700 mb-2">Metadata</h4>
          <pre className="bg-gray-50 p-3 rounded text-sm text-gray-600 overflow-x-auto">
            {JSON.stringify(data.metadata, null, 2)}
          </pre>
        </div>
      )}

      {/* CIA Explanation */}
      {ciaExplanation && (
        <div className="bg-blue-50 p-4 rounded">
          <h4 className="font-medium text-blue-800 mb-2">CIA Model Explanation</h4>
          <p className="text-blue-700">{ciaExplanation}</p>
        </div>
      )}
    </div>
  );
}