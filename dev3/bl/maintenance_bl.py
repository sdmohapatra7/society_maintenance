import os
from dev3.sql import maintenance_queries
from dev3.common import db
from sqlalchemy import text
from flask import current_app
from fpdf import FPDF
import io

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
    def generate_invoice_pdf(bill_id):
        # Fetch bill details
        q = text("""
            SELECT b.*, h.house_no, h.wing, h.resident_name, h.resident_email, s.name as society_name, s.address as society_address
            FROM maintenance_bills b
            JOIN houses h ON b.house_id = h.id
            JOIN societies s ON h.society_id = s.id
            WHERE b.id = :id
        """)
        bill = db.session.execute(q, {"id": bill_id}).fetchone()
        if not bill: return None

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 24)
        pdf.cell(0, 20, "MAINTENANCE INVOICE", ln=True, align="C")
        
        pdf.set_font("Helvetica", "", 12)
        pdf.ln(10)
        
        # Header Info
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(100, 10, f"Society: {bill.society_name}")
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 10, f"Invoice #: INV-{bill.id}", ln=True, align="R")
        
        pdf.cell(100, 10, f"Address: {bill.society_address or 'N/A'}")
        pdf.cell(0, 10, f"Bill Date: {bill.bill_month}", ln=True, align="R")
        
        pdf.ln(10)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Billing To
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Billed To:", ln=True)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 8, f"Resident: {bill.resident_name}", ln=True)
        pdf.cell(0, 8, f"House: {bill.wing}-{bill.house_no}", ln=True)
        pdf.cell(0, 8, f"Email: {bill.resident_email}", ln=True)
        
        pdf.ln(10)
        
        # Table Header
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(130, 10, "Description", 1, 0, "L", True)
        pdf.cell(60, 10, "Amount (INR)", 1, 1, "R", True)
        
        # Table Rows
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(130, 10, "Fixed Maintenance Charges", 1)
        pdf.cell(60, 10, f"{bill.fixed_charge:,.2f}", 1, 1, "R")
        
        pdf.cell(130, 10, "Area Based Charges", 1)
        pdf.cell(60, 10, f"{bill.area_charge:,.2f}", 1, 1, "R")
        
        if bill.late_fee > 0:
            pdf.cell(130, 10, "Late Fees", 1)
            pdf.cell(60, 10, f"{bill.late_fee:,.2f}", 1, 1, "R")
            
        if bill.other_charges > 0:
            pdf.cell(130, 10, "Other Charges", 1)
            pdf.cell(60, 10, f"{bill.other_charges:,.2f}", 1, 1, "R")
            
        # Total
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(130, 10, "TOTAL AMOUNT DUE", 1, 0, "L", True)
        pdf.cell(60, 10, f"{bill.amount:,.2f}", 1, 1, "R", True)
        
        pdf.ln(10)
        
        # Status
        status_color = (34, 197, 94) if bill.status == 'paid' else (239, 68, 68)
        pdf.set_text_color(*status_color)
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, f"STATUS: {bill.status.upper()}", ln=True, align="C")
        pdf.set_text_color(0, 0, 0)
        
        if bill.status == 'paid' and bill.paid_date:
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(0, 10, f"Paid On: {bill.paid_date}", ln=True, align="C")

        pdf.ln(20)
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 10, "Thank you for being a part of our community!", ln=True, align="C")
        
        # Return as bytes
        buffer = io.BytesIO()
        pdf.output(buffer)
        return buffer.getvalue()

    @staticmethod
    def generate_invoice_html(bill_id):
        # Keep for legacy or simple preview
        return "<html><body>Invoice Details Dummy</body></html>"

    @staticmethod
    def get_upcoming_notifications(date):
        q = text(maintenance_queries.get_bills_to_notify())
        return db.session.execute(q, {"due_date": date}).fetchall()
