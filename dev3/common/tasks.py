from datetime import datetime, timedelta
from dev3.bl.maintenance_bl import MaintenanceBL
from dev3.common.mail_utils import send_invoice_email
from flask import current_app

def check_and_send_reminders(app):
    with app.app_context():
        # Check for bills due in 3 days
        reminder_date = (datetime.now() + timedelta(days=3)).date()
        upcoming_bills = MaintenanceBL.get_upcoming_notifications(reminder_date)
        
        print(f"Running automated reminder task for {reminder_date}. Found {len(upcoming_bills)} bills.")
        
        for bill in upcoming_bills:
            html_content = MaintenanceBL.generate_invoice_html(bill.id)
            subject = f"REMINDER: Maintenance Bill Due in 3 Days - {bill.society_name}"
            
            success = send_invoice_email(bill.resident_email, subject, html_content)
            if success:
                print(f"Sent reminder to {bill.resident_email} for bill {bill.id}")
            else:
                print(f"Failed to send reminder to {bill.resident_email}")
