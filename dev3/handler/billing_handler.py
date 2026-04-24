from flask import Blueprint, request, jsonify, render_template, make_response
from dev3.bl.maintenance_bl import MaintenanceBL
import os
import razorpay
from flask_login import login_required, current_user

RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_dummykey')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'dummysecret')
try:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except:
    razorpay_client = None

maintenance_bp = Blueprint('maintenance', __name__)

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
    pdf_bytes = MaintenanceBL.generate_invoice_pdf(bill_id)
    if not pdf_bytes:
        return "Invoice not found", 404
    
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=invoice_{bill_id}.pdf'
    return response

@maintenance_bp.route('/api/<int:bill_id>/status', methods=['PUT'])
def update_status(bill_id):
    data = request.json
    new_status = data.get('status', 'paid')
    from dev3.common import db
    from sqlalchemy import text
    from datetime import datetime
    
    paid_date = datetime.now().date() if new_status == 'paid' else None
    
    db.session.execute(text("UPDATE maintenance_bills SET status = :status, paid_date = :paid_date WHERE id = :id"), 
                       {"status": new_status, "id": bill_id, "paid_date": paid_date})
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
            return jsonify({"order_id": f"order_mock_{bill_id}", "amount": amount_in_paise, "key_id": RAZORPAY_KEY_ID})
            
    return jsonify({"order_id": f"order_mock_{bill_id}", "amount": amount_in_paise, "key_id": RAZORPAY_KEY_ID})

@maintenance_bp.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    bill_id = data.get('bill_id')
    from dev3.common import db
    from sqlalchemy import text
    from datetime import datetime
    
    paid_date = datetime.now().date()
    db.session.execute(text("UPDATE maintenance_bills SET status = 'paid', paid_date = :paid_date WHERE id = :id"), 
                       {"id": bill_id, "paid_date": paid_date})
    db.session.commit()
    return jsonify({"success": True, "message": "Payment verified"})
