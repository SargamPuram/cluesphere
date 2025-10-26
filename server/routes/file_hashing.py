from flask import Blueprint, request, jsonify
import hashlib
import magic
from PIL import Image
import io
import math
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.binary import Binary
from bson.objectid import ObjectId
from datetime import datetime

file_hashing_bp = Blueprint('file_hashing', __name__)

# MongoDB Connection
# FIX: Ensure connection details are correct. Using a placeholder here.
client = MongoClient('mongodb+srv://sargampuram3:CKk8etX6deBFpnLb@cluster0.yb7y1yq.mongodb.net/')
db = client['cyber_forensics']
file_hashes_collection = db['file_hashes'] 

# Helper function to process file data (used by both endpoints)
def process_file_data(file, file_bytes, file_size):
    """Calculates file info, hashes, entropy, and attempts metadata extraction."""
    
    file_info = {
        "original_filename": secure_filename(file.filename),
        "size_bytes": file_size,
        "size_kb": round(file_size / 1024, 2) if file_size > 0 else 0,
        "mime_type": magic.from_buffer(file_bytes, mime=True)
    }

    hashes = {
        "md5": hashlib.md5(file_bytes).hexdigest(),
        "sha1": hashlib.sha1(file_bytes).hexdigest(),
        "sha256": hashlib.sha256(file_bytes).hexdigest()
    }

    entropy = 0
    if file_size > 0:
        byte_counts = [file_bytes.count(i) for i in range(256)]
        byte_probs = [count / file_size for count in byte_counts if count > 0]
        entropy = -sum(p * math.log2(p) for p in byte_probs) if byte_probs else 0
        entropy = round(entropy, 2)

    metadata = {}
    try:
        # NOTE: Metadata extraction here is basic, full extraction is in the separate metadata route
        if file_info["mime_type"].startswith("image/"):
            img = Image.open(io.BytesIO(file_bytes))
            metadata["image_format"] = img.format
            metadata["image_size"] = img.size
    except Exception:
        pass # Ignore metadata errors here

    return file_info, hashes, entropy, metadata


# Endpoint: Analyze and Store (initial upload as known good)
@file_hashing_bp.route('/analyze-and-store', methods=['POST'])
def analyze_and_store():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # FIX: Read file once for consistent hashing
        file_bytes = file.read()
        file_size = len(file_bytes)
        
        file_info, hashes, entropy, metadata = process_file_data(file, file_bytes, file_size)

        analysis = {
            "is_encrypted": entropy > 7.5,
            "is_image": file_info["mime_type"].startswith("image/")
        }

        cia_analysis = {
            "confidentiality": "Hash comparison helps identify known files and detect unauthorized modifications",
            "integrity": "Cryptographic hashes verify file integrity - any change would alter the hash",
            "availability": "File metadata helps verify legitimate access and usage patterns"
        }

        document = {
            "file_info": file_info,
            "hashes": hashes,
            "metadata": metadata,
            "entropy": entropy,
            "analysis": analysis,
            "cia_analysis": cia_analysis,
            # "file_binary": Binary(file_bytes), # Commented out for potentially large files
            "stored_at": datetime.utcnow()
        }
        # FIX: Insert into DB
        inserted_id = file_hashes_collection.insert_one(document).inserted_id

        response = document.copy()
        response["_id"] = str(inserted_id)
        response["message"] = f"File '{file_info['original_filename']}' analyzed and stored successfully as known good."

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Analysis failed during storage: {str(e)}"}), 500

# Endpoint: File Hashing (verify with DB check)
@file_hashing_bp.route('/file-hashing', methods=['POST'])
def hash_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # FIX: Read file once for consistent hashing
        file_bytes = file.read()
        file_size = len(file_bytes)
        
        file_info, hashes, entropy, metadata = process_file_data(file, file_bytes, file_size)
        
        # FIX: Query DB using the calculated SHA256 hash
        existing_doc = file_hashes_collection.find_one({"hashes.sha256": hashes["sha256"]})

        if existing_doc:
            # Found in DB: Use stored data
            hash_check = {
                "known_file": True,
                "matched_hash": hashes["sha256"],
                "matched_filename": existing_doc["file_info"]["original_filename"],
                "hash_type": "sha256"
            }

            analysis = {
                "is_known": True,
                "is_encrypted": existing_doc["entropy"] > 7.5,
                "is_image": existing_doc["file_info"]["mime_type"].startswith("image/")
            }

            response = {
                "file_info": existing_doc["file_info"],
                "hashes": hashes, # Use the freshly calculated hashes
                "hash_check": hash_check,
                "metadata": existing_doc.get("metadata", {}),
                "entropy": existing_doc["entropy"],
                "analysis": analysis,
                "cia_analysis": existing_doc["cia_analysis"],
                "stored_at": existing_doc["stored_at"].isoformat()
            }
            return jsonify(response)

        else:
            # Not found in DB: Use calculated data
            return jsonify({
                "hash_check": {
                    "known_file": False,
                    "message": "File hash not found in the database of known files."
                },
                "hashes": hashes,
                "file_info": file_info, 
                "metadata": metadata, # Now includes any basic metadata we could get
                "entropy": entropy, 
                "analysis": {
                    "is_known": False,
                    "is_encrypted": entropy > 7.5,
                    "is_image": file_info["mime_type"].startswith("image/")
                }
            }), 200 

    except Exception as e:
        return jsonify({"error": f"Analysis failed during verification: {str(e)}"}), 500

# Endpoint: Get Known Files (list stored files for forensics overview)
@file_hashing_bp.route('/get-known-files', methods=['GET'])
def get_known_files():
    # ... (Omitted, as this endpoint was not reported to have issues)
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        files = list(file_hashes_collection.find({}, {"file_binary": 0}).skip(skip).limit(limit)) 
        for file in files:
            file["_id"] = str(file["_id"])
            file["stored_at"] = file["stored_at"].isoformat()

        total = file_hashes_collection.count_documents({})
        return jsonify({
            "files": files,
            "total": total,
            "page": page,
            "limit": limit
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch files: {str(e)}"}), 500