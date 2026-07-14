import os
import MySQLdb
from config import Config

def init_database():
    """Initialize the database with required tables"""
    
    # SQL statements to create tables
    sql_statements = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL,
            nid VARCHAR(20) UNIQUE NOT NULL,
            address TEXT,
            password VARCHAR(255) NOT NULL,
            role ENUM('citizen', 'police', 'hospital', 'city_corp', 'blood_bank', 'admin', 'superadmin') DEFAULT 'citizen',
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_email (email),
            INDEX idx_role (role)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS service_applications (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            service_type VARCHAR(50) NOT NULL,
            description TEXT,
            document_path VARCHAR(255),
            status ENUM('pending', 'approved', 'rejected', 'completed', 'cancelled', 'info_requested') DEFAULT 'pending',
            remarks TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            INDEX idx_user_id (user_id),
            INDEX idx_service_type (service_type),
            INDEX idx_status (status)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS complaints (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            category VARCHAR(50),
            status ENUM('pending', 'in_progress', 'resolved', 'closed') DEFAULT 'pending',
            priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
            assigned_to INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            INDEX idx_user_id (user_id),
            INDEX idx_status (status)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            message TEXT,
            type VARCHAR(50),
            is_read BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            INDEX idx_user_id (user_id),
            INDEX idx_is_read (is_read)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            action VARCHAR(255) NOT NULL,
            entity_type VARCHAR(50),
            entity_id INT,
            details TEXT,
            ip_address VARCHAR(45),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_created_at (created_at)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS blood_inventory (
            id INT PRIMARY KEY AUTO_INCREMENT,
            blood_type VARCHAR(5) NOT NULL,
            quantity INT DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY unique_blood_type (blood_type)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS departments (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            head_id INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (head_id) REFERENCES users(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS service_requests (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            service_type VARCHAR(50) NOT NULL,
            status ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending',
            priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id),
            INDEX idx_user_id (user_id),
            INDEX idx_status (status)
        )
        """,
    ]
    
    try:
        conn = MySQLdb.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            passwd=Config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.select_db(Config.MYSQL_DB)
        
        # Create tables
        for sql in sql_statements:
            cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Database initialized successfully!")
        return True
    
    except MySQLdb.Error as e:
        print(f"Database initialization error: {e}")
        return False

if __name__ == '__main__':
    init_database()
