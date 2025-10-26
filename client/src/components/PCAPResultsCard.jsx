export default function PCAPResultsCard({ results, error }) {
  if (!results && !error) return null;

  if (error) {
    return (
      <div className="mt-6 bg-red-900/50 shadow rounded-lg p-6 border border-red-700">
        <h3 className="text-lg font-medium text-red-300">Analysis Failed</h3>
        <p className="text-red-200 mt-2">{error}</p>
      </div>
    );
  }

  return (
    <div className="mt-6 bg-gray-900 shadow-lg rounded-lg p-6 border border-gray-700">
      <h3 className="text-lg font-medium text-gray-100 mb-4">Forensic Analysis Summary</h3>

      {/* Security Findings */}
      <div className="mb-6">
        <h4 className="font-medium text-yellow-400 mb-2">🚨 Security Findings</h4>
        <div className="bg-yellow-900/30 border-l-4 border-yellow-500 p-4 rounded">
          <ul className="list-disc pl-5 space-y-1">
            {results.security_findings.map((finding, index) => (
              <li key={index} className="text-sm text-yellow-200">{finding}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Top Conversations & Protocol Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
        <div>
          <h4 className="font-medium text-gray-300 mb-2">Top 10 Conversations</h4>
          <div className="overflow-x-auto border border-gray-700 rounded-lg">
            <table className="min-w-full">
              <thead className="bg-gray-800">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-300 uppercase">Source IP</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-300 uppercase">Destination IP</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-300 uppercase">Packets</th>
                </tr>
              </thead>
              <tbody className="bg-gray-900 divide-y divide-gray-700">
                {results.top_conversations.map((conv, index) => (
                  <tr key={index} className="hover:bg-gray-800 transition-colors">
                    <td className="px-4 py-2 text-sm font-mono text-blue-300">{conv.src}</td>
                    <td className="px-4 py-2 text-sm font-mono text-green-300">{conv.dst}</td>
                    <td className="px-4 py-2 text-sm text-gray-200">{conv.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div>
          <h4 className="font-medium text-gray-300 mb-2">Protocol Distribution</h4>
          <div className="overflow-x-auto border border-gray-700 rounded-lg">
            <table className="min-w-full">
              <thead className="bg-gray-800">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-300 uppercase">Protocol</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-300 uppercase">Packet Count</th>
                </tr>
              </thead>
              <tbody className="bg-gray-900 divide-y divide-gray-700">
                {results.protocol_summary.map((proto, index) => (
                  <tr key={index} className="hover:bg-gray-800 transition-colors">
                    <td className="px-4 py-2 text-sm text-blue-300">{proto.protocol}</td>
                    <td className="px-4 py-2 text-sm text-gray-200">{proto.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* DNS Queries */}
      {results.dns_queries && results.dns_queries.length > 0 && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-300 mb-2">Unique DNS Queries Detected</h4>
          <div className="bg-gray-800 p-3 rounded text-sm text-gray-300 font-mono max-h-40 overflow-y-auto border border-gray-700">
            {results.dns_queries.join(', ')}
          </div>
        </div>
      )}

      {/* CIA Explanation */}
      <div className="bg-blue-900/30 border border-blue-700 p-4 rounded">
        <h4 className="font-medium text-blue-300 mb-2">CIA Model Explanation</h4>
        <p className="text-sm text-blue-200"><strong>Confidentiality:</strong> {results.cia_analysis.confidentiality}</p>
        <p className="text-sm text-blue-200 mt-1"><strong>Integrity:</strong> {results.cia_analysis.integrity}</p>
        <p className="text-sm text-blue-200 mt-1"><strong>Availability:</strong> {results.cia_analysis.availability}</p>
      </div>
    </div>
  );
}
