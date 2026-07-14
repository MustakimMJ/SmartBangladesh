import MySQLdb
from config import Config
from datetime import datetime

class Database:
    """Database connection manager"""
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        try:
            conn = MySQLdb.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                passwd=Config.MYSQL_PASSWORD,
                db=Config.MYSQL_DB,
                charset='utf8mb4'
            )
            return conn
        except MySQLdb.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None):
        """Execute a query and return results"""
        conn = Database.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # If SELECT query
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                conn.close()
                return results
            else:
                conn.commit()
                conn.close()
                return True
        except MySQLdb.Error as e:
            print(f"Query execution error: {e}")
            conn.close()
            return None
    
    @staticmethod
    def insert(table, data):
        """Insert a record"""
        conn = Database.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(data.values()))
            conn.commit()
            insert_id = cursor.lastrowid
            conn.close()
            return insert_id
        except MySQLdb.Error as e:
            print(f"Insert error: {e}")
            conn.close()
            return None
    
    @staticmethod
    def update(table, data, where_clause):
        """Update records"""
        conn = Database.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            set_clause = ', '.join([f"{k}=%s" for k in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            cursor.execute(query, tuple(data.values()))
            conn.commit()
            conn.close()
            return True
        except MySQLdb.Error as e:
            print(f"Update error: {e}")
            conn.close()
            return False
    
    @staticmethod
    def delete(table, where_clause):
        """Delete records"""
        conn = Database.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = f"DELETE FROM {table} WHERE {where_clause}"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return True
        except MySQLdb.Error as e:
            print(f"Delete error: {e}")
            conn.close()
            return False

class User:
    """User model"""
    
    @staticmethod
    def create(user_data):
        """Create a new user"""
        return Database.insert('users', user_data)
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        results = Database.execute_query(
            "SELECT * FROM users WHERE id=%s",
            (user_id,)
        )
        return results[0] if results else None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        results = Database.execute_query(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )
        return results[0] if results else None
    
    @staticmethod
    def get_by_phone(phone):
        """Get user by phone"""
        results = Database.execute_query(
            "SELECT * FROM users WHERE phone=%s",
            (phone,)
        )
        return results[0] if results else None
    
    @staticmethod
    def update_user(user_id, data):
        """Update user data"""
        return Database.update('users', data, f"id={user_id}")
    
    @staticmethod
    def get_all_by_role(role):
        """Get all users by role"""
        results = Database.execute_query(
            "SELECT * FROM users WHERE role=%s ORDER BY created_at DESC",
            (role,)
        )
        return results if results else []

class ServiceApplication:
    """Service Application model"""
    
    @staticmethod
    def create(app_data):
        """Create a new service application"""
        return Database.insert('service_applications', app_data)
    
    @staticmethod
    def get_by_id(app_id):
        """Get application by ID"""
        results = Database.execute_query(
            "SELECT * FROM service_applications WHERE id=%s",
            (app_id,)
        )
        return results[0] if results else None
    
    @staticmethod
    def get_by_user(user_id):
        """Get all applications by user"""
        results = Database.execute_query(
            "SELECT * FROM service_applications WHERE user_id=%s ORDER BY created_at DESC",
            (user_id,)
        )
        return results if results else []
    
    @staticmethod
    def update_status(app_id, status, remarks=''):
        """Update application status"""
        data = {'status': status}
        if remarks:
            data['remarks'] = remarks
        data['updated_at'] = datetime.now()
        return Database.update('service_applications', data, f"id={app_id}")

class Complaint:
    """Complaint model"""
    
    @staticmethod
    def create(complaint_data):
        """Create a new complaint"""
        return Database.insert('complaints', complaint_data)
    
    @staticmethod
    def get_by_id(complaint_id):
        """Get complaint by ID"""
        results = Database.execute_query(
            "SELECT * FROM complaints WHERE id=%s",
            (complaint_id,)
        )
        return results[0] if results else None
    
    @staticmethod
    def get_all(limit=50, offset=0):
        """Get all complaints with pagination"""
        results = Database.execute_query(
            "SELECT * FROM complaints ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (limit, offset)
        )
        return results if results else []
    
    @staticmethod
    def get_count():
        """Get total complaint count"""
        results = Database.execute_query("SELECT COUNT(*) as count FROM complaints")
        return results[0]['count'] if results else 0
    
    @staticmethod
    def update_status(complaint_id, status):
        """Update complaint status"""
        return Database.update('complaints', {'status': status}, f"id={complaint_id}")

class Notification:
    """Notification model"""
    
    @staticmethod
    def create(notif_data):
        """Create a new notification"""
        return Database.insert('notifications', notif_data)
    
    @staticmethod
    def get_by_user(user_id):
        """Get notifications for a user"""
        results = Database.execute_query(
            "SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC LIMIT 10",
            (user_id,)
        )
        return results if results else []
    
    @staticmethod
    def mark_as_read(notif_id):
        """Mark notification as read"""
        return Database.update('notifications', {'is_read': 1}, f"id={notif_id}")
