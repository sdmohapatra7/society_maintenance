from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from dev3.common import db
from sqlalchemy import text
from datetime import datetime

event_bp = Blueprint('events', __name__)

@event_bp.route('/')
@login_required
def index():
    if current_user.role != 'admin' and not current_user.has_feature('events'):
        return "Unauthorized", 403
        
    q = text("SELECT id, title, description, TO_CHAR(event_date, 'YYYY-MM-DD HH24:MI') as event_date_str, TO_CHAR(event_date, 'YYYY-MM-DD\"T\"HH24:MI') as event_date_iso, location FROM events ORDER BY event_date DESC")
    events = [dict(row._mapping) for row in db.session.execute(q).fetchall()]
    return render_template('events.html', events=events)

@event_bp.route('/add', methods=['POST'])
@login_required
def add_event():
    if current_user.role != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    event_date = data.get('event_date')
    location = data.get('location', '')
    
    q = text("""
        INSERT INTO events (title, description, event_date, location) 
        VALUES (:title, :description, :event_date, :location)
    """)
    db.session.execute(q, {
        "title": title, "description": description, 
        "event_date": event_date, "location": location
    })
    db.session.commit()
    
    # BONUS: Send Automated Email Blast to all Residents
    from dev3.common.mail_utils import send_event_email
    q_emails = text("SELECT email FROM users WHERE role = 'resident' AND email IS NOT NULL AND is_active = TRUE")
    resident_emails = [row[0] for row in db.session.execute(q_emails).fetchall() if row[0]]
    
    if resident_emails:
        html_body = f"""
        <h3>New Society Event: {title}</h3>
        <p><strong>Date & Time:</strong> {event_date.replace('T', ' ')}</p>
        <p><strong>Location:</strong> {location}</p>
        <p>{description}</p>
        <br>
        <p>Looking forward to seeing you there!</p>
        <p><em>- Society Admin</em></p>
        """
        # Run email sending synchronously or asynchronously; doing it inline here for simplicity
        send_event_email(resident_emails, f"Society Event Invitation: {title}", html_body)

    return jsonify({"success": True})

@event_bp.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    if current_user.role != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    db.session.execute(text("DELETE FROM events WHERE id = :id"), {"id": event_id})
    db.session.commit()
    return jsonify({"success": True})

@event_bp.route('/edit/<int:event_id>', methods=['POST'])
@login_required
def edit_event(event_id):
    if current_user.role != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.json
    q = text("""
        UPDATE events 
        SET title = :title, description = :description, event_date = :event_date, location = :location
        WHERE id = :id
    """)
    db.session.execute(q, {
        "id": event_id,
        "title": data.get('title'), 
        "description": data.get('description', ''), 
        "event_date": data.get('event_date'), 
        "location": data.get('location', '')
    })
    db.session.commit()
    return jsonify({"success": True})
