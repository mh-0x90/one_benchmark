import math
from flask import Blueprint, request, jsonify, render_template_string
from app.database.models import User
from app import db

bp = Blueprint('tech_004_cs', __name__)

# In a real app, you'd have a login mechanism that sets a session cookie.
# For this demo, we'll assume a user is "logged in".
LOGGED_IN_USER_ID = 1

@bp.route('/account/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        # ----
        to_account = request.form['to_account']
        amount = float(request.form['amount'])
        
        sender = User.query.get(LOGGED_IN_USER_ID)
        
        if sender.balance >= amount:
            sender.balance -= amount
            db.session.commit()
            return "Transfer successful!"
        else:
            return "Insufficient funds.", 400

    # A simple form to initiate the transfer
    form = """
    <form method="post" action="/account/transfer">
        <h2>Transfer Funds</h2>
        <p>To Account: <input type="text" name="to_account" value="2"></p>
        <p>Amount: <input type="text" name="amount" value="100"></p>
        <button type="submit">Transfer</button>
    </form>
    """
    return render_template_string(form)

@bp.route('/siterel/tech_004_cs', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_004_cs'
    
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
