from dev3.sql import house_queries
from dev3.common import db
from sqlalchemy import text
from dev3.bl.user_bl import UserBL
import secrets
from datetime import datetime, timedelta
from dev3.common.mail_utils import send_invoice_email # We can reuse this or make a new one

class HouseBL:
    @staticmethod
    def create(society_id, wing, house_no, area_sq_ft, house_type, resident_name, resident_email, resident_phone):
        q = text(house_queries.insert_house())
        res = db.session.execute(q, {
            "society_id": society_id,
            "wing": wing,
            "house_no": house_no,
            "area_sq_ft": area_sq_ft,
            "house_type": house_type,
            "resident_name": resident_name,
            "resident_email": resident_email,
            "resident_phone": resident_phone
        })
        house = res.fetchone()
        db.session.commit()
        
        # Automatically create a user for the resident
        if resident_email and resident_name:
            username = resident_name.lower().replace(' ', '_')
            from dev3.bl.user_dbh import UserDBH
            if UserDBH.get_by_username(username):
                username = f"{username}_{house_no}"
                
            success, user = UserBL.register(
                username=username,
                email=resident_email,
                password=secrets.token_hex(16), # Temporary random password
                role="resident",
                house_id=house.id
            )
            
            if success:
                # Generate setup token
                token = secrets.token_urlsafe(32)
                expires_at = datetime.now() + timedelta(days=7)
                
                db.session.execute(text("""
                    INSERT INTO user_setup_tokens (user_id, token, expires_at)
                    VALUES (:user_id, :token, :expires_at)
                """), {"user_id": user['id'], "token": token, "expires_at": expires_at})
                db.session.commit()
                
                # Send welcome email
                setup_url = f"http://127.0.0.1:5000/auth/setup-password?token={token}"
                subject = "Welcome to SocietyPro - Set Up Your Account"
                html_body = f"""
                <div style="font-family: 'Outfit', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px;">
                    <h2 style="color: #4f46e5;">Welcome to {house.house_no}, {resident_name}!</h2>
                    <p>Your resident account has been created for your new home in SocietyPro.</p>
                    <p>To access your bills, file complaints, and manage your residence, please set your password by clicking the button below:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{setup_url}" style="background: #4f46e5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 700;">Set My Password</a>
                    </div>
                    <p style="color: #64748b; font-size: 0.85rem;">This link will expire in 7 days. If you did not expect this email, please contact your society administration.</p>
                    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
                    <p style="font-size: 0.8rem; color: #94a3b8;">SocietyPro - Premium Society Management System</p>
                </div>
                """
                send_invoice_email(resident_email, subject, html_body)
            
        return house

    @staticmethod
    def list_by_society(society_id):
        q = text(house_queries.list_houses_by_society())
        return db.session.execute(q, {"society_id": society_id}).fetchall()

    @staticmethod
    def get(house_id):
        q = text(house_queries.get_house_by_id())
        return db.session.execute(q, {"id": house_id}).fetchone()
