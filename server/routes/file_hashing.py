from flask import Blueprint, request, jsonify, redirect, url_for
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
client = MongoClient('mongodb+srv://sargampuram3:CKk8etX6deBFpnLb@cluster0.yb7y1yq.mongodb.net/')
db = client['cyber_forensics']
file_hashes_collection = db['file_hashes']  # Collection for known good hashes and metadata

# Endpoint: Analyze and Store (initial upload as known good)
@file_hashing_bp.route('/analyze-and-store', methods=['POST'])
def analyze_and_store():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file.seek(0)
        file_bytes = file.read()
        file_size = len(file_bytes)

        file_info = {
            "original_filename": secure_filename(file.filename),
            "size_bytes": file_size,
            "size_kb": round(file_size / 1024, 2),
            "mime_type": magic.from_buffer(file_bytes, mime=True)
        }

        hashes = {
            "md5": hashlib.md5(file_bytes).hexdigest(),
            "sha1": hashlib.sha1(file_bytes).hexdigest(),
            "sha256": hashlib.sha256(file_bytes).hexdigest()
        }

        metadata = {}
        try:
            if file_info["mime_type"].startswith("image/"):
                img = Image.open(io.BytesIO(file_bytes))
                exif_data = img.info
                metadata = {
                    "image_format": img.format,
                    "image_mode": img.mode,
                    "image_size": img.size,
                    "exif_data": exif_data
                }
        except Exception as e:
            metadata["error"] = f"Metadata extraction failed: {str(e)}"

        entropy = 0
        if file_size > 0:
            byte_counts = [file_bytes.count(i) for i in range(256)]
            byte_probs = [count / file_size for count in byte_counts if count > 0]
            entropy = -sum(p * math.log2(p) for p in byte_probs)

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
            "entropy": round(entropy, 2),
            "analysis": analysis,
            "cia_analysis": cia_analysis,
            "file_binary": Binary(file_bytes),  # Optional; comment out if files are large
            "stored_at": datetime.utcnow()
        }
        inserted_id = file_hashes_collection.insert_one(document).inserted_id

        response = document.copy()
        response["_id"] = str(inserted_id)
        response["message"] = "File analyzed and stored successfully as known good."

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

# Endpoint: File Hashing (verify with DB check)
@file_hashing_bp.route('/file-hashing', methods=['POST'])
def hash_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file.seek(0)
        file_bytes = file.read()
        file_size = len(file_bytes)

        hashes = {
            "md5": hashlib.md5(file_bytes).hexdigest(),
            "sha1": hashlib.sha1(file_bytes).hexdigest(),
            "sha256": hashlib.sha256(file_bytes).hexdigest()
        }

        existing_doc = file_hashes_collection.find_one({"hashes.sha256": hashes["sha256"]})

        if existing_doc:
            file_info = existing_doc["file_info"]
            metadata = existing_doc["metadata"]
            entropy = existing_doc["entropy"]

            hash_check = {
                "known_file": True,
                "matched_hash": hashes["sha256"],
                "matched_filename": file_info["original_filename"],
                "hash_type": "sha256"
            }

            analysis = {
                "is_known": True,
                "is_encrypted": entropy > 7.5,
                "is_image": file_info["mime_type"].startswith("image/")
            }

            response = {
                "file_info": file_info,
                "hashes": hashes,
                "hash_check": hash_check,
                "metadata": metadata,
                "entropy": entropy,
                "analysis": analysis,
                "cia_analysis": existing_doc["cia_analysis"],
                "stored_at": existing_doc["stored_at"].isoformat()
            }
            return jsonify(response)

        else:
            return jsonify({
                "hash_check": {
                    "known_file": False,
                    "message": "File hash not found in the database of known files."
                },
                "hashes": hashes,
                "file_info": {
                     "original_filename": secure_filename(file.filename)
                }
            }), 200 # Return 200 OK because the API call itself was successful

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

# New Endpoint: Get Known Files (list stored files for forensics overview)
@file_hashing_bp.route('/get-known-files', methods=['GET'])
def get_known_files():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        files = list(file_hashes_collection.find({}, {"file_binary": 0}).skip(skip).limit(limit))  # Exclude binary for efficiency
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