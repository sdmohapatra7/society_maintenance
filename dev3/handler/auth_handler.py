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

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
