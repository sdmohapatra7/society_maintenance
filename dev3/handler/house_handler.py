from flask import Blueprint, request, jsonify, render_template
from dev3.bl.house_bl import HouseBL

house_bp = Blueprint('house', __name__)

@house_bp.route('/society/<int:society_id>', methods=['GET'])
def list_by_society(society_id):
    return render_template('houses.html', society_id=society_id)

@house_bp.route('/api', methods=['POST'])
def create_house():
    data = request.json
    res = HouseBL.create(
        data.get('society_id'),
        data.get('wing'),
        data.get('house_no'),
        data.get('area_sq_ft'),
        data.get('house_type'),
        data.get('resident_name'),
        data.get('resident_email'),
        data.get('resident_phone')
    )
    return jsonify(dict(res._mapping)), 201

@house_bp.route('/api/<int:id>', methods=['PUT'])
def update_house(id):
    data = request.json
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("""
        UPDATE houses SET wing = :wing, house_no = :house_no, area_sq_ft = :area_sq_ft,
        house_type = :house_type, resident_name = :resident_name, 
        resident_email = :resident_email, resident_phone = :resident_phone
        WHERE id = :id
    """), {
        "id": id,
        "wing": data.get('wing'),
        "house_no": data.get('house_no'),
        "area_sq_ft": data.get('area_sq_ft'),
        "house_type": data.get('house_type'),
        "resident_name": data.get('resident_name'),
        "resident_email": data.get('resident_email'),
        "resident_phone": data.get('resident_phone')
    })
    db.session.commit()
    return jsonify({"success": True})

@house_bp.route('/api/<int:id>', methods=['DELETE'])
def delete_house(id):
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("DELETE FROM houses WHERE id = :id"), {"id": id})
    db.session.commit()
    return jsonify({"success": True})

@house_bp.route('/api/society/<int:society_id>', methods=['GET'])
def get_houses_api(society_id):
    houses = [dict(row._mapping) for row in HouseBL.list_by_society(society_id)]
    return jsonify(houses)
