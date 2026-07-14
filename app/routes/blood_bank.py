from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import Database, ServiceApplication
from app.utils import role_required, paginate
from datetime import datetime

blood_bank_bp = Blueprint('blood_bank', __name__, url_prefix='/blood-bank')

@blood_bank_bp.route('/dashboard')
@role_required('blood_bank')
def dashboard():
    """Blood Bank dashboard"""
    # Get blood donation statistics
    apps = Database.execute_query(
        "SELECT * FROM service_applications WHERE service_type='blood_donation'"
    ) or []
    
    stats = {
        'total_requests': len(apps),
        'pending': sum(1 for app in apps if app['status'] == 'pending'),
        'completed': sum(1 for app in apps if app['status'] == 'completed'),
        'cancelled': sum(1 for app in apps if app['status'] == 'cancelled')
    }
    
    recent_apps = apps[:5]
    
    return render_template('blood_bank/dashboard.html', stats=stats, recent_apps=recent_apps)

@blood_bank_bp.route('/requests')
@role_required('blood_bank')
def requests():
    """View blood donation requests"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    blood_type_filter = request.args.get('blood_type', '')
    
    query = "SELECT * FROM service_applications WHERE service_type='blood_donation'"
    
    if status_filter:
        query += f" AND status='{status_filter}'"
    
    if blood_type_filter:
        query += f" AND description LIKE '%{blood_type_filter}%'"
    
    query += " ORDER BY created_at DESC"
    
    apps = Database.execute_query(query) or []
    total = len(apps)
    
    paginated = paginate(apps, total, page)
    
    return render_template('blood_bank/requests.html', paginated=paginated, status_filter=status_filter, blood_type_filter=blood_type_filter)

@blood_bank_bp.route('/request/<int:app_id>')
@role_required('blood_bank')
def view_request(app_id):
    """View blood donation request details"""
    app = ServiceApplication.get_by_id(app_id)
    
    if not app:
        flash('Request not found', 'error')
        return redirect(url_for('blood_bank.requests'))
    
    from app.models import User
    user = User.get_by_id(app['user_id'])
    
    return render_template('blood_bank/request_details.html', application=app, user=user)

@blood_bank_bp.route('/request/<int:app_id>/fulfill', methods=['POST'])
@role_required('blood_bank')
def fulfill_request(app_id):
    """Fulfill blood donation request"""
    notes = request.form.get('notes', '')
    
    if ServiceApplication.update_status(app_id, 'completed', notes):
        flash('Blood donation request fulfilled', 'success')
    else:
        flash('Failed to fulfill request', 'error')
    
    return redirect(url_for('blood_bank.view_request', app_id=app_id))

@blood_bank_bp.route('/request/<int:app_id>/cancel', methods=['POST'])
@role_required('blood_bank')
def cancel_request(app_id):
    """Cancel blood donation request"""
    reason = request.form.get('reason', '')
    
    if ServiceApplication.update_status(app_id, 'cancelled', reason):
        flash('Blood donation request cancelled', 'success')
    else:
        flash('Failed to cancel request', 'error')
    
    return redirect(url_for('blood_bank.view_request', app_id=app_id))
