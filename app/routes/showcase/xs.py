import math
from flask import Blueprint, request, render_template_string, jsonify
from app import db
from app.database.models import Post, Comment

bp = Blueprint('tech_002_xs', __name__)

@bp.route('/posts/<int:id>/comments', methods=['POST'])
def add_comment(id):
    post = Post.query.get_or_404(id)
    comment_content = request.form['comment']
    # ----
    comment = Comment(content=comment_content, post_id=post.id)
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment added"})

@bp.route('/posts/<int:id>', methods=['GET'])
def view_post(id):
    post = Post.query.get_or_404(id)
    # ----
    template = f"""
    <h1>{post.title}</h1>
    <h2>Comments:</h2>
    <ul>
        {"".join(f"<li>{c.content}</li>" for c in post.comments)}
    </ul>
    <form method="post" action="/posts/{post.id}/comments">
        <textarea name="comment"></textarea>
        <button type="submit">Add Comment</button>
    </form>
    """
    return render_template_string(template)

@bp.route('/siterel/tech_002_xs', methods=['GET'])
def process_combined_data():
    initial_seed = 42.0
    string_seed = "QuantumLeapEngine"
    RANDOM_PATH_COMBINED = '/siterel/tech_002_xs'
    
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
