import math
from flask import Blueprint, request, jsonify
from app import db
from app.database.models import Order

# BL-005

bp = Blueprint('refunds', __name__)

@bp.route('/orders/<int:order_id>/refund', methods=['POST'])
def refund_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    # -----
    refund_amount = float(request.form.get('amount', 0))

    if order.status == 'paid':
        order.status = 'refunded'
        order.refunded_amount = refund_amount
        # In a real app, this would also credit the user's account.
        db.session.commit()
        return jsonify({"message": f"Order {order_id} refunded for ${refund_amount}"})
    else:
        return jsonify({"message": "Order not eligible for refund"}), 400

@bp.route('/operation/refunds', methods=['GET'])
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
