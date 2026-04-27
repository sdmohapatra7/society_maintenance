import os
import sys

# Add the project root to sys.path so we can import dev3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from dev3 import create_app
from dev3.common.mail_utils import send_invoice_email

app = create_app()

with app.app_context():
    success = send_invoice_email(
        recipient_email="sdmohapatra7@gmail.com",
        subject="Test Email from Society Maintenance",
        html_body="<h1>Hello</h1><p>If you see this, email works perfectly!</p>"
    )
    if success:
        print("MAIL_SUCCESS: The test email was sent successfully!")
    else:
        print("MAIL_FAILED: Failed to send the test email.")
