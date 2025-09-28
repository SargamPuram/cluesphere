import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between">
          <div className="flex space-x-4">
            <Link to="/" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
              Home
            </Link>
            <Link to="/log-analysis" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
              Log Analysis
            </Link>
            <Link to="/file-hashing" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
              File Hashing
            </Link>
            <Link to="/metadata" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">Metadata Analysis</Link>

          </div>
        </div>
      </div>
    </nav>
  )
}