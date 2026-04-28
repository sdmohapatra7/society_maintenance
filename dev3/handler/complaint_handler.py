from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from dev3.bl.complaint_bl import ComplaintBL

complaint_bp = Blueprint('complaint', __name__)

@complaint_bp.route('/')
@login_required
def index():
    if not current_user.has_feature('complaints'):
        return "Unauthorized", 403
    if current_user.role in ['admin', 'staff']:
        from dev3.common import db
        from sqlalchemy import text
        q = text("SELECT c.*, u.username FROM complaints c JOIN users u ON c.user_id = u.id ORDER BY c.created_at DESC")
        complaints = db.session.execute(q).fetchall()
    else:
        complaints = ComplaintBL.list_by_user(current_user.id)
    return render_template('complaints.html', complaints=complaints)

@complaint_bp.route('/api', methods=['GET'])
@login_required
def get_complaints():
    from dev3.common import db
    from sqlalchemy import text
    if current_user.role in ['admin', 'staff']:
        q = text("SELECT c.*, u.username FROM complaints c JOIN users u ON c.user_id = u.id ORDER BY c.created_at DESC")
        complaints = db.session.execute(q).fetchall()
    else:
        q = text("SELECT * FROM complaints WHERE user_id = :u_id ORDER BY created_at DESC")
        complaints = db.session.execute(q, {"u_id": current_user.id}).fetchall()
    return jsonify([dict(row._mapping) for row in complaints])

@complaint_bp.route('/api/<int:id>', methods=['DELETE'])
@login_required
def delete_complaint(id):
    # Only admin or owner can delete
    from dev3.common import db
    from sqlalchemy import text
    if current_user.role != 'admin':
        check = db.session.execute(text("SELECT user_id FROM complaints WHERE id = :id"), {"id": id}).fetchone()
        if not check or check.user_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
            
    db.session.execute(text("DELETE FROM complaints WHERE id = :id"), {"id": id})
    db.session.commit()
    return jsonify({"success": True})

@complaint_bp.route('/api/<int:id>', methods=['PUT'])
@login_required
def update_complaint(id):
    data = request.json
    from dev3.common import db
    from sqlalchemy import text
    # Verify ownership
    if current_user.role != 'admin':
        check = db.session.execute(text("SELECT user_id FROM complaints WHERE id = :id"), {"id": id}).fetchone()
        if not check or check.user_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
            
    db.session.execute(text("""
        UPDATE complaints SET title = :title, description = :description 
        WHERE id = :id
    """), {"id": id, "title": data.get('title'), "description": data.get('description')})
    db.session.commit()
    return jsonify({"success": True})

import os
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@complaint_bp.route('/api', methods=['POST'])
@login_required
def create_complaint():
    title = request.form.get('title')
    description = request.form.get('description')
    
    from dev3.common import db
    from sqlalchemy import text
    
    # 1. Insert complaint first to get the ID
    q = text("""
        INSERT INTO complaints (user_id, title, description, status)
        VALUES (:user_id, :title, :description, 'open')
        RETURNING id
    """)
    res = db.session.execute(q, {
        "user_id": current_user.id,
        "title": title,
        "description": description
    })
    complaint_id = res.fetchone().id
    
    # 2. Handle multiple documents (images only)
    document_paths = []
    if 'document' in request.files:
        files = request.files.getlist('document')
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_dir = os.path.join(current_app.root_path, 'ui', 'uploads', 'complaints', str(complaint_id))
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                upload_path = os.path.join(upload_dir, filename)
                file.save(upload_path)
                document_paths.append(f"/ui/uploads/complaints/{complaint_id}/{filename}")

    # 3. Update complaint with document URLs
    doc_url_str = ",".join(document_paths) if document_paths else None
    db.session.execute(text("UPDATE complaints SET document_url = :doc_url WHERE id = :id"), 
                       {"doc_url": doc_url_str, "id": complaint_id})
    db.session.commit()
    
    # Return the full object
    q_full = text("SELECT * FROM complaints WHERE id = :id")
    row = db.session.execute(q_full, {"id": complaint_id}).fetchone()
    return jsonify(dict(row._mapping)), 201

@complaint_bp.route('/api/<int:id>/status', methods=['PATCH'])
@login_required
def update_status(id):
    if current_user.role not in ['admin', 'staff']:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    res = ComplaintBL.update_status(id, data.get('status'))
    return jsonify(dict(res._mapping))
