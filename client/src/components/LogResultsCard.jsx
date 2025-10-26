// in src/components/LogResultsCard.js

import React from 'react';
import ReactMarkdown from 'react-markdown';

export default function LogResultsCard({ results, error }) {
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
    <div className="mt-6 bg-white shadow rounded-lg p-6 space-y-8">
      
      {/* Gemini AI Report Section */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-3">🤖 AI Generated Incident Report</h3>
        {/* --- FIXES ARE HERE --- */}
        <div 
          className="bg-gray-50 p-6 rounded-lg border prose prose-sm max-w-none text-gray-800 break-words"
          style={{ whiteSpace: 'pre-wrap' }}
        >
          <ReactMarkdown>{results.gemini_report}</ReactMarkdown>
        </div>
      </div>

      {/* Analysis Summaries */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h4 className="font-medium text-gray-700 mb-2">Top 5 Threats</h4>
          <div className="overflow-x-auto border rounded-lg">
             <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Threat Type</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Count</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200 text-black">
                {results.top_threats.map((item, index) => (
                  <tr key={index}>
                    <td className="px-4 py-2 text-sm">{item.threat}</td>
                    <td className="px-4 py-2 text-sm">{item.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div>
          <h4 className="font-medium text-gray-700 mb-2">Top 5 Source IPs</h4>
          <div className="overflow-x-auto border rounded-lg">
            <table className="min-w-full">
               <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">IP Address</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Count</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200 text-black">
                {results.top_source_ips.map((item, index) => (
                  <tr key={index}>
                    <td className="px-4 py-2 text-sm font-mono">{item.ip}</td>
                    <td className="px-4 py-2 text-sm">{item.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Detailed Suspicious Activities */}
      <div>
        <h4 className="font-medium text-gray-700 mb-2">Suspicious Activity Details (First 100)</h4>
        <div className="overflow-x-auto border rounded-lg">
          <table className="min-w-full table-fixed">
            <thead className="bg-gray-50">
              <tr>
                <th className="w-1/12 px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Line</th>
                <th className="w-2/12 px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Threat Type</th>
                <th className="w-2/12 px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Source IP</th>
                <th className="w-7/12 px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Log Entry</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200 text-black">
              {results.suspicious_activities.map((item) => (
                <tr key={item.line_number}>
                  <td className="px-4 py-2 text-sm">{item.line_number}</td>
                  <td className="px-4 py-2 text-sm">{item.threat_type}</td>
                  <td className="px-4 py-2 text-sm font-mono">{item.source_ip}</td>
                  <td className="px-4 py-2 text-xs font-mono break-words">{item.log_entry}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* CIA Model Explanation */}
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