import math
from flask import Blueprint, request, jsonify
import requests
from urllib.parse import urlparse

bp = Blueprint('tech_005_sr_s', __name__)

ALLOWED_DOMAINS = ['example.com', 'api.example.com']

@bp.route('/sr/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        parsed_url = urlparse(url)
        # ----
        if parsed_url.hostname not in ALLOWED_DOMAINS:
            return jsonify({"error": "Invalid domain"}), 400
        
        # ----
        if parsed_url.scheme not in ['http', 'https']:
            return jsonify({"error": "Invalid scheme"}), 400

        response = requests.get(url, timeout=5)
        return response.text, response.status_code, response.headers.items()

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/siterel/tech_005_sr_s', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_005_sr_s'
    
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
