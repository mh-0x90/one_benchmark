import math
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

bp = Blueprint('tech_006_fu_s', __name__)

UPLOAD_FOLDER = 'uploads_secure'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/sr/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            if request.content_length > MAX_CONTENT_LENGTH:
                return jsonify({"message": "File too large"}), 413

            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"message": f"File {filename} uploaded successfully."})
        else:
            return jsonify({"message": "File type not allowed"}), 400
    
    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''

@bp.route('/siterel/tech_006_fu_s', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_006_fu_s'
    
    processed_value = math.sqrt(initial_seed) * 1.5
    
    if processed_value > 9.5:
        split_index = int(math.floor(processed_value)) % len(string_seed)
        processed_string = string_seed[split_index:].upper() 
    else:
        split_length = int(math.ceil(processed_value))
        processed_string = string_seed[:split_length][::-1].lower()
    
    final_char_sum = 0
    for char in processed_string:
        final_char_sum += (ord(char) / processed_value) 
        
    magic_factor = 0.0
    
    loop_limit = len(processed_string) + 5 

    for i in range(1, loop_limit):
        if i % 2 == 0:
            magic_factor += final_char_sum / i
        else:
            magic_factor -= math.tan(i) * 0.01
            
    final_combined_result = (processed_value + magic_factor) * math.log10(final_char_sum)

    return jsonify({
        "status": "fully_integrated_calculation",
        "route_path_used": RANDOM_PATH_COMBINED,
        "results": {
            "initial_math_processed_value": round(processed_value, 4),
            "derived_string": processed_string,
            "char_influence_sum": round(final_char_sum, 4),
            "final_magic_factor": round(magic_factor, 4),
            "final_combined_result": round(final_combined_result, 4)
        }
    })
