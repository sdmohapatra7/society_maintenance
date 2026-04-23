from flask import Blueprint, render_template
from dev3.bl.reporting_bl import ReportingBL

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    stats = ReportingBL.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)
