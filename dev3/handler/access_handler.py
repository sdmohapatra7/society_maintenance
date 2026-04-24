from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from dev3.common import db
from sqlalchemy import text

access_bp = Blueprint('access', __name__, url_prefix='/access')

@access_bp.route('/')
@login_required
def index():
    if current_user.role != 'admin':
        return "Unauthorized", 403
    
    # Get all users and their current permissions
    q_users = text("SELECT id, username, email, role FROM users ORDER BY username")
    users = db.session.execute(q_users).fetchall()
    
    q_perms = text("SELECT user_id, feature_name, can_access FROM user_permissions")
    perms = db.session.execute(q_perms).fetchall()
    
    # Organize permissions by user_id
    user_perms = {}
    for p in perms:
        if p.user_id not in user_perms:
            user_perms[p.user_id] = {}
        user_perms[p.user_id][p.feature_name] = p.can_access
        
    features = ['societies', 'houses', 'users', 'billing', 'expenses', 'complaints']
    
    return render_template('access_management.html', 
                           users=users, 
                           user_perms=user_perms, 
                           features=features)

@access_bp.route('/update', methods=['POST'])
@login_required
def update_access():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    user_id = data.get('user_id')
    feature_name = data.get('feature_name')
    can_access = data.get('can_access')
    
    # Upsert permission
    q = text("""
        INSERT INTO user_permissions (user_id, feature_name, can_access)
        VALUES (:uid, :feature, :access)
        ON CONFLICT (user_id, feature_name)
        DO UPDATE SET can_access = EXCLUDED.can_access
    """)
    db.session.execute(q, {"uid": user_id, "feature": feature_name, "access": can_access})
    db.session.commit()
    
    return jsonify({"success": True})
