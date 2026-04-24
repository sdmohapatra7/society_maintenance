from flask import Blueprint, render_template, request, redirect, url_for, flash
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
