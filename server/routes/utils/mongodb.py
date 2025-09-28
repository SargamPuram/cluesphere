from pymongo import MongoClient
from datetime import datetime

class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://sargampuram3:CKk8etX6deBFpnLb@cluster0.yb7y1yq.mongodb.net/cyber_forensics")
        self.db = self.client["cyber_forensics"]
        self.files = self.db["files"]

    def store_file(self, filename, hash, metadata):
        file_document = {
            "filename": filename,
            "hash": hash,
            "metadata": metadata,
            "first_seen": datetime.now(),
            "last_seen": datetime.now(),
            "analysis": {
                "is_known": False,
                "is_suspicious": False,
                "notes": ""
            }
        }
        return self.files.insert_one(file_document)

    def find_file_by_hash(self, hash):
        return self.files.find_one({"hash": hash})

    def update_file_analysis(self, file_id, analysis_data):
        return self.files.update_one(
            {"_id": file_id},
            {"$set": {"analysis": analysis_data}}
        )

# Singleton instance
mongodb = MongoDB()