from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import User, Database, Complaint
from app.utils import role_required, paginate, hash_password
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@role_required('admin', 'superadmin')
def dashboard():
    """Admin dashboard"""
    # Get system statistics
    users = Database.execute_query("SELECT * FROM users") or []
    applications = Database.execute_query("SELECT * FROM service_applications") or []
    complaints = Database.execute_query("SELECT * FROM complaints") or []
    
    stats = {
        'total_users': len(users),
        'citizens': sum(1 for u in users if u['role'] == 'citizen'),
        'staff': sum(1 for u in users if u['role'] != 'citizen'),
        'total_applications': len(applications),
        'pending_applications': sum(1 for a in applications if a['status'] == 'pending'),
        'total_complaints': len(complaints),
        'pending_complaints': sum(1 for c in complaints if c['status'] == 'pending')
    }
    
    recent_users = users[-5:] if users else []
    recent_apps = applications[-5:] if applications else []
    
    return render_template('admin/dashboard.html', stats=stats, recent_users=recent_users, recent_apps=recent_apps)

@admin_bp.route('/users')
@role_required('admin', 'superadmin')
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '')
    
    query = "SELECT * FROM users"
    
    if role_filter:
        query += f" WHERE role='{role_filter}'"
    
    query += " ORDER BY created_at DESC"
    
    all_users = Database.execute_query(query) or []
    total = len(all_users)
    
    paginated = paginate(all_users, total, page)
    
    return render_template('admin/users.html', paginated=paginated, role_filter=role_filter)

@admin_bp.route('/user/<int:user_id>')
@role_required('admin', 'superadmin')
def view_user(user_id):
    """View user details"""
    user = User.get_by_id(user_id)
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.users'))
    
    if user['role'] == 'citizen':
        apps = Database.execute_query(
            "SELECT * FROM service_applications WHERE user_id=%s",
            (user_id,)
        ) or []
    else:
        apps = []
    
    return render_template('admin/user_details.html', user=user, applications=apps)

@admin_bp.route('/user/<int:user_id>/edit', methods=['POST'])
@role_required('superadmin')
def edit_user(user_id):
    """Edit user"""
    data = {
        'name': request.form.get('name', ''),
        'email': request.form.get('email', ''),
        'phone': request.form.get('phone', ''),
        'role': request.form.get('role', 'citizen'),
        'updated_at': datetime.now()
    }
    
    if User.update_user(user_id, data):
        flash('User updated successfully', 'success')
    else:
        flash('Failed to update user', 'error')
    
    return redirect(url_for('admin.view_user', user_id=user_id))

@admin_bp.route('/user/<int:user_id>/reset-password', methods=['POST'])
@role_required('superadmin')
def reset_password(user_id):
    """Reset user password"""
    new_password = request.form.get('new_password', '')
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters', 'error')
        return redirect(url_for('admin.view_user', user_id=user_id))
    
    if User.update_user(user_id, {'password': hash_password(new_password)}):
        flash('Password reset successfully', 'success')
    else:
        flash('Failed to reset password', 'error')
    
    return redirect(url_for('admin.view_user', user_id=user_id))

@admin_bp.route('/user/<int:user_id>/deactivate', methods=['POST'])
@role_required('superadmin')
def deactivate_user(user_id):
    """Deactivate user"""
    if User.update_user(user_id, {'is_active': 0}):
        flash('User deactivated successfully', 'success')
    else:
        flash('Failed to deactivate user', 'error')
    
    return redirect(url_for('admin.view_user', user_id=user_id))

@admin_bp.route('/complaints')
@role_required('admin', 'superadmin')
def complaints():
    """View all complaints"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = "SELECT * FROM complaints"
    
    if status_filter:
        query += f" WHERE status='{status_filter}'"
    
    query += " ORDER BY created_at DESC"
    
    all_complaints = Database.execute_query(query) or []
    total = len(all_complaints)
    
    paginated = paginate(all_complaints, total, page)
    
    return render_template('admin/complaints.html', paginated=paginated, status_filter=status_filter)

@admin_bp.route('/complaint/<int:complaint_id>')
@role_required('admin', 'superadmin')
def view_complaint(complaint_id):
    """View complaint details"""
    complaint = Complaint.get_by_id(complaint_id)
    
    if not complaint:
        flash('Complaint not found', 'error')
        return redirect(url_for('admin.complaints'))
    
    user = User.get_by_id(complaint['user_id'])
    
    return render_template('admin/complaint_details.html', complaint=complaint, user=user)

@admin_bp.route('/complaint/<int:complaint_id>/resolve', methods=['POST'])
@role_required('admin', 'superadmin')
def resolve_complaint(complaint_id):
    """Resolve complaint"""
    resolution = request.form.get('resolution', '')
    
    if Complaint.update_status(complaint_id, 'resolved'):
        flash('Complaint marked as resolved', 'success')
    else:
        flash('Failed to resolve complaint', 'error')
    
    return redirect(url_for('admin.view_complaint', complaint_id=complaint_id))

@admin_bp.route('/audit-logs')
@role_required('superadmin')
def audit_logs():
    """View audit logs"""
    page = request.args.get('page', 1, type=int)
    
    logs = Database.execute_query(
        "SELECT * FROM audit_logs ORDER BY created_at DESC"
    ) or []
    
    total = len(logs)
    paginated = paginate(logs, total, page)
    
    return render_template('admin/audit_logs.html', paginated=paginated)
