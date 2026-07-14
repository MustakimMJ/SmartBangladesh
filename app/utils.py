import hashlib
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import session, redirect, url_for, render_template

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return hash_password(password) == hashed

def allowed_file(filename):
    """Check if file extension is allowed"""
    from config import Config
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """Save uploaded file and return filename"""
    from config import Config
    from werkzeug.utils import secure_filename
    
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    # Create uploads directory if it doesn't exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = secure_filename(file.filename)
    filename = timestamp + filename
    
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return filename

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role')
            if user_role not in roles:
                return render_template('error.html', message='Access Denied'), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def format_date(date_str):
    """Format date string"""
    if isinstance(date_str, str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except:
            return date_str
    else:
        date_obj = date_str
    
    return date_obj.strftime('%d %b %Y')

def format_datetime(datetime_str):
    """Format datetime string"""
    if isinstance(datetime_str, str):
        try:
            dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except:
            return datetime_str
    else:
        dt_obj = datetime_str
    
    return dt_obj.strftime('%d %b %Y, %I:%M %p')

def get_status_badge(status):
    """Get HTML badge for status"""
    badge_map = {
        'pending': '<span class="badge badge-warning">Pending</span>',
        'approved': '<span class="badge badge-success">Approved</span>',
        'rejected': '<span class="badge badge-danger">Rejected</span>',
        'processing': '<span class="badge badge-info">Processing</span>',
        'completed': '<span class="badge badge-success">Completed</span>',
        'cancelled': '<span class="badge badge-secondary">Cancelled</span>',
    }
    return badge_map.get(status, f'<span class="badge badge-secondary">{status}</span>')

def paginate(query_results, total_count, page, per_page=10):
    """Calculate pagination info"""
    total_pages = (total_count + per_page - 1) // per_page
    offset = (page - 1) * per_page
    
    return {
        'records': query_results,
        'total_count': total_count,
        'current_page': page,
        'total_pages': total_pages,
        'per_page': per_page,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None,
    }
