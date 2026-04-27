from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from dev3.common import db
from sqlalchemy import text

visitor_bp = Blueprint('visitors', __name__)

@visitor_bp.route('/')
@login_required
def index():
    if not current_user.has_feature('visitors') and current_user.role not in ['staff', 'resident', 'security_guard']:
        return "Unauthorized", 403
        
    # Get houses for dropdown
    q_houses = text("SELECT id, house_no, wing FROM houses ORDER BY wing, house_no")
    houses = [dict(row._mapping) for row in db.session.execute(q_houses).fetchall()]
    
    # Get visitors based on role
    if current_user.role == 'resident':
        q = text("""
            SELECT v.id, v.house_id, v.name, v.phone, v.purpose, v.status, 
                   TO_CHAR(v.entry_time, 'YYYY-MM-DD HH24:MI') as entry_time_str, 
                   TO_CHAR(v.exit_time, 'YYYY-MM-DD HH24:MI') as exit_time_str, 
                   h.house_no, h.wing 
            FROM visitors v
            JOIN houses h ON v.house_id = h.id
            WHERE v.house_id = :house_id
            ORDER BY v.entry_time DESC
        """)
        visitors = [dict(row._mapping) for row in db.session.execute(q, {"house_id": current_user.house_id}).fetchall()]
    else:
        q = text("""
            SELECT v.id, v.house_id, v.name, v.phone, v.purpose, v.status, 
                   TO_CHAR(v.entry_time, 'YYYY-MM-DD HH24:MI') as entry_time_str, 
                   TO_CHAR(v.exit_time, 'YYYY-MM-DD HH24:MI') as exit_time_str, 
                   h.house_no, h.wing 
            FROM visitors v
            LEFT JOIN houses h ON v.house_id = h.id
            ORDER BY v.entry_time DESC
        """)
        visitors = [dict(row._mapping) for row in db.session.execute(q).fetchall()]
        
    return render_template('visitors.html', visitors=visitors, houses=houses)

@visitor_bp.route('/add', methods=['POST'])
@login_required
def add_visitor():
    if current_user.role not in ['admin', 'staff']:
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.json
    house_id = data.get('house_id')
    name = data.get('name')
    phone = data.get('phone', '')
    purpose = data.get('purpose', '')
    
    q = text("""
        INSERT INTO visitors (house_id, name, phone, purpose) 
        VALUES (:house_id, :name, :phone, :purpose)
    """)
    db.session.execute(q, {
        "house_id": house_id, "name": name, 
        "phone": phone, "purpose": purpose
    })
    db.session.commit()
    return jsonify({"success": True})

@visitor_bp.route('/checkout/<int:visitor_id>', methods=['POST'])
@login_required
def checkout_visitor(visitor_id):
    if current_user.role not in ['admin', 'staff']:
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    q = text("UPDATE visitors SET status = 'out', exit_time = NOW() WHERE id = :id")
    db.session.execute(q, {"id": visitor_id})
    db.session.commit()
    return jsonify({"success": True})

@visitor_bp.route('/edit/<int:visitor_id>', methods=['POST'])
@login_required
def edit_visitor(visitor_id):
    if current_user.role not in ['admin', 'staff']:
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.json
    q = text("""
        UPDATE visitors 
        SET house_id = :house_id, name = :name, phone = :phone, purpose = :purpose
        WHERE id = :id
    """)
    db.session.execute(q, {
        "id": visitor_id,
        "house_id": data.get('house_id'), 
        "name": data.get('name'), 
        "phone": data.get('phone', ''), 
        "purpose": data.get('purpose', '')
    })
    db.session.commit()
    return jsonify({"success": True})

@visitor_bp.route('/delete/<int:visitor_id>', methods=['POST'])
@login_required
def delete_visitor(visitor_id):
    if current_user.role not in ['admin', 'staff']:
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    db.session.execute(text("DELETE FROM visitors WHERE id = :id"), {"id": visitor_id})
    db.session.commit()
    return jsonify({"success": True})
