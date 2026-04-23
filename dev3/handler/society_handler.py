from flask import Blueprint, request, jsonify, render_template
from dev3.bl.society_bl import SocietyBL

society_bp = Blueprint('society', __name__)

@society_bp.route('/', methods=['GET'])
def index():
    societies = SocietyBL.list_all()
    return render_template('societies.html', societies=societies)

@society_bp.route('/api', methods=['GET'])
def get_societies():
    societies = [dict(row._mapping) for row in SocietyBL.list_all()]
    return jsonify(societies)

@society_bp.route('/api', methods=['POST'])
def create_society():
    data = request.json
    res = SocietyBL.create(
        data.get('name'),
        data.get('address'),
        data.get('registration_no'),
        data.get('contact_email')
    )
    return jsonify(dict(res._mapping)), 201

@society_bp.route('/api/<int:id>', methods=['PUT'])
def update_society(id):
    data = request.json
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("""
        UPDATE societies SET name = :name, address = :address, 
        registration_no = :registration_no, contact_email = :contact_email
        WHERE id = :id
    """), {
        "id": id,
        "name": data.get('name'),
        "address": data.get('address'),
        "registration_no": data.get('registration_no'),
        "contact_email": data.get('contact_email')
    })
    db.session.commit()
    return jsonify({"success": True})

@society_bp.route('/api/<int:id>', methods=['DELETE'])
def delete_society(id):
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("DELETE FROM societies WHERE id = :id"), {"id": id})
    db.session.commit()
    return jsonify({"success": True})

@society_bp.route('/<int:id>', methods=['GET'])
def get_society(id):
    society = SocietyBL.get(id)
    if not society:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(society._mapping))
