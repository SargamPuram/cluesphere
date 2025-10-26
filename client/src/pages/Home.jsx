import React from "react";

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Hero Section */}
      <header className="text-center py-16 px-6">
        <h1 className="text-4xl sm:text-5xl font-bold text-cyan-400 drop-shadow-md">
          Cyber Crime Forensics Analysis
        </h1>
        <p className="mt-4 text-lg text-gray-300 max-w-2xl mx-auto">
          A mini-project demonstrating multiple cyber forensic techniques for
          crime investigation and their evaluation against the{" "}
          <span className="font-semibold text-cyan-300">CIA Model</span>.
        </p>
      </header>

      {/* Case Workflow */}
      <section className="max-w-5xl mx-auto px-6 mt-10">
        <h2 className="text-2xl font-bold text-cyan-400 text-center mb-6">
          Investigation Workflow
        </h2>
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="bg-gray-800 p-6 rounded-xl text-center">
            <div className="text-4xl">📂</div>
            <p className="mt-2">Upload File</p>
          </div>
          <div className="text-3xl">➡️</div>
          <div className="bg-gray-800 p-6 rounded-xl text-center">
            <div className="text-4xl">🔎</div>
            <p className="mt-2">Run Analysis</p>
          </div>
          <div className="text-3xl">➡️</div>
          <div className="bg-gray-800 p-6 rounded-xl text-center">
            <div className="text-4xl">📊</div>
            <p className="mt-2">CIA Comparison</p>
          </div>
          <div className="text-3xl">➡️</div>
          <div className="bg-gray-800 p-6 rounded-xl text-center">
            <div className="text-4xl">📑</div>
            <p className="mt-2">Generate Report</p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-6 grid gap-8 sm:grid-cols-2 lg:grid-cols-3 mt-12">
        <div className="bg-gray-800 rounded-2xl shadow-md p-6 hover:shadow-cyan-500/50 transition">
          <div className="text-4xl">📜</div>
          <h2 className="mt-4 text-xl font-bold">Log Analysis</h2>
          <p className="mt-2 text-gray-400">Trace attacker activities and anomalies.</p>
        </div>

        <div className="bg-gray-800 rounded-2xl shadow-md p-6 hover:shadow-cyan-500/50 transition">
          <div className="text-4xl">🌐</div>
          <h2 className="mt-4 text-xl font-bold">PCAP Analysis</h2>
          <p className="mt-2 text-gray-400">Inspect packets to detect suspicious traffic.</p>
        </div>

        <div className="bg-gray-800 rounded-2xl shadow-md p-6 hover:shadow-cyan-500/50 transition">
          <div className="text-4xl">🖼️</div>
          <h2 className="mt-4 text-xl font-bold">Steganography</h2>
          <p className="mt-2 text-gray-400">Reveal hidden data in images.</p>
        </div>

        <div className="bg-gray-800 rounded-2xl shadow-md p-6 hover:shadow-cyan-500/50 transition">
          <div className="text-4xl">🛡️</div>
          <h2 className="mt-4 text-xl font-bold">Metadata Analysis</h2>
          <p className="mt-2 text-gray-400">Extract EXIF and hidden timestamps.</p>
        </div>

        <div className="bg-gray-800 rounded-2xl shadow-md p-6 hover:shadow-cyan-500/50 transition">
          <div className="text-4xl">🔑</div>
          <h2 className="mt-4 text-xl font-bold">File Hashing</h2>
          <p className="mt-2 text-gray-400">Verify integrity with hashes.</p>
        </div>
      </section>

      {/* Report Section */}
      <section className="mt-16 text-center">
        <h2 className="text-2xl font-bold text-cyan-400">Forensic Report</h2>
        <p className="mt-2 text-gray-300">Get a consolidated PDF with analysis results.</p>
        <button
          className="mt-4 px-6 py-2 bg-cyan-600 rounded-lg hover:bg-cyan-700 transition"
          onClick={() => alert("Report generation coming soon!")}
        >
          📑 Generate Report
        </button>
      </section>

      {/* Footer */}
      <footer className="mt-16 py-6 border-t border-gray-700 text-center text-gray-500">
        © 2025 Cyber Forensics Mini Project
      </footer>
    </div>
  );
};

export default Home;
