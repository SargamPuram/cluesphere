# in routes/steganography.py

from flask import Blueprint, request, jsonify
from PIL import Image
import os

steganography_bp = Blueprint('steganography', __name__)

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
        
        byte_chunk = []
        ascii_chars = []
        found_terminator = False

        # Iterate through each pixel
        for y in range(height):
            if found_terminator:
                break
            for x in range(width):
                if found_terminator:
                    break
                
                # Get pixel data, handle both RGB and RGBA
                pixel_data = pixels[x, y]
                
                # We only care about the R, G, B channels
                for c in pixel_data[:3]: 
                    
                    # Add the last bit (as a '0' or '1' char) to our chunk
                    byte_chunk.append(bin(c)[-1])

                    # Once we have 8 bits, process them
                    if len(byte_chunk) == 8:
                        byte_str = "".join(byte_chunk)
                        
                        # Check for the null terminator
                        if byte_str == '00000000':
                            found_terminator = True
                            break # Stop processing channels
                        
                        try:
                            # Convert the 8-bit string to an integer, then to a character
                            ascii_chars.append(chr(int(byte_str, 2)))
                        except ValueError:
                            # Not a printable character, just ignore it
                            pass
                        
                        # Reset the chunk for the next byte
                        byte_chunk = []

        hidden_text = "".join(ascii_chars)

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
        # We also catch memory errors here, just in case
        if isinstance(e, MemoryError):
            return jsonify({"error": "Analysis failed: Image is too large and caused a memory error."}), 500
        return jsonify({"error": f"Steganography analysis failed: {str(e)}"}), 500