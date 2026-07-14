from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import Database, ServiceApplication
from app.utils import role_required, paginate
from datetime import datetime

city_corp_bp = Blueprint('city_corp', __name__, url_prefix='/city-corp')

@city_corp_bp.route('/dashboard')
@role_required('city_corp')
def dashboard():
    """City Corporation dashboard"""
    # Get license and permit statistics
    apps = Database.execute_query(
        "SELECT * FROM service_applications WHERE service_type IN ('trade_license', 'building_permit')"
    ) or []
    
    stats = {
        'total_applications': len(apps),
        'pending': sum(1 for app in apps if app['status'] == 'pending'),
        'approved': sum(1 for app in apps if app['status'] == 'approved'),
        'rejected': sum(1 for app in apps if app['status'] == 'rejected')
    }
    
    recent_apps = apps[:5]
    
    return render_template('city_corp/dashboard.html', stats=stats, recent_apps=recent_apps)

@city_corp_bp.route('/applications')
@role_required('city_corp')
def applications():
    """View city corp applications"""
    page = request.args.get('page', 1, type=int)
    service_filter = request.args.get('service', '')
    status_filter = request.args.get('status', '')
    
    query = "SELECT * FROM service_applications WHERE service_type IN ('trade_license', 'building_permit')"
    
    if service_filter:
        query += f" AND service_type='{service_filter}'"
    
    if status_filter:
        query += f" AND status='{status_filter}'"
    
    query += " ORDER BY created_at DESC"
    
    apps = Database.execute_query(query) or []
    total = len(apps)
    
    paginated = paginate(apps, total, page)
    
    return render_template('city_corp/applications.html', paginated=paginated, service_filter=service_filter, status_filter=status_filter)

@city_corp_bp.route('/application/<int:app_id>')
@role_required('city_corp')
def view_application(app_id):
    """View application details"""
    app = ServiceApplication.get_by_id(app_id)
    
    if not app:
        flash('Application not found', 'error')
        return redirect(url_for('city_corp.applications'))
    
    from app.models import User
    user = User.get_by_id(app['user_id'])
    
    return render_template('city_corp/application_details.html', application=app, user=user)

@city_corp_bp.route('/application/<int:app_id>/approve', methods=['POST'])
@role_required('city_corp')
def approve_application(app_id):
    """Approve application"""
    remarks = request.form.get('remarks', '')
    
    if ServiceApplication.update_status(app_id, 'approved', remarks):
        flash('Application approved', 'success')
    else:
        flash('Failed to approve application', 'error')
    
    return redirect(url_for('city_corp.view_application', app_id=app_id))

@city_corp_bp.route('/application/<int:app_id>/reject', methods=['POST'])
@role_required('city_corp')
def reject_application(app_id):
    """Reject application"""
    remarks = request.form.get('remarks', '')
    
    if ServiceApplication.update_status(app_id, 'rejected', remarks):
        flash('Application rejected', 'success')
    else:
        flash('Failed to reject application', 'error')
    
    return redirect(url_for('city_corp.view_application', app_id=app_id))

@city_corp_bp.route('/application/<int:app_id>/request-info', methods=['POST'])
@role_required('city_corp')
def request_info(app_id):
    """Request additional information"""
    info_needed = request.form.get('info_needed', '')
    
    if ServiceApplication.update_status(app_id, 'info_requested', info_needed):
        flash('Information requested from applicant', 'success')
    else:
        flash('Failed to request information', 'error')
    
    return redirect(url_for('city_corp.view_application', app_id=app_id))
