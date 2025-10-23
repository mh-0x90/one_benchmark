import math
from flask import Blueprint, request, render_template_string, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired
from app.database.models import User
from app import db

bp = Blueprint('tech_004_cs_s', __name__)

# In a real app, you'd have a login mechanism that sets a session cookie.
# For this demo, we'll assume a user is "logged in".
LOGGED_IN_USER_ID = 1

class TransferForm(FlaskForm):
    to_account = StringField('To Account', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Transfer')

@bp.route('/sr/account/transfer', methods=['GET', 'POST'])
def transfer():
    form = TransferForm()
    if form.validate_on_submit():
        to_account = form.to_account.data
        amount = form.amount.data
        
        sender = User.query.get(LOGGED_IN_USER_ID)
        
        if sender.balance >= amount:
            sender.balance -= amount
            # Receiver lookup and balance update would happen here
            db.session.commit()
            flash('Transfer successful!')
        else:
            flash('Insufficient funds.')
        return render_template_string("""
            {% with messages = get_flashed_messages() %}
              {% if messages %}
                <ul>
                {% for message in messages %}
                  <li>{{ message }}</li>
                {% endfor %}
                </ul>
              {% endif %}
            {% endwith %}
            <a href="/sr/account/transfer">New Transfer</a>
        """)

    # A simple form to initiate the transfer
    template = """
    <form method="post" action="/sr/account/transfer">
        {{ form.csrf_token }}
        <h2>Transfer Funds</h2>
        <p>{{ form.to_account.label }} {{ form.to_account(value='2') }}</p>
        <p>{{ form.amount.label }} {{ form.amount(value='100') }}</p>
        {{ form.submit() }}
    </form>
    """
    return render_template_string(template, form=form)

@bp.route('/siterel/tech_004_cs_s', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_004_cs_s'
    
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
