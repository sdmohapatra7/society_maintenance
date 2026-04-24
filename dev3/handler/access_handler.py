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
    
    # Get all unique roles from permissions and users table
    q_roles = text("SELECT DISTINCT role FROM role_permissions UNION SELECT DISTINCT role FROM users")
    roles = [row[0] for row in db.session.execute(q_roles).fetchall() if row[0]]
    
    # Get permissions for all roles
    q_perms = text("SELECT role, feature_name, can_access FROM role_permissions")
    perms = db.session.execute(q_perms).fetchall()
    
    # Organize permissions by role
    role_perms = {}
    for p in perms:
        if p.role not in role_perms:
            role_perms[p.role] = {}
        role_perms[p.role][p.feature_name] = p.can_access
        
    # Get unique features from permissions table
    q_features = text("SELECT DISTINCT feature_name FROM role_permissions")
    features = [row[0] for row in db.session.execute(q_features).fetchall() if row[0]]
    if not features:
        features = ['societies', 'houses', 'users', 'billing', 'expenses', 'complaints', 'reports', 'accounting']
    
    return render_template('access_management.html', 
                           roles=roles, 
                           role_perms=role_perms, 
                           features=features)

@access_bp.route('/update', methods=['POST'])
@login_required
def update_access():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    role = data.get('role')
    feature_name = data.get('feature_name')
    can_access = data.get('can_access')
    
    # Upsert role permission
    q = text("""
        INSERT INTO role_permissions (role, feature_name, can_access)
        VALUES (:role, :feature, :access)
        ON CONFLICT (role, feature_name)
        DO UPDATE SET can_access = EXCLUDED.can_access
    """)
    db.session.execute(q, {"role": role, "feature": feature_name, "access": can_access})
    db.session.commit()
    
    return jsonify({"success": True})
