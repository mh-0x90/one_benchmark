import math
from flask import Blueprint, request, jsonify
from app.database.models import User
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('tech_001_sq_s', __name__)

@bp.route('/sr/login', methods=['POST'])
def login():
    email = request.form.get('email')
    pwd = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    #----

    if user and user.password == pwd: 
        login_user(user)
        return jsonify({"message": f"Welcome {user.email}! You are now logged in."})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/sr/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "You have been logged out."})

@bp.route('/sr/profile')
@login_required
def profile():
    return jsonify({"email": current_user.email, "role": current_user.role, "id": current_user.id})


@bp.route('/siterel/tech_001_sq_s', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_001_sq_s'
    
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


