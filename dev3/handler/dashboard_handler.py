from flask import Blueprint, render_template, redirect, url_for, make_response
from flask_login import login_required, current_user
from dev3.bl.reporting_bl import ReportingBL
import csv
import io
from dev3.common import db
from sqlalchemy import text

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    if current_user.role != 'admin':
        # If not admin, redirect to relevant page based on role
        if current_user.role == 'resident':
            return redirect(url_for('maintenance.index'))
        return redirect(url_for('complaint.index'))
        
    stats = ReportingBL.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@main_bp.route('/export/paid-bills')
@login_required
def export_paid_bills():
    if current_user.role != 'admin':
        return "Unauthorized", 403
        
    # Fetch all paid bills joined with society and house
    q = text("""
        SELECT s.name as society, b.bill_month, b.amount, b.paid_date, h.wing, h.house_no, h.resident_name
        FROM maintenance_bills b
        JOIN houses h ON b.house_id = h.id
        JOIN societies s ON h.society_id = s.id
        WHERE b.status = 'paid'
        ORDER BY s.name, b.bill_month DESC
    """)
    rows = db.session.execute(q).fetchall()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Society', 'Month', 'Amount', 'Paid Date', 'Wing', 'House No', 'Resident Name'])
    
    for r in rows:
        writer.writerow([r.society, r.bill_month, r.amount, r.paid_date, r.wing, r.house_no, r.resident_name])
        
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=paid_bills_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response
