import math
from flask import Blueprint, request, jsonify
from app import db
from app.database.models import Product
import time

# BL-004

bp = Blueprint('stock_mgnt', __name__)

@bp.route('/buy_product/<int:product_id>', methods=['POST'])
def buy_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # -----
    if product.stock > 0:
        # Simulate a delay between checking stock and updating it
        time.sleep(1) 
        product.stock -= 1
        db.session.commit()
        return jsonify({"message": "Purchase successful!"})
    else:
        return jsonify({"message": "Out of stock"}), 400

@bp.route('/operation/stock_mgnt', methods=['GET'])
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
