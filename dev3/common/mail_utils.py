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

def send_event_email(recipient_emails, subject, html_body):
    if not recipient_emails:
        return True
    msg = Message(
        subject,
        bcc=recipient_emails,  # Use BCC so residents don't see each other's emails
        html=html_body,
        sender=current_app.config.get('MAIL_DEFAULT_SENDER')
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending event email: {e}")
        return False
