from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from dev3.common import db
from sqlalchemy import text

vehicle_bp = Blueprint('vehicles', __name__)

@vehicle_bp.route('/')
@login_required
def index():
    if not current_user.has_feature('vehicles') and current_user.role not in ['resident', 'security_guard']:
        return "Unauthorized", 403
        
    q_houses = text("SELECT id, house_no, wing FROM houses ORDER BY wing, house_no")
    houses = [dict(row._mapping) for row in db.session.execute(q_houses).fetchall()]
    
    if current_user.role == 'resident':
        q = text("""
            SELECT v.id, v.license_plate, v.make_model, v.vehicle_type, v.parking_slot, v.house_id, h.house_no, h.wing 
            FROM vehicles v
            JOIN houses h ON v.house_id = h.id
            WHERE v.house_id = :house_id
        """)
        vehicles = [dict(row._mapping) for row in db.session.execute(q, {"house_id": current_user.house_id}).fetchall()]
    else:
        q = text("""
            SELECT v.id, v.license_plate, v.make_model, v.vehicle_type, v.parking_slot, v.house_id, h.house_no, h.wing 
            FROM vehicles v
            LEFT JOIN houses h ON v.house_id = h.id
            ORDER BY h.wing, h.house_no
        """)
        vehicles = [dict(row._mapping) for row in db.session.execute(q).fetchall()]
        
    return render_template('vehicles.html', vehicles=vehicles, houses=houses)

@vehicle_bp.route('/add', methods=['POST'])
@login_required
def add_vehicle():
    if current_user.role != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.json
    q = text("""
        INSERT INTO vehicles (house_id, license_plate, make_model, vehicle_type, parking_slot) 
        VALUES (:house_id, :license_plate, :make_model, :vehicle_type, :parking_slot)
    """)
    try:
        db.session.execute(q, {
            "house_id": data.get('house_id'),
            "license_plate": data.get('license_plate'),
            "make_model": data.get('make_model'),
            "vehicle_type": data.get('vehicle_type'),
            "parking_slot": data.get('parking_slot')
        })
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)})

@vehicle_bp.route('/delete/<int:vehicle_id>', methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):
    if current_user.role != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    db.session.execute(text("DELETE FROM vehicles WHERE id = :id"), {"id": vehicle_id})
    db.session.commit()
    return jsonify({"success": True})

@vehicle_bp.route('/edit/<int:vehicle_id>', methods=['POST'])
@login_required
def edit_vehicle(vehicle_id):
    if current_user.role != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.json
    q = text("""
        UPDATE vehicles 
        SET house_id = :house_id, license_plate = :license_plate, 
            make_model = :make_model, vehicle_type = :vehicle_type, 
            parking_slot = :parking_slot
        WHERE id = :id
    """)
    try:
        db.session.execute(q, {
            "id": vehicle_id,
            "house_id": data.get('house_id'),
            "license_plate": data.get('license_plate'),
            "make_model": data.get('make_model'),
            "vehicle_type": data.get('vehicle_type'),
            "parking_slot": data.get('parking_slot')
        })
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)})
