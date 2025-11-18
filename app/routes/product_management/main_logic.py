from flask import Blueprint, request, jsonify
from .utils import validate_string_format

bp = Blueprint('main_logic', __name__)

@bp.route('/validate', methods=['GET'])
def validate_input():
    user_text = request.args.get('text')
    if not user_text:
        return jsonify({"message": "Please provide text to validate."}), 400

    if validate_string_format(user_text):
        return jsonify({"message": "Congratulations! The format is correct."})
    else:
        return jsonify({"message": "Invalid format. Please try again with the format 'xxxx-xxxxx-xxxxxx'."}), 400


@bp.route('/operation/magiclog', methods=['GET'])
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
