import os
from lxml import etree
from dev3.sql import maintenance_queries
from dev3.common import db
from sqlalchemy import text
from flask import current_app

class MaintenanceBL:
    @staticmethod
    def create_bill(house_id, bill_month, amount, fixed_charge, area_charge, due_date, status='unpaid'):
        from datetime import datetime
        
        # Ensure dates are in correct format
        if isinstance(bill_month, str):
            # Handle YYYY-MM or YYYY-MM-DD
            if len(bill_month) == 7: bill_month += "-01"
            bill_month = datetime.strptime(bill_month, '%Y-%m-%d').date()
            
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

        q = text(maintenance_queries.insert_bill())
        res = db.session.execute(q, {
            "house_id": house_id,
            "bill_month": bill_month,
            "amount": amount,
            "fixed_charge": fixed_charge,
            "area_charge": area_charge,
            "late_fee": 0,
            "other_charges": 0,
            "due_date": due_date,
            "status": status
        })
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def generate_invoice_html(bill_id):
        # 1. Get Bill Data
        q = text(maintenance_queries.get_bill_by_id())
        bill = db.session.execute(q, {"id": bill_id}).fetchone()
        
        if not bill:
            return None

        # 2. Convert to XML
        root = etree.Element("Invoice")
        etree.SubElement(root, "BillID").text = str(bill.id)
        etree.SubElement(root, "SocietyName").text = bill.society_name
        etree.SubElement(root, "SocietyAddress").text = bill.society_address
        etree.SubElement(root, "HouseNo").text = f"{bill.wing}-{bill.house_no}"
        etree.SubElement(root, "ResidentName").text = bill.resident_name
        etree.SubElement(root, "BillMonth").text = str(bill.bill_month)
        etree.SubElement(root, "Amount").text = str(bill.amount)
        etree.SubElement(root, "FixedCharge").text = str(bill.fixed_charge)
        etree.SubElement(root, "AreaCharge").text = str(bill.area_charge)
        etree.SubElement(root, "DueDate").text = str(bill.due_date)
        etree.SubElement(root, "Status").text = bill.status

        # 3. Load XSLT
        xslt_path = os.path.join(current_app.root_path, 'ui', 'xslt', 'invoice.xslt')
        if not os.path.exists(xslt_path):
            # Fallback or create dummy for now
            return etree.tostring(root, encoding='unicode', pretty_print=True)

        xslt_tree = etree.parse(xslt_path)
        transform = etree.XSLT(xslt_tree)

        # 4. Transform
        result_tree = transform(root)
        return str(result_tree)

    @staticmethod
    def get_upcoming_notifications(date):
        q = text(maintenance_queries.get_bills_to_notify())
        return db.session.execute(q, {"due_date": date}).fetchall()
