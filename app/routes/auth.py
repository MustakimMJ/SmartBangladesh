from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import User, Database
from app.utils import hash_password, verify_password, login_required
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        nid = request.form.get('nid', '').strip()
        address = request.form.get('address', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = 'citizen'  # Default role
        
        # Validation
        errors = []
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Invalid email format')
        if not phone or len(phone) < 10:
            errors.append('Valid phone number required')
        if not nid or len(nid) < 10:
            errors.append('Valid NID required')
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters')
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if user already exists
        if not errors:
            existing = User.get_by_email(email)
            if existing:
                errors.append('Email already registered')
            
            existing = User.get_by_phone(phone)
            if existing:
                errors.append('Phone number already registered')
        
        if errors:
            return render_template('auth/register.html', errors=errors), 400
        
        # Create user
        user_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'nid': nid,
            'address': address,
            'password': hash_password(password),
            'role': role,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        user_id = User.create(user_data)
        if user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/login.html'), 400
        
        user = User.get_by_email(email)
        if user and verify_password(password, user['password']):
            # Set session
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            session['role'] = user['role']
            session.permanent = True
            
            # Redirect based on role
            if user['role'] == 'citizen':
                return redirect(url_for('citizen.dashboard'))
            elif user['role'] == 'police':
                return redirect(url_for('police.dashboard'))
            elif user['role'] == 'hospital':
                return redirect(url_for('hospital.dashboard'))
            elif user['role'] == 'city_corp':
                return redirect(url_for('city_corp.dashboard'))
            elif user['role'] == 'blood_bank':
                return redirect(url_for('blood_bank.dashboard'))
            else:  # admin/superadmin
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('auth/login.html'), 401
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """View user profile"""
    user = User.get_by_id(session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/profile.html', user=user)

@auth_bp.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    user_id = session['user_id']
    
    data = {
        'name': request.form.get('name', ''),
        'address': request.form.get('address', ''),
        'phone': request.form.get('phone', ''),
        'updated_at': datetime.now()
    }
    
    if User.update_user(user_id, data):
        session['name'] = data['name']
        flash('Profile updated successfully', 'success')
    else:
        flash('Failed to update profile', 'error')
    
    return redirect(url_for('auth.profile'))

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    user_id = session['user_id']
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.profile'))
    
    if not verify_password(old_password, user['password']):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('auth.profile'))
    
    if len(new_password) < 6:
        flash('New password must be at least 6 characters', 'error')
        return redirect(url_for('auth.profile'))
    
    if new_password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('auth.profile'))
    
    if User.update_user(user_id, {'password': hash_password(new_password)}):
        flash('Password changed successfully', 'success')
    else:
        flash('Failed to change password', 'error')
    
    return redirect(url_for('auth.profile'))
