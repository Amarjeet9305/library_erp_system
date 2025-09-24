CREATE DATABASE IF NOT EXISTS `library_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `library_db`;

-- Core reference tables
CREATE TABLE IF NOT EXISTS roles (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(32) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	full_name VARCHAR(255) NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	type ENUM('student','staff','admin') NOT NULL DEFAULT 'student',
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_roles (
	user_id INT NOT NULL,
	role_id INT NOT NULL,
	PRIMARY KEY (user_id, role_id),
	CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	CONSTRAINT fk_user_roles_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS categories (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(128) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS authors (
	id INT AUTO_INCREMENT PRIMARY KEY,
	full_name VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS books (
	id INT AUTO_INCREMENT PRIMARY KEY,
	isbn VARCHAR(32) NOT NULL UNIQUE,
	title VARCHAR(255) NOT NULL,
	category_id INT NULL,
	total_copies INT NOT NULL DEFAULT 0,
	available_copies INT NOT NULL DEFAULT 0,
	CONSTRAINT fk_books_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS book_authors (
	book_id INT NOT NULL,
	author_id INT NOT NULL,
	PRIMARY KEY (book_id, author_id),
	CONSTRAINT fk_book_authors_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
	CONSTRAINT fk_book_authors_author FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS book_copies (
	id INT AUTO_INCREMENT PRIMARY KEY,
	book_id INT NOT NULL,
	barcode VARCHAR(64) NOT NULL UNIQUE,
	status ENUM('available','issued','lost','repair') NOT NULL DEFAULT 'available',
	CONSTRAINT fk_book_copies_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS transactions (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	book_id INT NOT NULL,
	copy_id INT NOT NULL,
	issue_date DATE NOT NULL,
	due_date DATE NOT NULL,
	return_date DATE NULL,
	fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
	status ENUM('issued','returned','overdue') NOT NULL DEFAULT 'issued',
	CONSTRAINT fk_tx_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
	CONSTRAINT fk_tx_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE RESTRICT,
	CONSTRAINT fk_tx_copy FOREIGN KEY (copy_id) REFERENCES book_copies(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Seed roles
INSERT INTO roles (name) VALUES ('admin'),('staff'),('student')
ON DUPLICATE KEY UPDATE name=VALUES(name);
