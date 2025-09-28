from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register blueprints
from routes.log_analysis import log_analysis_bp
from routes.file_hashing import file_hashing_bp
from routes.metadata import metadata_bp  

app.register_blueprint(log_analysis_bp)
app.register_blueprint(file_hashing_bp)
app.register_blueprint(metadata_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)