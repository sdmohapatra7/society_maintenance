from flask import Blueprint, render_template, make_response, request, jsonify
from flask_login import login_required, current_user
from dev3.common import db
from sqlalchemy import text
import csv
import io
from datetime import datetime

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/')
@login_required
def index():
    if not current_user.has_feature('reports'):
        return "Unauthorized", 403
        
    # Get societies for filtering
    societies = db.session.execute(text("SELECT id, name FROM societies ORDER BY name")).fetchall()
    return render_template('reports.html', societies=societies)

@report_bp.route('/export', methods=['POST'])
@login_required
def export_report():
    if not current_user.has_feature('reports'):
        return "Unauthorized", 403
        
    data = request.form
    report_type = data.get('report_type')
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    society_id = data.get('society_id')
    status = data.get('status', 'all')

    output = io.StringIO()
    writer = csv.writer(output)
    filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d')}.csv"

    if report_type == 'billing':
        query = """
            SELECT s.name as society, b.bill_month, b.amount, b.status, b.paid_date, h.wing, h.house_no, h.resident_name
            FROM maintenance_bills b
            JOIN houses h ON b.house_id = h.id
            JOIN societies s ON h.society_id = s.id
            WHERE 1=1
        """
        params = {}
        if society_id and society_id != 'all':
            query += " AND s.id = :s_id"
            params['s_id'] = society_id
        if status and status != 'all':
            query += " AND b.status = :status"
            params['status'] = status
        if from_date:
            query += " AND b.bill_month >= :from_d"
            params['from_d'] = from_date
        if to_date:
            query += " AND b.bill_month <= :to_d"
            params['to_d'] = to_date
            
        query += " ORDER BY s.name, b.bill_month DESC"
        rows = db.session.execute(text(query), params).fetchall()
        
        writer.writerow(['Society', 'Month', 'Amount', 'Status', 'Paid Date', 'Wing', 'House No', 'Resident Name'])
        for r in rows:
            writer.writerow([r.society, r.bill_month, r.amount, r.status, r.paid_date, r.wing, r.house_no, r.resident_name])

    elif report_type == 'expenses':
        query = """
            SELECT s.name as society, e.category, e.amount, e.expense_date, e.description, e.payment_mode
            FROM expenses e
            JOIN societies s ON e.society_id = s.id
            WHERE 1=1
        """
        params = {}
        if society_id and society_id != 'all':
            query += " AND s.id = :s_id"
            params['s_id'] = society_id
        if from_date:
            query += " AND e.expense_date >= :from_d"
            params['from_d'] = from_date
        if to_date:
            query += " AND e.expense_date <= :to_d"
            params['to_d'] = to_date
            
        query += " ORDER BY e.expense_date DESC"
        rows = db.session.execute(text(query), params).fetchall()
        
        writer.writerow(['Society', 'Category', 'Amount', 'Date', 'Description', 'Payment Mode'])
        for r in rows:
            writer.writerow([r.society, r.category, r.amount, r.expense_date, r.description, r.payment_mode])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "text/csv"
    return response
