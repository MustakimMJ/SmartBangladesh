import os
from flask import Flask, render_template
from config import config
from app.models import Database

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Configuration
    app.config.from_object(config[config_name])
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.citizen import citizen_bp
    from app.routes.police import police_bp
    from app.routes.hospital import hospital_bp
    from app.routes.city_corp import city_corp_bp
    from app.routes.blood_bank import blood_bank_bp
    from app.routes.admin import admin_bp
    from app.routes.certificate import certificate_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(police_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(city_corp_bp)
    app.register_blueprint(blood_bank_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(certificate_bp)
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/services')
    def services():
        return render_template('services.html')
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', message='Page not found'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return render_template('error.html', message='Server error'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error.html', message='Access forbidden'), 403
    
    # Context processors
    @app.context_processor
    def inject_user():
        from flask import session
        return dict(
            user_id=session.get('user_id'),
            user_name=session.get('name'),
            user_role=session.get('role')
        )
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
