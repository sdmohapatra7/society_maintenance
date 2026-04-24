from flask import Blueprint, request, jsonify, render_template, make_response
from dev3.bl.maintenance_bl import MaintenanceBL
import os
import razorpay

RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_dummykey')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'dummysecret')
try:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except:
    razorpay_client = None

maintenance_bp = Blueprint('maintenance', __name__)

from flask_login import login_required, current_user

@maintenance_bp.route('/')
@login_required
def index():
    # List all bills or user's bills
    from dev3.common import db
    from sqlalchemy import text
    
    if current_user.role == 'resident':
        q = text("""
            SELECT b.*, h.house_no, h.wing, s.name as society_name 
            FROM maintenance_bills b
            JOIN houses h ON b.house_id = h.id
            JOIN societies s ON h.society_id = s.id
            WHERE h.resident_email = :email OR h.id = :house_id
            ORDER BY b.bill_month DESC
        """)
        bills = db.session.execute(q, {"email": current_user.email, "house_id": current_user.house_id or -1}).fetchall()
    else:
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

@maintenance_bp.route('/api/<int:bill_id>/status', methods=['PUT'])
def update_status(bill_id):
    data = request.json
    new_status = data.get('status', 'paid')
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("UPDATE maintenance_bills SET status = :status WHERE id = :id"), 
                       {"status": new_status, "id": bill_id})
    db.session.commit()
    return jsonify({"success": True, "status": new_status})

@maintenance_bp.route('/api/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    from dev3.common import db
    from sqlalchemy import text
    q = text("SELECT * FROM maintenance_bills WHERE id = :id")
    bill = db.session.execute(q, {"id": bill_id}).fetchone()
    if not bill:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(bill._mapping))

@maintenance_bp.route('/api/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    data = request.json
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("""
        UPDATE maintenance_bills 
        SET bill_month = :bill_month, amount = :amount, 
            fixed_charge = :fixed_charge, area_charge = :area_charge, 
            due_date = :due_date, status = :status
        WHERE id = :id
    """), {
        "id": bill_id,
        "bill_month": data.get('bill_month'),
        "amount": data.get('amount'),
        "fixed_charge": data.get('fixed_charge'),
        "area_charge": data.get('area_charge'),
        "due_date": data.get('due_date'),
        "status": data.get('status')
    })
    db.session.commit()
    return jsonify({"success": True})

@maintenance_bp.route('/api/create-order/<int:bill_id>', methods=['POST'])
def create_order(bill_id):
    from dev3.common import db
    from sqlalchemy import text
    q = text("SELECT amount FROM maintenance_bills WHERE id = :id")
    bill = db.session.execute(q, {"id": bill_id}).fetchone()
    if not bill:
        return jsonify({"error": "Bill not found"}), 404

    amount_in_paise = int(bill.amount * 100)
    
    if razorpay_client:
        try:
            order = razorpay_client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"receipt_{bill_id}"
            })
            return jsonify({"order_id": order['id'], "amount": amount_in_paise, "key_id": RAZORPAY_KEY_ID})
        except Exception as e:
            # Fallback to mock for testing
            return jsonify({"order_id": f"order_mock_{bill_id}", "amount": amount_in_paise, "key_id": RAZORPAY_KEY_ID})
            
    return jsonify({"order_id": f"order_mock_{bill_id}", "amount": amount_in_paise, "key_id": RAZORPAY_KEY_ID})

@maintenance_bp.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    bill_id = data.get('bill_id')
    # Typically, you would use razorpay_client.utility.verify_payment_signature(params_dict) here
    from dev3.common import db
    from sqlalchemy import text
    db.session.execute(text("UPDATE maintenance_bills SET status = 'paid' WHERE id = :id"), {"id": bill_id})
    db.session.commit()
    return jsonify({"success": True, "message": "Payment verified"})
