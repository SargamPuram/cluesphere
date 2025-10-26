from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv 
import os # <-- 1. ADD THIS IMPORT

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
from routes.log_analysis import log_analysis_bp
from routes.file_hashing import file_hashing_bp
from routes.metadata import metadata_bp  
from routes.steganography import steganography_bp 
from routes.pcap_analysis import pcap_bp         

app.register_blueprint(log_analysis_bp)
app.register_blueprint(file_hashing_bp)
app.register_blueprint(metadata_bp)
app.register_blueprint(steganography_bp) 
app.register_blueprint(pcap_bp)         

if __name__ == '__main__':
    # --- 2. UPDATE THIS BLOCK ---
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)