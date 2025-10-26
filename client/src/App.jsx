import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import LogAnalysis from './pages/LogAnalysis'
import Home from './pages/Home'
import FileHashing from './pages/FileHashing'
import Metadata from './pages/Metadata'
import Steganography from './pages/Steganography'
import PCAPAnalysis from './pages/PCAPAnalysis'

function App() {
  return (
    <Router>
      <div className="min-h-screen min-w-screen bg-gray-50">
        <Navbar />
        <div className="py-8">
          <Routes>
            {/* Default route redirects to /log-analysis */}
            <Route path="/" element={<Home />} />
            <Route path="/log-analysis" element={<LogAnalysis />} />
            <Route path="/file-hashing" element={<FileHashing />} />
            <Route path="/metadata" element={<Metadata />} />
            <Route path="/steganography" element={<Steganography />} />
            <Route path="/pcap" element={<PCAPAnalysis />} />
            
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
