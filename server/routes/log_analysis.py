# in routes/log_analysis.py

from flask import Blueprint, request, jsonify
import os
import re
from collections import Counter
import google.generativeai as genai

log_analysis_bp = Blueprint('log_analysis', __name__)

# --- TEMPORARY HARDCODING FOR TESTING ---
# This is NOT a permanent solution. It is only to debug your key issue.

# 1. DELETE YOUR OLD, SHARED KEY FROM GOOGLE AI STUDIO.
# 2. CREATE A BRAND-NEW KEY.
# 3. PASTE THE NEW KEY BETWEEN THE QUOTATION MARKS BELOW.
api_key = 'AIzaSyCddsnciPg6WmiQG83YHWZHIZKC33wdTu0'

gemini_model = None
GEMINI_ENABLED = False

if not api_key or api_key == "PASTE_YOUR_NEW_KEY_HERE":
    print("Warning: API KEY IS MISSING. Please paste your new key into the api_key variable.")
else:
    try:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash-lite')
        GEMINI_ENABLED = True
        print("Gemini API configured successfully with hardcoded key.")
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")


# (The rest of your code is the same)
THREAT_PATTERNS = {
    'Failed Login': r'failed login|authentication failure|invalid password|failed password',
    'SQL Injection Attempt': r'(\'|%27).*(union|select|insert|update|delete|drop)',
    'Cross-Site Scripting (XSS)': r'<script>|(%3C|&lt;)script(%3E|&gt;)|javascript:',
    'Directory Traversal': r'\.\./|\.\.\\',
    'Command Injection': r'(;|\%3B)\s*(ls|dir|cat|whoami|uname|net\s+user)',
    'Unauthorized Access': r'access denied|unauthorized|forbidden',
    'Malware/Bot Activity': r'\.(exe|dll|sh|ps1)\s+HTTP/|cve-|masscan|nmap',
    'Error Condition': r'error|exception|critical'
}
IP_REGEX = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

def generate_gemini_report(summary_data):
    if not GEMINI_ENABLED or not gemini_model:
        return "Gemini report generation is disabled. Please check your API key and server logs."

    prompt = f"""
    You are a senior cybersecurity analyst. Your task is to generate a concise executive summary and an incident report based on the following log analysis data. The tone should be professional and informative.
    **Log Analysis Data:**
    - Total Suspicious Entries: {summary_data['total_suspicious']}
    - Top 5 Threats Detected: {summary_data['top_threats']}
    - Top 5 Suspicious Source IPs: {summary_data['top_source_ips']}
    **Instructions:**
    Using the data above, generate a report with the following sections using Markdown formatting:
    1.  **Executive Summary:** A brief, high-level overview of the findings.
    2.  **Key Findings:** A bulleted list detailing the most significant threats and attacker IPs.
    3.  **Recommended Actions:** A short, actionable list of next steps (e.g., "Investigate IPs", "Review firewall rules", "Patch vulnerable applications").
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Failed to generate Gemini report. Error: {str(e)}"

@log_analysis_bp.route('/log-analysis', methods=['POST'])
def analyze_log():
    if 'file' not in request.files: return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({"error": "No selected file"}), 400

    try:
        log_content = file.read().decode('utf-8', errors='ignore')
        log_lines = log_content.splitlines()
        suspicious_activities, threat_counts, source_ip_counts = [], Counter(), Counter()

        for i, line in enumerate(log_lines):
            for threat, pattern in THREAT_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    ip_match = re.search(IP_REGEX, line)
                    source_ip = ip_match.group(0) if ip_match else "N/A"
                    suspicious_activities.append({"line_number": i + 1, "threat_type": threat, "log_entry": line, "source_ip": source_ip})
                    threat_counts[threat] += 1
                    if source_ip != "N/A": source_ip_counts[source_ip] += 1
                    break
        
        top_threats = [{"threat": t, "count": c} for t, c in threat_counts.most_common(5)]
        top_source_ips = [{"ip": ip, "count": c} for ip, c in source_ip_counts.most_common(5)]
        summary_message = f"Found {len(suspicious_activities)} suspicious log entries across {len(threat_counts)} threat categories."

        summary_data_for_ai = { "total_suspicious": len(suspicious_activities), "top_threats": top_threats, "top_source_ips": top_source_ips }
        gemini_report = generate_gemini_report(summary_data_for_ai)

        return jsonify({
            "analysis_summary": summary_message,
            "total_suspicious": len(suspicious_activities),
            "top_threats": top_threats,
            "top_source_ips": top_source_ips,
            "suspicious_activities": suspicious_activities[:100],
            "gemini_report": gemini_report
        })

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500