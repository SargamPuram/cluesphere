import { useState } from 'react'
import axios from 'axios'
import UploadForm from '../components/UploadForm'
import ResultsCard from '../components/ResultsCard'

export default function LogAnalysis() {
  const [results, setResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (file) => {
    setIsLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('http://localhost:5000/log-analysis', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setResults({
        data: response.data,
        ciaExplanation: "This relates to Confidentiality because it detects unauthorized access attempts in the log files. The analysis helps identify potential breaches of confidential information by flagging suspicious activities."
      })
    } catch (error) {
      console.error("Analysis error:", error)
      setResults({
        data: { error: "Analysis failed" },
        ciaExplanation: "Error occurred during analysis"
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="border-b border-gray-200 pb-5">
          <h1 className="text-2xl font-bold text-gray-900">Log Analysis</h1>
          <p className="mt-2 text-gray-600">
            Upload a log file to analyze for suspicious activities. This technique helps identify unauthorized access attempts.
          </p>
        </div>

        <UploadForm onSubmit={handleSubmit} techniqueName="Log" />

        {isLoading && (
          <div className="mt-4 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600">Analyzing log file...</p>
          </div>
        )}

        <ResultsCard results={results} />
      </div>
    </div>
  )
}