# Smart Bangladesh - Digital Services Platform

A comprehensive Flask-based web application providing digital government services to citizens of Bangladesh.

## Features

- **Multi-role Authentication**: Citizen, Police, Hospital, City Corporation, Blood Bank, Admin, Superadmin
- **Citizen Services**: 
  - Birth Certificate Application
  - Death Certificate Application
  - Family Certificate Application
  - Police Clearance Request
- **Police Portal**: Manage clearance applications
- **Hospital Portal**: Manage healthcare appointments
- **City Corporation Portal**: Manage trade licenses and building permits
- **Blood Bank Portal**: Manage blood donation requests
- **Admin Dashboard**: User management, complaint handling, audit logs
- **Responsive Design**: Mobile-friendly interface
- **File Upload**: Support for document uploads (PDF, DOC, JPG, PNG)

## Requirements

- Python 3.7+
- MySQL/MariaDB
- Flask 2.3.3
- MySQLdb 1.0.1

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-bangladesh
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your database credentials:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DB=smart_bangladesh
```

### 5. Initialize Database

```bash
python init_db.py
```

### 6. Run the Application

```bash
python app.py
```

The application will be accessible at `http://localhost:5000`

## Project Structure

```
smart-bangladesh/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── init_db.py            # Database initialization
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
│
├── app/
│   ├── models.py         # Database models
│   ├── utils.py          # Utility functions
│   └── routes/
│       ├── auth.py       # Authentication routes
│       ├── citizen.py    # Citizen portal routes
│       ├── police.py     # Police portal routes
│       ├── hospital.py   # Hospital portal routes
│       ├── city_corp.py  # City corporation routes
│       ├── blood_bank.py # Blood bank routes
│       └── admin.py      # Admin routes
│
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── auth/             # Authentication templates
│   ├── citizen/          # Citizen portal templates
│   ├── police/           # Police portal templates
│   ├── hospital/         # Hospital portal templates
│   ├── city_corp/        # City corporation templates
│   ├── blood_bank/       # Blood bank templates
│   └── admin/            # Admin templates
│
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet
    ├── js/
    │   └── main.js       # JavaScript functionality
    └── uploads/          # User-uploaded files
```

## User Roles and Access

### Citizen
- View dashboard with application statistics
- Apply for services (birth certificate, death certificate, etc.)
- Track application status
- Download approved documents
- Update profile

### Police Officer
- View pending clearance applications
- Approve or reject applications
- Add remarks/comments
- Track processed applications

### Hospital Staff
- View healthcare appointments
- Mark appointments as completed
- Cancel appointments
- Add medical notes

### City Corporation
- Manage trade license applications
- Manage building permit applications
- Request additional information
- Approve/reject applications

### Blood Bank
- View blood donation requests
- Fulfill donation requests
- Cancel requests
- Track request history

### Admin
- Manage all users
- View system statistics
- Handle complaints
- Monitor applications
- Audit logs

### Superadmin
- Full system access
- Reset user passwords
- Deactivate users
- View all audit logs

## Default Credentials

To set up initial admin users, use the user registration form and manually update the `role` field in the database.

## Database Schema

### Main Tables
- **users**: User accounts and authentication
- **service_applications**: Service applications and requests
- **complaints**: Citizen complaints
- **notifications**: System notifications
- **audit_logs**: System activity logs
- **blood_inventory**: Blood bank inventory
- **departments**: Government departments
- **service_requests**: Service requests tracking

## Security Features

- Password hashing (SHA-256)
- Session-based authentication
- Role-based access control
- File upload validation
- SQL injection prevention (parameterized queries)
- CSRF protection ready
- Secure password reset

## API Response Codes

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Development Notes

### Adding New Services

1. Create a service application form in the citizen portal
2. Add database table for service-specific data
3. Create approval workflow route
4. Add notification system for status updates

### Customization

- Colors and branding: Edit `static/css/style.css`
- Email templates: Add in templates directory
- Database fields: Modify `init_db.py`
- Routes: Add new blueprints in `app/routes/`

## Troubleshooting

### Database Connection Error
- Verify MySQL/MariaDB is running
- Check credentials in `.env` file
- Ensure database exists

### File Upload Issues
- Check `static/uploads/` directory permissions
- Verify file type in ALLOWED_EXTENSIONS
- Check file size limits in config

### Session Errors
- Clear browser cookies
- Check SECRET_KEY in .env
- Verify session configuration

## Production Deployment

Before deploying to production:

1. Change `FLASK_ENV` to `production`
2. Set a strong `SECRET_KEY`
3. Use HTTPS (set `SESSION_COOKIE_SECURE=True`)
4. Configure proper MYSQL credentials
5. Set up proper logging
6. Use a production WSGI server (Gunicorn, uWSGI)
7. Configure reverse proxy (Nginx, Apache)

## Contributing

1. Create feature branches
2. Follow PEP 8 style guide
3. Add tests for new features
4. Submit pull requests

## License

This project is part of the Smart Bangladesh initiative.

## Support

For support, contact: info@smartbangladesh.gov.bd

---

**Last Updated**: June 2024
