# in routes/steganography.py

from flask import Blueprint, request, jsonify
from PIL import Image
import os

steganography_bp = Blueprint('steganography', __name__)

# Helper function to convert binary to string
def binary_to_string(binary_data):
    # Split binary string into 8-bit chunks
    byte_chunks = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    ascii_chars = []
    for byte in byte_chunks:
        if len(byte) == 8:
            # Check for a null terminator (8 zeros), a common way to end hidden messages
            if byte == '00000000':
                break
            try:
                ascii_chars.append(chr(int(byte, 2)))
            except ValueError:
                # This happens if a non-printable character is found
                pass 
    return "".join(ascii_chars)

@steganography_bp.route('/steganography', methods=['POST'])
def detect_steganography():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.lower().endswith(('.png', '.bmp', '.tiff')):
        return jsonify({"error": "Please upload a lossless image format like PNG for LSB analysis."}), 400
    
    try:
        image = Image.open(file.stream)
        pixels = image.load()
        width, height = image.size
        
        extracted_bits = ""
        
        # Iterate through each pixel to extract the LSB
        for y in range(height):
            for x in range(width):
                r, g, b, *a = pixels[x, y] # Use *a to handle images with/without alpha channel
                
                extracted_bits += bin(r)[-1]
                extracted_bits += bin(g)[-1]
                extracted_bits += bin(b)[-1]

        hidden_text = binary_to_string(extracted_bits)

        cia_analysis = {
            "confidentiality": "This tool attempts to break the confidentiality of a hidden message.",
            "integrity": "The presence of a hidden message proves the image's integrity was compromised.",
            "availability": "Poorly embedded steganography can corrupt an image, affecting its availability."
        }

        if hidden_text:
            return jsonify({
                "message": "Potential hidden data found!",
                "hidden_text": hidden_text,
                "cia_analysis": cia_analysis
            })
        else:
            return jsonify({
                "message": "No obvious hidden data found via LSB analysis.",
                 "cia_analysis": cia_analysis
            })

    except Exception as e:
        return jsonify({"error": f"Steganography analysis failed: {str(e)}"}), 500