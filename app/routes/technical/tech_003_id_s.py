import math
from flask import Blueprint, jsonify
from app.database.models import Invoice

bp = Blueprint('tech_003_id_s', __name__)

# In a real app, you'd get this from the session
LOGGED_IN_USER_ID = 1 

@bp.route('/sr/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({"message": "Invoice not found"}), 404

    # ----
    if invoice.owner_user_id != LOGGED_IN_USER_ID:
        return jsonify({"message": "Forbidden"}), 403

    return jsonify({
        "id": invoice.id,
        "owner_user_id": invoice.owner_user_id,
        "amount": invoice.amount
    })

@bp.route('/siterel/tech_003_id_s', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_003_id_s'
    
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
