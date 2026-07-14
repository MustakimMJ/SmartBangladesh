-- ============================================================
-- Smart Bangladesh - Database Setup for phpMyAdmin
-- Import this file in phpMyAdmin (Import tab)
-- Default login password for ALL users below: Password123
-- ============================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET FOREIGN_KEY_CHECKS = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `smart_bangladesh`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `smart_bangladesh`;

-- Drop existing tables (reverse dependency order)
DROP TABLE IF EXISTS `service_requests`;
DROP TABLE IF EXISTS `departments`;
DROP TABLE IF EXISTS `blood_inventory`;
DROP TABLE IF EXISTS `audit_logs`;
DROP TABLE IF EXISTS `notifications`;
DROP TABLE IF EXISTS `complaints`;
DROP TABLE IF EXISTS `service_applications`;
DROP TABLE IF EXISTS `users`;

-- ------------------------------------------------------------
-- Tables
-- ------------------------------------------------------------

CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `nid` VARCHAR(20) NOT NULL,
  `address` TEXT DEFAULT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('citizen','police','hospital','city_corp','blood_bank','admin','superadmin') DEFAULT 'citizen',
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `nid` (`nid`),
  KEY `idx_email` (`email`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `service_applications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `service_type` VARCHAR(50) NOT NULL,
  `description` TEXT DEFAULT NULL,
  `document_path` VARCHAR(255) DEFAULT NULL,
  `status` ENUM('pending','approved','rejected','completed','cancelled','info_requested') DEFAULT 'pending',
  `remarks` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_service_type` (`service_type`),
  KEY `idx_status` (`status`),
  CONSTRAINT `service_applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `complaints` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT DEFAULT NULL,
  `category` VARCHAR(50) DEFAULT NULL,
  `status` ENUM('pending','in_progress','resolved','closed') DEFAULT 'pending',
  `priority` ENUM('low','medium','high') DEFAULT 'medium',
  `assigned_to` INT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `notifications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `message` TEXT DEFAULT NULL,
  `type` VARCHAR(50) DEFAULT NULL,
  `is_read` TINYINT(1) DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_is_read` (`is_read`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `audit_logs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT DEFAULT NULL,
  `action` VARCHAR(255) NOT NULL,
  `entity_type` VARCHAR(50) DEFAULT NULL,
  `entity_id` INT DEFAULT NULL,
  `details` TEXT DEFAULT NULL,
  `ip_address` VARCHAR(45) DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `blood_inventory` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `blood_type` VARCHAR(5) NOT NULL,
  `quantity` INT DEFAULT 0,
  `last_updated` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_blood_type` (`blood_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `departments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT DEFAULT NULL,
  `head_id` INT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `head_id` (`head_id`),
  CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`head_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `service_requests` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `service_type` VARCHAR(50) NOT NULL,
  `status` ENUM('pending','approved','rejected','completed') DEFAULT 'pending',
  `priority` ENUM('low','medium','high') DEFAULT 'medium',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `completed_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `service_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Users (password = Password123, SHA-256 hashed)
-- ------------------------------------------------------------

INSERT INTO `users` (`id`, `name`, `email`, `phone`, `nid`, `address`, `password`, `role`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Super Admin',        'superadmin@smartbangladesh.gov.bd', '01700000001', '1990000000001', 'Secretariat, Dhaka',           '008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'superadmin', 1, '2024-06-01 09:00:00', '2024-06-01 09:00:00'),
(2, 'System Admin',       'admin@smartbangladesh.gov.bd',      '01700000002', '1990000000002', 'ICT Division, Dhaka',          '008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'admin',      1, '2024-06-01 09:00:00', '2024-06-01 09:00:00'),
(3, 'Fatima Rahman',      'citizen@example.com',               '01711111111', '1991111111111', 'Mirpur, Dhaka',                '008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'citizen',    1, '2024-06-02 10:00:00', '2024-06-02 10:00:00'),
(4, 'Karim Ahmed',        'karim@example.com',                 '01722222222', '1992222222222', 'Chittagong',                   '008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'citizen',    1, '2024-06-02 11:00:00', '2024-06-02 11:00:00'),
(5, 'Inspector Rahim',    'police@smartbangladesh.gov.bd',     '01700000005', '1990000000005', 'Ramna Police Station, Dhaka',  '008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'police',     1, '2024-06-01 09:00:00', '2024-06-01 09:00:00'),
(6, 'Dr. Nasreen Hossain','hospital@smartbangladesh.gov.bd',   '01700000006', '1990000000006', 'Dhaka Medical College Hospital','008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'hospital',   1, '2024-06-01 09:00:00', '2024-06-01 09:00:00'),
(7, 'Officer Siddique',   'citycorp@smartbangladesh.gov.bd',   '01700000007', '1990000000007', 'DNCC Office, Gulshan',         '008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'city_corp',  1, '2024-06-01 09:00:00', '2024-06-01 09:00:00'),
(8, 'Manager Salma',      'bloodbank@smartbangladesh.gov.bd',  '01700000008', '1990000000008', 'Sandhani Blood Bank, Dhaka',   '008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601', 'blood_bank', 1, '2024-06-01 09:00:00', '2024-06-01 09:00:00');

-- ------------------------------------------------------------
-- Sample service applications (for all portals)
-- ------------------------------------------------------------

INSERT INTO `service_applications` (`id`, `user_id`, `service_type`, `description`, `document_path`, `status`, `remarks`, `created_at`, `updated_at`) VALUES
(1,  3, 'birth_certificate',      'Birth certificate for my son Ahmed Rahman, born 15 March 2024 at Dhaka Medical College.', NULL, 'pending',  NULL, '2024-06-03 10:00:00', '2024-06-03 10:00:00'),
(2,  3, 'death_certificate',      'Death certificate for my father Abdul Rahman, passed away 1 June 2024.', NULL, 'approved', 'Verified and approved.', '2024-06-04 11:00:00', '2024-06-05 14:00:00'),
(3,  4, 'family_certificate',     'Family certificate required for visa application to UAE.', NULL, 'pending', NULL, '2024-06-05 09:30:00', '2024-06-05 09:30:00'),
(4,  3, 'police_clearance',       'Police clearance certificate needed for overseas employment in Saudi Arabia.', NULL, 'pending', NULL, '2024-06-06 08:00:00', '2024-06-06 08:00:00'),
(5,  4, 'police_clearance',       'Police clearance for university scholarship abroad.', NULL, 'approved', 'No criminal record found.', '2024-06-07 10:00:00', '2024-06-08 16:00:00'),
(6,  3, 'healthcare_appointment', 'General checkup appointment for diabetes management. Preferred date: next Monday.', NULL, 'pending', NULL, '2024-06-08 14:00:00', '2024-06-08 14:00:00'),
(7,  4, 'healthcare_appointment', 'Cardiology consultation for chest pain symptoms.', NULL, 'completed', 'Patient seen and prescribed medication.', '2024-06-09 09:00:00', '2024-06-10 11:00:00'),
(8,  3, 'trade_license',          'New trade license for grocery shop at Mirpur-10, Block C.', NULL, 'pending', NULL, '2024-06-10 10:00:00', '2024-06-10 10:00:00'),
(9,  4, 'building_permit',        'Building permit for 3-storey residential building in Agrabad, Chittagong.', NULL, 'rejected', 'Incomplete structural drawings submitted.', '2024-06-11 11:00:00', '2024-06-12 15:00:00'),
(10, 3, 'blood_donation',         'Urgent blood needed: B+ type, 2 units for surgery at DMCH.', NULL, 'pending', NULL, '2024-06-12 07:00:00', '2024-06-12 07:00:00'),
(11, 4, 'blood_donation',         'Blood request: O- type, 1 unit for accident victim.', NULL, 'completed', 'Blood arranged from inventory.', '2024-06-13 08:00:00', '2024-06-13 12:00:00');

-- ------------------------------------------------------------
-- Sample complaints
-- ------------------------------------------------------------

INSERT INTO `complaints` (`id`, `user_id`, `title`, `description`, `category`, `status`, `priority`, `assigned_to`, `created_at`, `updated_at`) VALUES
(1, 3, 'Delayed birth certificate', 'Applied 2 weeks ago but no status update received.', 'service_delay', 'pending',     'medium', 2, '2024-06-10 15:00:00', '2024-06-10 15:00:00'),
(2, 4, 'Website login issue',       'Could not login yesterday, got server error.',         'technical',     'in_progress', 'high',   2, '2024-06-11 09:00:00', '2024-06-11 14:00:00'),
(3, 3, 'Wrong address on certificate', 'Approved certificate shows old address.',          'data_error',    'resolved',    'low',    2, '2024-06-12 10:00:00', '2024-06-13 11:00:00');

-- ------------------------------------------------------------
-- Sample notifications
-- ------------------------------------------------------------

INSERT INTO `notifications` (`id`, `user_id`, `title`, `message`, `type`, `is_read`, `created_at`) VALUES
(1, 3, 'Application Received',       'Your birth certificate application has been received and is under review.', 'info',    0, '2024-06-03 10:05:00'),
(2, 3, 'Application Approved',       'Your death certificate application has been approved.',                   'success', 1, '2024-06-05 14:00:00'),
(3, 4, 'Police Clearance Approved',  'Your police clearance certificate is ready for download.',                'success', 0, '2024-06-08 16:00:00'),
(4, 3, 'Blood Request Received',     'Your blood donation request has been logged. We will contact you shortly.', 'info',    0, '2024-06-12 07:05:00'),
(5, 2, 'New Complaint Assigned',     'A new complaint has been assigned to the admin team.',                    'warning', 0, '2024-06-10 15:05:00');

-- ------------------------------------------------------------
-- Blood inventory
-- ------------------------------------------------------------

INSERT INTO `blood_inventory` (`id`, `blood_type`, `quantity`, `last_updated`) VALUES
(1, 'A+',  45, '2024-06-13 08:00:00'),
(2, 'A-',  12, '2024-06-13 08:00:00'),
(3, 'B+',  38, '2024-06-13 08:00:00'),
(4, 'B-',  10, '2024-06-13 08:00:00'),
(5, 'AB+', 8,  '2024-06-13 08:00:00'),
(6, 'AB-', 5,  '2024-06-13 08:00:00'),
(7, 'O+',  52, '2024-06-13 08:00:00'),
(8, 'O-',  15, '2024-06-13 08:00:00');

-- ------------------------------------------------------------
-- Departments
-- ------------------------------------------------------------

INSERT INTO `departments` (`id`, `name`, `description`, `head_id`, `created_at`) VALUES
(1, 'Police Department',        'Handles police clearance and law enforcement services.', 5, '2024-06-01 09:00:00'),
(2, 'Health Services',          'Manages healthcare appointments and hospital coordination.', 6, '2024-06-01 09:00:00'),
(3, 'City Corporation',         'Trade licenses, building permits, and municipal services.', 7, '2024-06-01 09:00:00'),
(4, 'Blood Bank Services',      'Blood donation requests and inventory management.', 8, '2024-06-01 09:00:00'),
(5, 'ICT & Administration',     'System administration and citizen support.', 2, '2024-06-01 09:00:00');

-- ------------------------------------------------------------
-- Service requests
-- ------------------------------------------------------------

INSERT INTO `service_requests` (`id`, `user_id`, `service_type`, `status`, `priority`, `created_at`, `completed_at`) VALUES
(1, 3, 'birth_certificate',  'pending',   'medium', '2024-06-03 10:00:00', NULL),
(2, 3, 'police_clearance',   'pending',   'high',   '2024-06-06 08:00:00', NULL),
(3, 4, 'police_clearance',   'completed', 'medium', '2024-06-07 10:00:00', '2024-06-08 16:00:00'),
(4, 4, 'healthcare_appointment', 'completed', 'high', '2024-06-09 09:00:00', '2024-06-10 11:00:00');

-- ------------------------------------------------------------
-- Audit logs
-- ------------------------------------------------------------

INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `details`, `ip_address`, `created_at`) VALUES
(1, 1, 'login',              'user', 1,  'Super admin logged in',           '127.0.0.1', '2024-06-01 09:00:00'),
(2, 3, 'create_application', 'service_application', 1, 'Birth certificate application submitted', '127.0.0.1', '2024-06-03 10:00:00'),
(3, 5, 'approve_application','service_application', 5, 'Police clearance approved for user 4', '127.0.0.1', '2024-06-08 16:00:00'),
(4, 2, 'assign_complaint',   'complaint', 1, 'Complaint assigned to admin', '127.0.0.1', '2024-06-10 15:05:00'),
(5, 8, 'fulfill_blood_request','service_application', 11, 'Blood request fulfilled from inventory', '127.0.0.1', '2024-06-13 12:00:00');

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

-- ============================================================
-- LOGIN CREDENTIALS (password for all: Password123)
-- ============================================================
-- Role        | Email                              | Portal URL after login
-- ------------|------------------------------------|---------------------------
-- Superadmin  | superadmin@smartbangladesh.gov.bd  | /admin/dashboard
-- Admin       | admin@smartbangladesh.gov.bd       | /admin/dashboard
-- Citizen     | citizen@example.com                | /citizen/dashboard
-- Citizen     | karim@example.com                  | /citizen/dashboard
-- Police      | police@smartbangladesh.gov.bd      | /police/dashboard
-- Hospital    | hospital@smartbangladesh.gov.bd    | /hospital/dashboard
-- City Corp   | citycorp@smartbangladesh.gov.bd    | /city-corp/dashboard
-- Blood Bank  | bloodbank@smartbangladesh.gov.bd   | /blood-bank/dashboard
-- ============================================================
