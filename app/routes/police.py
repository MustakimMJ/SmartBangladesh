from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import User, ServiceApplication, Database
from app.utils import role_required, format_date, paginate
from datetime import datetime

police_bp = Blueprint('police', __name__, url_prefix='/police')

@police_bp.route('/dashboard')
@role_required('police')
def dashboard():
    """Police dashboard"""
    # Get clearance statistics
    apps = Database.execute_query(
        "SELECT * FROM service_applications WHERE service_type='police_clearance'"
    ) or []
    
    stats = {
        'total_applications': len(apps),
        'pending': sum(1 for app in apps if app['status'] == 'pending'),
        'approved': sum(1 for app in apps if app['status'] == 'approved'),
        'rejected': sum(1 for app in apps if app['status'] == 'rejected')
    }
    
    recent_apps = apps[:5]
    
    return render_template('police/dashboard.html', stats=stats, recent_apps=recent_apps)

@police_bp.route('/applications')
@role_required('police')
def applications():
    """View police clearance applications"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = "SELECT * FROM service_applications WHERE service_type='police_clearance'"
    
    if status_filter:
        query += f" AND status='{status_filter}'"
    
    query += " ORDER BY created_at DESC"
    
    apps = Database.execute_query(query) or []
    total = len(apps)
    
    paginated = paginate(apps, total, page)
    
    return render_template('police/applications.html', paginated=paginated, status_filter=status_filter)

@police_bp.route('/application/<int:app_id>')
@role_required('police')
def view_application(app_id):
    """View application details"""
    app = ServiceApplication.get_by_id(app_id)
    
    if not app:
        flash('Application not found', 'error')
        return redirect(url_for('police.applications'))
    
    user = User.get_by_id(app['user_id'])
    
    return render_template('police/application_details.html', application=app, user=user)

@police_bp.route('/application/<int:app_id>/approve', methods=['POST'])
@role_required('police')
def approve_application(app_id):
    """Approve clearance application"""
    remarks = request.form.get('remarks', '')
    
    if ServiceApplication.update_status(app_id, 'approved', remarks):
        flash('Application approved', 'success')
    else:
        flash('Failed to approve application', 'error')
    
    return redirect(url_for('police.view_application', app_id=app_id))

@police_bp.route('/application/<int:app_id>/reject', methods=['POST'])
@role_required('police')
def reject_application(app_id):
    """Reject clearance application"""
    remarks = request.form.get('remarks', '')
    
    if ServiceApplication.update_status(app_id, 'rejected', remarks):
        flash('Application rejected', 'success')
    else:
        flash('Failed to reject application', 'error')
    
    return redirect(url_for('police.view_application', app_id=app_id))
