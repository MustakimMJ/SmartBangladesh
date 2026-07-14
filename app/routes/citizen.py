from flask import Blueprint, render_template, request, session, redirect, url_for, flash, send_file
from app.models import User, ServiceApplication, Database
from app.utils import login_required, role_required, save_uploaded_file, format_date, paginate
from datetime import datetime
import os

citizen_bp = Blueprint('citizen', __name__, url_prefix='/citizen')

@citizen_bp.route('/dashboard')
@role_required('citizen')
def dashboard():
    """Citizen dashboard"""
    user_id = session['user_id']
    
    # Get user stats
    apps = ServiceApplication.get_by_user(user_id)
    
    stats = {
        'total_applications': len(apps),
        'pending': sum(1 for app in apps if app['status'] == 'pending'),
        'approved': sum(1 for app in apps if app['status'] == 'approved'),
        'rejected': sum(1 for app in apps if app['status'] == 'rejected')
    }
    
    # Get recent applications
    recent_apps = apps[:5]
    
    return render_template('citizen/dashboard.html', stats=stats, recent_apps=recent_apps)

@citizen_bp.route('/applications')
@role_required('citizen')
def applications():
    """View all applications"""
    user_id = session['user_id']
    page = request.args.get('page', 1, type=int)
    
    apps = ServiceApplication.get_by_user(user_id)
    total = len(apps)
    
    paginated = paginate(apps, total, page)
    
    return render_template('citizen/applications.html', paginated=paginated)

@citizen_bp.route('/apply/<service_type>', methods=['GET', 'POST'])
@role_required('citizen')
def apply_service(service_type):
    """Apply for a service"""
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    
    valid_services = ['birth_certificate', 'death_certificate', 'family_certificate', 'police_clearance']
    
    if service_type not in valid_services:
        flash('Invalid service type', 'error')
        return redirect(url_for('citizen.applications'))
    
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        file = request.files.get('document')
        
        errors = []
        if not description:
            errors.append('Description is required')
        
        filename = None
        if file:
            filename = save_uploaded_file(file)
            if not filename:
                errors.append('Invalid file type or size')
        
        if errors:
            return render_template(f'citizen/apply_{service_type}.html', errors=errors, user=user), 400
        
        app_data = {
            'user_id': user_id,
            'service_type': service_type,
            'description': description,
            'document_path': filename,
            'status': 'pending',
            'remarks': '',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        if ServiceApplication.create(app_data):
            flash(f'Application for {service_type.replace("_", " ")} submitted successfully', 'success')
            return redirect(url_for('citizen.applications'))
        else:
            flash('Failed to submit application', 'error')
    
    return render_template(f'citizen/apply_{service_type}.html', user=user)

@citizen_bp.route('/application/<int:app_id>')
@role_required('citizen')
def view_application(app_id):
    """View application details"""
    app = ServiceApplication.get_by_id(app_id)
    
    if not app or app['user_id'] != session['user_id']:
        flash('Application not found', 'error')
        return redirect(url_for('citizen.applications'))
    
    return render_template('citizen/application_details.html', application=app)

@citizen_bp.route('/download/<int:app_id>')
@role_required('citizen')
def download_document(app_id):
    """Download application document"""
    app = ServiceApplication.get_by_id(app_id)
    
    if not app or app['user_id'] != session['user_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('citizen.applications'))
    
    if not app['document_path']:
        flash('No document available', 'error')
        return redirect(url_for('citizen.view_application', app_id=app_id))
    
    from config import Config
    filepath = os.path.join(Config.UPLOAD_FOLDER, app['document_path'])
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('Document not found', 'error')
        return redirect(url_for('citizen.view_application', app_id=app_id))
