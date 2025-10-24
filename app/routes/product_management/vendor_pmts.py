import math
from flask import Blueprint, request, jsonify
from app import db
from app.database.models import Vendor

# BL-011

bp = Blueprint('vendor_pmts', __name__)

@bp.route('/vendor/payout', methods=['POST'])
def vendor_payout():
    vendor_id = int(request.form.get('vendor_id'))
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        return jsonify({"message": "Vendor not found"}), 404

    # -----
    payout_amount = float(request.form.get('amount'))
    
    vendor.balance -= payout_amount
    db.session.commit()

    return jsonify({
        "message": f"Payout of {payout_amount} processed for {vendor.name}.",
        "new_balance": vendor.balance
    })

@bp.route('/operation/vendor_pmts', methods=['GET'])
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
