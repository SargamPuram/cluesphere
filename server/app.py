from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv 
import os

load_dotenv()

app = Flask(__name__)

# --- THIS IS THE UPDATE ---
# Be more specific. Only allow requests from your live Vercel app
# and your local machine (for testing).
CORS(app, origins=["https://cluesphere.vercel.app", "http://localhost:3000"])

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
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)