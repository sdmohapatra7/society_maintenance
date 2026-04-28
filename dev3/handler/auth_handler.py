from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required
from dev3.bl.user_bl import UserBL
from dev3.common.auth_utils import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, res = UserBL.login(username, password)
        if success:
            from dev3.common import db
            from sqlalchemy import text
            
            # Fetch role-based permissions
            q = text("SELECT feature_name FROM role_permissions WHERE role = :role AND can_access = TRUE")
            perms_rows = db.session.execute(q, {"role": res['role']}).fetchall()
            permissions = {r[0] for r in perms_rows}
            
            user_obj = User(res, permissions)
            login_user(user_obj)
            return redirect(url_for('main.dashboard'))
        else:
            flash(res, 'error')
            
    return render_template('login.html')

@auth_bp.route('/setup-password', methods=['GET', 'POST'])
def setup_password():
    token = request.args.get('token')
    if not token:
        return "Invalid Token", 400
        
    from dev3.common import db
    from sqlalchemy import text
    from datetime import datetime
    
    q = text("SELECT * FROM user_setup_tokens WHERE token = :token AND used = FALSE AND expires_at > :now")
    token_rec = db.session.execute(q, {"token": token, "now": datetime.now()}).fetchone()
    
    if not token_rec:
        return "Token expired or invalid", 400
        
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('setup_password.html', token=token)
            
        # Update user password
        from dev3.bl.user_bl import UserBL
        UserBL.change_password(token_rec.user_id, new_password)
        
        # Mark token as used
        db.session.execute(text("UPDATE user_setup_tokens SET used = TRUE WHERE id = :id"), {"id": token_rec.id})
        db.session.commit()
        
        flash("Password set successfully! You can now login.", "success")
        return redirect(url_for('auth.login'))
        
    return render_template('setup_password.html', token=token)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/login/google')
def login_google():
    from dev3 import oauth
    redirect_uri = url_for('auth.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/authorize')
def authorize_google():
    from dev3 import oauth
    from dev3.common import db
    from sqlalchemy import text
    from dev3.common.auth_utils import User
    
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if not user_info or not user_info.get('email'):
        flash("Google login failed", "error")
        return redirect(url_for('auth.login'))
        
    email = user_info['email']
    
    # Check if user exists in the database by email
    # Assuming email is either username or stored in users table
    # Wait, let's see if the user table has an email field
    q = text("SELECT id, username, email, role, house_id, password, is_active FROM users WHERE email = :email OR username = :email")
    user_rec = db.session.execute(q, {"email": email}).fetchone()
    
    if user_rec:
        if not user_rec.is_active:
            flash("Account is disabled", "error")
            return redirect(url_for('auth.login'))
            
        res = {
            "id": user_rec.id,
            "username": user_rec.username,
            "email": user_rec.email,
            "role": user_rec.role,
            "house_id": user_rec.house_id
        }
        
        # Fetch role-based permissions
        q_perms = text("SELECT feature_name FROM role_permissions WHERE role = :role AND can_access = TRUE")
        perms_rows = db.session.execute(q_perms, {"role": res['role']}).fetchall()
        permissions = {r[0] for r in perms_rows}
        
        user_obj = User(res, permissions)
        login_user(user_obj)
        return redirect(url_for('main.dashboard'))
    else:
        flash(f"User with email {email} not found in the system. Please contact the administrator.", "error")
        return redirect(url_for('auth.login'))
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        from dev3.common import db
        from sqlalchemy import text
        import secrets
        from datetime import datetime, timedelta
        
        q = text("SELECT id FROM users WHERE email = :email")
        user = db.session.execute(q, {"email": email}).fetchone()
        
        if user:
            token = secrets.token_urlsafe(32)
            expires = datetime.now() + timedelta(hours=1)
            
            q_token = text("INSERT INTO password_resets (user_id, token, expires_at) VALUES (:u_id, :token, :expires)")
            db.session.execute(q_token, {"u_id": user.id, "token": token, "expires": expires})
            db.session.commit()
            
            from dev3.common.mail_utils import send_reset_email
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            send_reset_email(email, reset_url)
            
            flash("Reset link sent! Please check your email.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("No account found with that email address.", "error")
            
    return render_template('forgot_password.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')
    if not token:
        return "Missing token", 400
        
    from dev3.common import db
    from sqlalchemy import text
    from datetime import datetime
    
    q = text("SELECT * FROM password_resets WHERE token = :token AND used = FALSE AND expires_at > :now")
    res_rec = db.session.execute(q, {"token": token, "now": datetime.now()}).fetchone()
    
    if not res_rec:
        return "Invalid or expired token", 400
        
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('reset_password.html', token=token)
            
        # Update user password
        from dev3.bl.user_bl import UserBL
        UserBL.change_password(res_rec.user_id, new_password)
        
        # Mark token as used
        db.session.execute(text("UPDATE password_resets SET used = TRUE WHERE id = :id"), {"id": res_rec.id})
        db.session.commit()
        
        flash("Password reset successful! You can now login.", "success")
        return redirect(url_for('auth.login'))
        
    return render_template('reset_password.html', token=token)

@auth_bp.route('/contact-admin', methods=['POST'])
def contact_admin():
    data = request.json
    message = data.get('message')
    user_email = data.get('email')
    user_name = data.get('name', 'Anonymous')
    
    from dev3.common import db
    from sqlalchemy import text
    
    # Get Admin Email from settings
    q = text("SELECT value FROM app_settings WHERE key = 'admin_email'")
    admin_email = db.session.execute(q).scalar() or "admin@society.com"
    
    from dev3.common.mail_utils import send_contact_email
    user_info = {"username": user_name, "email": user_email}
    send_contact_email(admin_email, user_info, message)
    
    return jsonify({"success": True})
