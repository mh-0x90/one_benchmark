import math
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.database.models import User

bp = Blueprint('tech_001_sq', __name__)

@bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['password']
    query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{pwd}'"
    
    # ----
    result = db.session.execute(query)
    user = result.fetchone()

    if user:
        response = make_response(jsonify({"message": f"Welcome {user.email}"}))
        response.set_cookie('user_id', str(user.id))
        return response
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/siterel/tech_001_sq', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_001_sq'
    
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


