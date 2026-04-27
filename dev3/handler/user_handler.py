from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from dev3.bl.user_bl import UserBL

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@login_required
def index():
    if current_user.role != 'admin':
        return "Unauthorized", 403
    from dev3.common import db
    from sqlalchemy import text
    
    # Fetch all users
    q_users = text("SELECT id, username, email, role, is_active FROM users")
    users = db.session.execute(q_users).fetchall()
    
    # Fetch all available roles (standard + custom)
    q_roles = text("""
        SELECT name FROM roles 
        UNION 
        SELECT 'admin' as name UNION SELECT 'staff' UNION SELECT 'resident' UNION SELECT 'accountant'
    """)
    roles = [row[0] for row in db.session.execute(q_roles).fetchall() if row[0]]
    roles.sort()
    
    return render_template('users.html', users=users, roles=roles)

@user_bp.route('/api', methods=['GET'])
@login_required
def get_users():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    from dev3.common import db
    from sqlalchemy import text
    q = text("SELECT id, username, email, role, is_active FROM users")
    users = db.session.execute(q).fetchall()
    return jsonify([dict(row._mapping) for row in users])

@user_bp.route('/api/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("""
        UPDATE users SET email = :email, role = :role 
        WHERE id = :id
    """), {"id": id, "email": data.get('email'), "role": data.get('role')})
    db.session.commit()
    return jsonify({"success": True})

@user_bp.route('/api/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("DELETE FROM users WHERE id = :id"), {"id": id})
    db.session.commit()
    return jsonify({"success": True})

@user_bp.route('/api', methods=['POST'])
@login_required
def create_user():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    success, res = UserBL.register(
        data.get('username'),
        data.get('email'),
        data.get('password'),
        data.get('role'),
        data.get('house_id')
    )
    if success:
        return jsonify(res), 201
    return jsonify({"error": res}), 400
