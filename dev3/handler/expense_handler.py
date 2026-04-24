import os
from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from dev3.bl.expense_bl import ExpenseBL

expense_bp = Blueprint('expense', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@expense_bp.route('/')
@login_required
def index():
    if current_user.role not in ['admin', 'staff', 'accountant']:
        return "Unauthorized", 403
    
    from dev3.common import db
    from sqlalchemy import text
    categories = db.session.execute(text("SELECT * FROM master_data WHERE category = 'EXPENSE_CATEGORY' AND is_active = TRUE")).fetchall()
    
    expenses = ExpenseBL.list_all()
    return render_template('expenses.html', expenses=expenses, categories=categories)

@expense_bp.route('/api', methods=['POST'])
@login_required
def create():
    if current_user.role not in ['admin', 'staff']:
        return jsonify({"error": "Unauthorized"}), 403
    
    title = request.form.get('title')
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('expense_date')
    description = request.form.get('description')
    
    receipt_url = None
    if 'receipt' in request.files:
        file = request.files['receipt']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'ui', 'uploads', 'expenses', filename)
            file.save(upload_path)
            receipt_url = f"/ui/uploads/expenses/{filename}"

    res = ExpenseBL.create(title, amount, category, date, description, receipt_url)
    return jsonify(dict(res._mapping)), 201
