import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags
import PyPDF2
import datetime

metadata_bp = Blueprint('metadata', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

@metadata_bp.route('/metadata', methods=['POST'])
def analyze_metadata():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # Save the file
        file.save(filepath)

        metadata = {}
        file_lower = filename.lower()

        # IMAGE: Extract EXIF
        if file_lower.endswith(('.jpg', '.jpeg', '.png')):
            try:
                img = Image.open(filepath)
                # Ensure getexif() is called, then use TAGS mapping
                exif_data = img._getexif()
                if exif_data:
                    # Clean up the EXIF data dictionary
                    metadata = {ExifTags.TAGS.get(k, k): v for k, v in exif_data.items()}
                else:
                    metadata = {"info": "No EXIF data found"}
            except Exception as e:
                metadata = {"error": f"Image EXIF extraction failed: {str(e)}"}

        # PDF: Extract metadata
        elif file_lower.endswith('.pdf'):
            try:
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    # Convert raw metadata object to a clean dictionary
                    if reader.metadata:
                        metadata = {k: v for k, v in reader.metadata.items() if v is not None}
                    else:
                         metadata = {"info": "No PDF metadata found"}
            except Exception as e:
                metadata = {"error": f"PDF metadata extraction failed: {str(e)}"}
        
        # PYTHON FILES (or other source code): Basic analysis
        elif file_lower.endswith(('.py', '.js', '.c', '.java')):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    line_count = len(content.splitlines())
                    char_count = len(content)
                    
                    metadata = {
                        "file_type_details": "Source Code",
                        "line_count": line_count,
                        "character_count": char_count,
                        "potential_author": os.path.getlogin() if hasattr(os, 'getlogin') else 'unknown_user',
                        "info": "This is often useful for tracking developers or code origin."
                    }
            except Exception as e:
                metadata = {"error": f"Code file analysis failed: {str(e)}"}

        # TEXT / OTHER FILES
        else:
            metadata = {"info": "No specific metadata extraction implemented for this file type."}

        # Add basic info
        metadata["filename"] = filename
        metadata["size_bytes"] = os.path.getsize(filepath)
        metadata["last_modified"] = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
        
        # Clean up temporary file
        os.remove(filepath)

        cia_analysis = "Metadata analysis supports Confidentiality and Integrity by revealing hidden file attributes and potential data leakage risks."

        return jsonify({
            "metadata": metadata,
            "cia_analysis": cia_analysis,
            "message": f"File '{filename}' uploaded and metadata extracted successfully."
        })

    except Exception as e:
        # Ensure file is removed even on failure
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": f"Metadata analysis failed: {str(e)}"}), 500