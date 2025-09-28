from flask import Blueprint, request, jsonify
import pandas as pd
import io

log_analysis_bp = Blueprint('log_analysis', __name__)

@log_analysis_bp.route('/log-analysis', methods=['POST'])
def analyze_log():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the file content into a pandas DataFrame
        file_content = file.read().decode('utf-8')
        file.seek(0)  # Reset file pointer

        # Try CSV first
        try:
            df = pd.read_csv(io.StringIO(file_content))
        except:
            # If not CSV, try other formats
            try:
                df = pd.read_table(io.StringIO(file_content))
            except Exception as e:
                return jsonify({"error": f"Unsupported file format: {str(e)}"}), 400

        # Find suspicious activities
        suspicious_activities = df[df['activity'].str.contains('unauthorized|attack|malicious', case=False, na=False)]

        return jsonify({
            "suspicious_activities": suspicious_activities.to_dict('records'),
            "total_suspicious": len(suspicious_activities),
            "analysis_summary": f"Found {len(suspicious_activities)} suspicious activities in the log file"
        })

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500