import { useState } from 'react'
import { CloudArrowUpIcon } from '@heroicons/react/24/outline'

export default function UploadForm({ onSubmit, techniqueName }) {
  const [file, setFile] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (file) {
      onSubmit(file)
    }
  }

  return (
    <div className="mt-7">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex items-center justify-center w-full">
          <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <CloudArrowUpIcon className="w-10 h-10 text-gray-400" />
              <p className="mb-2 text-sm text-gray-500">
                <span className="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-gray-500">
                {techniqueName} file (CSV, LOG, etc.)
              </p>
            </div>
            <input
              type="file"
              className="hidden"
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
          </label>
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
        >
          Analyze
        </button>
      </form>
    </div>
  )
}