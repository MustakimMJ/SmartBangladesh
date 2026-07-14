from flask import Blueprint, render_template, session, redirect, url_for, flash, send_file, request
from app.models import Database, ServiceApplication, User
from app.utils_pdf import generate_certificate_pdf
from datetime import datetime

certificate_bp = Blueprint('certificate', __name__)

SERVICE_CODES = {
    'birth_certificate': 'BC',
    'death_certificate': 'DC',
    'family_certificate': 'FC',
    'police_clearance': 'PC'
}

REV_SERVICE_CODES = {v: k for k, v in SERVICE_CODES.items()}

def get_certificate_id(application):
    code = SERVICE_CODES.get(application['service_type'], 'GEN')
    return f"SB-{code}-{application['id']:06d}"

@certificate_bp.route('/certificate/<int:app_id>')
def view_certificate(app_id):
    """View certificate page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    app = ServiceApplication.get_by_id(app_id)
    if not app:
        flash('Certificate not found', 'error')
        return redirect(url_for('index'))
        
    if app['status'] != 'approved':
        flash('Certificate is not available or not yet approved', 'error')
        return redirect(url_for('index'))
        
    # Access checks
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    if user_role == 'citizen' and app['user_id'] != user_id:
        flash('Access Denied', 'error')
        return redirect(url_for('index'))
        
    user = User.get_by_id(app['user_id'])
    cert_id = get_certificate_id(app)
    
    return render_template('certificate/view.html', application=app, user=user, cert_id=cert_id)

@certificate_bp.route('/certificate/<int:app_id>/pdf')
def download_certificate_pdf(app_id):
    """Download certificate in PDF format"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    app = ServiceApplication.get_by_id(app_id)
    if not app or app['status'] != 'approved':
        flash('Certificate not available', 'error')
        return redirect(url_for('index'))
        
    # Access checks
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    if user_role == 'citizen' and app['user_id'] != user_id:
        flash('Access Denied', 'error')
        return redirect(url_for('index'))
        
    user = User.get_by_id(app['user_id'])
    cert_id = get_certificate_id(app)
    
    pdf_buffer = generate_certificate_pdf(app, user, cert_id)
    
    return send_file(
        pdf_buffer,
        download_name=f"{cert_id}.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

@certificate_bp.route('/verify/<cert_id>')
def verify_certificate(cert_id):
    """Public certificate verification page"""
    verified = False
    app = None
    user = None
    
    try:
        if cert_id.startswith('SB-') and '-' in cert_id:
            parts = cert_id.split('-')
            if len(parts) == 3:
                _, code, app_id_str = parts
                app_id = int(app_id_str)
                
                app = ServiceApplication.get_by_id(app_id)
                if app and app['status'] == 'approved':
                    expected_code = SERVICE_CODES.get(app['service_type'])
                    if expected_code == code:
                        user = User.get_by_id(app['user_id'])
                        verified = True
    except Exception as e:
        print(f"Verification parsing error: {e}")
        verified = False
        
    return render_template('certificate/verify.html', verified=verified, application=app, user=user, cert_id=cert_id)
