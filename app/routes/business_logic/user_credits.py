import math
from flask import Blueprint, request, jsonify
from app import db
from app.database.models import User

# BL-008

bp = Blueprint('user_credits', __name__)

# Assume a logged-in user
LOGGED_IN_USER_ID = 2 # Bob, who has a low balance

@bp.route('/account/add_credit', methods=['POST'])
def add_credit():
    user = User.query.get(LOGGED_IN_USER_ID)
    # -----
    amount = float(request.form.get('amount'))

    user.balance += amount
    db.session.commit()

    return jsonify({
        "message": f"Credit of {amount} added.",
        "new_balance": user.balance
    })

@bp.route('/operation/user_credits', methods=['GET'])
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
