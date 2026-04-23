from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_invoice_email(recipient_email, subject, html_body, pdf_attachment=None):
    msg = Message(
        subject,
        recipients=[recipient_email],
        html=html_body,
        sender=current_app.config.get('MAIL_DEFAULT_SENDER')
    )
    # In a real app, we might attach a PDF here.
    # For now, we send the HTML body which is the invoice.
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
