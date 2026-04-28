from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from dev3.common import db
from sqlalchemy import text

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/')
@login_required
def index():
    if current_user.role != 'admin':
        return "Unauthorized", 403
    
    # Fetch App Settings
    app_settings = db.session.execute(text("SELECT * FROM app_settings")).fetchall()
    
    # Fetch Master Data grouped by category
    master_rows = db.session.execute(text("SELECT * FROM master_data ORDER BY category, label")).fetchall()
    master_data = {}
    for r in master_rows:
        if r.category not in master_data:
            master_data[r.category] = []
        master_data[r.category].append(dict(r._mapping))
        
    # Fetch Roles
    roles = db.session.execute(text("SELECT * FROM roles ORDER BY name")).fetchall()
        
    return render_template('settings.html', 
                           settings_list=[dict(r._mapping) for r in app_settings], 
                           master_data=master_data,
                           roles=[dict(r._mapping) for r in roles])

@settings_bp.route('/app/update', methods=['POST'])
@login_required
def update_app_setting():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    db.session.execute(text("UPDATE app_settings SET value = :val WHERE key = :key"), 
                       {"val": data['value'], "key": data['key']})
    db.session.commit()
    return jsonify({"success": True})

@settings_bp.route('/master/add', methods=['POST'])
@login_required
def add_master_data():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    db.session.execute(text("""
        INSERT INTO master_data (category, label, value) 
        VALUES (:category, :label, :value)
    """), data)
    db.session.commit()
    return jsonify({"success": True})

@settings_bp.route('/master/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_master_data(id):
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    db.session.execute(text("DELETE FROM master_data WHERE id = :id"), {"id": id})
    db.session.commit()
    return jsonify({"success": True})

@settings_bp.route('/role/add', methods=['POST'])
@login_required
def add_role():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    try:
        db.session.execute(text("INSERT INTO roles (name, description) VALUES (:name, :description)"), data)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)})

@settings_bp.route('/role/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_role(id):
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    db.session.execute(text("DELETE FROM roles WHERE id = :id"), {"id": id})
    db.session.commit()
    return jsonify({"success": True})

@settings_bp.route('/logs')
@login_required
def view_logs():
    if current_user.role != 'admin':
        return "Unauthorized", 403
    
    import os
    log_path = os.path.join(os.getcwd(), 'app.log')
    if not os.path.exists(log_path):
        return "No log file found."
        
    with open(log_path, 'r') as f:
        # Get last 100 lines
        lines = f.readlines()
        content = "".join(lines[-100:])
        return f"<pre>{content}</pre>"

