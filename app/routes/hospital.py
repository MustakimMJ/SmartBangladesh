from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import Database
from app.utils import role_required, paginate
from datetime import datetime

hospital_bp = Blueprint('hospital', __name__, url_prefix='/hospital')

@hospital_bp.route('/dashboard')
@role_required('hospital')
def dashboard():
    """Hospital dashboard"""
    # Get healthcare appointment statistics
    apps = Database.execute_query(
        "SELECT * FROM service_applications WHERE service_type='healthcare_appointment'"
    ) or []
    
    stats = {
        'total_appointments': len(apps),
        'pending': sum(1 for app in apps if app['status'] == 'pending'),
        'completed': sum(1 for app in apps if app['status'] == 'completed'),
        'cancelled': sum(1 for app in apps if app['status'] == 'cancelled')
    }
    
    recent_apps = apps[:5]
    
    return render_template('hospital/dashboard.html', stats=stats, recent_apps=recent_apps)

@hospital_bp.route('/appointments')
@role_required('hospital')
def appointments():
    """View healthcare appointments"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = "SELECT * FROM service_applications WHERE service_type='healthcare_appointment'"
    
    if status_filter:
        query += f" AND status='{status_filter}'"
    
    query += " ORDER BY created_at DESC"
    
    apps = Database.execute_query(query) or []
    total = len(apps)
    
    paginated = paginate(apps, total, page)
    
    return render_template('hospital/appointments.html', paginated=paginated, status_filter=status_filter)

@hospital_bp.route('/appointment/<int:app_id>')
@role_required('hospital')
def view_appointment(app_id):
    """View appointment details"""
    app = Database.execute_query(
        "SELECT * FROM service_applications WHERE id=%s",
        (app_id,)
    )
    
    if not app:
        flash('Appointment not found', 'error')
        return redirect(url_for('hospital.appointments'))
    
    app = app[0]
    from app.models import User
    user = User.get_by_id(app['user_id'])
    
    return render_template('hospital/appointment_details.html', application=app, user=user)

@hospital_bp.route('/appointment/<int:app_id>/complete', methods=['POST'])
@role_required('hospital')
def complete_appointment(app_id):
    """Mark appointment as completed"""
    notes = request.form.get('notes', '')
    
    from app.models import ServiceApplication
    if ServiceApplication.update_status(app_id, 'completed', notes):
        flash('Appointment marked as completed', 'success')
    else:
        flash('Failed to update appointment', 'error')
    
    return redirect(url_for('hospital.view_appointment', app_id=app_id))

@hospital_bp.route('/appointment/<int:app_id>/cancel', methods=['POST'])
@role_required('hospital')
def cancel_appointment(app_id):
    """Cancel appointment"""
    reason = request.form.get('reason', '')
    
    from app.models import ServiceApplication
    if ServiceApplication.update_status(app_id, 'cancelled', reason):
        flash('Appointment cancelled', 'success')
    else:
        flash('Failed to cancel appointment', 'error')
    
    return redirect(url_for('hospital.view_appointment', app_id=app_id))
