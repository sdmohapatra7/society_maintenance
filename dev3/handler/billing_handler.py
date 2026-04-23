from flask import Blueprint, request, jsonify, render_template, make_response
from dev3.bl.maintenance_bl import MaintenanceBL

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/')
def index():
    # List all bills
    from dev3.common import db
    from sqlalchemy import text
    q = text("""
        SELECT b.*, h.house_no, h.wing, s.name as society_name 
        FROM maintenance_bills b
        JOIN houses h ON b.house_id = h.id
        JOIN societies s ON h.society_id = s.id
        ORDER BY b.bill_month DESC
    """)
    bills = db.session.execute(q).fetchall()
    return render_template('billing.html', bills=bills)

@maintenance_bp.route('/generate', methods=['POST'])
def generate_bill():
    data = request.json
    # Logic to calculate amount could be here or in BL
    res = MaintenanceBL.create_bill(
        data.get('house_id'),
        data.get('bill_month'),
        data.get('amount'),
        data.get('fixed_charge'),
        data.get('area_charge'),
        data.get('due_date')
    )
    return jsonify(dict(res._mapping)), 201

@maintenance_bp.route('/invoice/<int:bill_id>', methods=['GET'])
def view_invoice(bill_id):
    html_content = MaintenanceBL.generate_invoice_html(bill_id)
    if not html_content:
        return "Invoice not found", 404
    
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html'
    return response

@maintenance_bp.route('/api/send-email/<int:bill_id>', methods=['POST'])
def send_email(bill_id):
    # This would call BL to get HTML and send via mail_utils
    from dev3.common.mail_utils import send_invoice_email
    from dev3.sql import maintenance_queries
    from dev3.common import db
    from sqlalchemy import text

    q = text(maintenance_queries.get_bill_by_id())
    bill = db.session.execute(q, {"id": bill_id}).fetchone()
    
    if not bill:
        return jsonify({"error": "Bill not found"}), 404

    html_content = MaintenanceBL.generate_invoice_html(bill_id)
    subject = f"Maintenance Bill - {bill.bill_month} - {bill.society_name}"
    
    try:
        success = send_invoice_email(bill.resident_email, subject, html_content)
        if success:
            return jsonify({"message": "Email sent successfully"})
        else:
            return jsonify({"error": "Failed to send email. Check SMTP settings."}), 500
    except Exception as e:
        return jsonify({"error": f"Mail system error: {str(e)}"}), 500
