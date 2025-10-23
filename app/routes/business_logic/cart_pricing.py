import math
from flask import Blueprint, request, jsonify
from app.database.models import Product

# BL-001

bp = Blueprint('cart_pricing', __name__)

@bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    # -----
    price = float(request.form.get('price'))
    quantity = int(request.form.get('quantity', 1))

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # In a real app, this would add to a cart object.
    # Here, we just calculate the total.
    total_price = price * quantity
    
    return jsonify({
        "message": f"Added {quantity} of {product.name} to cart.",
        "total": total_price
    })

@bp.route('/operation/cart_pricing', methods=['GET'])
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
