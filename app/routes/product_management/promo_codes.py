import math
from flask import Blueprint, request, jsonify
from app.database.models import Coupon

# BL-002

bp = Blueprint('promo_codes', __name__)

# Assume a cart total for demonstration
CART_TOTAL = 200.0 

@bp.route('/cart/apply_coupon', methods=['POST'])
def apply_coupon():
    coupon_code = request.form.get('coupon_code')
    
    # -----
    coupon = Coupon.query.filter_by(code=coupon_code).first()

    if coupon:
        discount = (coupon.discount_percent / 100) * CART_TOTAL
        new_total = CART_TOTAL - discount
        return jsonify({
            "message": "Coupon applied!",
            "original_total": CART_TOTAL,
            "new_total": new_total,
            "discount_amount": discount
        })
    
    return jsonify({"message": "Invalid coupon code"}), 400

@bp.route('/operation/promo_codes', methods=['GET'])
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
