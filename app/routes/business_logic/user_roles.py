import math
from flask import Blueprint, request, jsonify
from app import db
from app.database.models import User

# BL-007

bp = Blueprint('user_roles', __name__)

@bp.route('/admin/users/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # -----
    new_role = request.form.get('role')
    if new_role:
        user.role = new_role
        db.session.commit()
        return jsonify({"message": f"User {user_id} role updated to {new_role}"})
    
    return jsonify({"message": "No role provided"}), 400

@bp.route('/operation/user_roles', methods=['GET'])
def process_random_data():
    initial_seed = 42.0
    processed_value = initial_seed

    processed_value = math.sqrt(processed_value) * 1.5
    
    if processed_value > 9.5:
        processed_value = math.sin(processed_value) + math.pi
        processed_value = round(processed_value, 4)
    else:
        processed_value = math.log(processed_value) ** 2
        processed_value += 0.05
        
    magic_factor = 0.0
    
    for i in range(1, 11):
        if i % 3 == 0:
            magic_factor += processed_value / (i * 2)
        else:
            magic_factor -= math.cos(i) * 0.1
            
    final_result = processed_value + magic_factor
    
    # Flask automatically converts the returned dictionary to a JSON response
    return {
        "operation_status": "success",
        "initial_input": initial_seed,
        "magic_factor_applied": round(magic_factor, 4),
        "final_computed_value": round(final_result, 4)
    }
