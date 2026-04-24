from flask import Blueprint, render_template
from flask_login import login_required, current_user
from dev3.bl.accounting_bl import AccountingBL

accounting_bp = Blueprint('accounting', __name__, url_prefix='/accounting')

@accounting_bp.route('/')
@login_required
def index():
    if not current_user.has_feature('accounting'):
        # For now, if role is accountant or admin, show it
        if current_user.role not in ['admin', 'accountant']:
            return "Unauthorized", 403
            
    summary = AccountingBL.get_financial_summary()
    return render_template('accounting.html', summary=summary)
