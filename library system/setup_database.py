"""
Database Setup Script
Run this script to initialize the database and test the connection
"""

import mysql.connector
from mysql.connector import Error
import hashlib

def setup_database():
    """Setup database and tables"""
    
    print("=" * 60)
    print("Library Management System - Database Setup")
    print("=" * 60)
    print()
    
    # Get database credentials
    print("Please enter your MySQL credentials:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    user = input("Username (default: root): ").strip() or "root"
    password = input("Password: ").strip()
    
    print("\n" + "=" * 60)
    print("Creating database and tables...")
    print("=" * 60 + "\n")
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("✓ Connected to MySQL server")
            
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
            print("✓ Database 'library_db' created/verified")
            
            cursor.execute("USE library_db")
            
            # Create Books table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    book_id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    isbn VARCHAR(50) UNIQUE,
                    category VARCHAR(100),
                    quantity INT DEFAULT 1,
                    available INT DEFAULT 1,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✓ Books table created")
            
            # Create Students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    phone VARCHAR(20),
                    address TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✓ Students table created")
            
            # Create Librarians table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS librarians (
                    librarian_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    email VARCHAR(255),
                    role VARCHAR(50) DEFAULT 'librarian'
                )
            """)
            print("✓ Librarians table created")
            
            # Create Issues table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS issues (
                    issue_id INT AUTO_INCREMENT PRIMARY KEY,
                    book_id INT,
                    student_id INT,
                    issue_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    return_date DATE,
                    status VARCHAR(50) DEFAULT 'issued',
                    fine DECIMAL(10,2) DEFAULT 0,
                    damage_charge DECIMAL(10,2) DEFAULT 0,
                    FOREIGN KEY (book_id) REFERENCES books(book_id),
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                )
            """)
            print("✓ Issues table created")
            
            # Create default admin
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            try:
                cursor.execute("""
                    INSERT INTO librarians (username, password, full_name, role)
                    VALUES (%s, %s, %s, %s)
                """, ('admin', password_hash, 'Administrator', 'admin'))
                connection.commit()
                print("✓ Default admin account created (username: admin, password: admin123)")
            except Error:
                print("✓ Default admin account already exists")
            
            # Insert sample data
            print("\n" + "=" * 60)
            print("Adding sample data...")
            print("=" * 60 + "\n")
            
            # Sample books
            sample_books = [
                ("To Kill a Mockingbird", "Harper Lee", "978-0061120084", "Fiction", 3),
                ("1984", "George Orwell", "978-0451524935", "Fiction", 2),
                ("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", "Fiction", 2),
                ("Python Programming", "John Smith", "978-1234567890", "Programming", 5),
                ("Data Structures", "Jane Doe", "978-0987654321", "Computer Science", 4)
            ]
            
            for book in sample_books:
                try:
                    cursor.execute("""
                        INSERT INTO books (title, author, isbn, category, quantity, available)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, book + (book[4],))
                except Error:
                    pass  # Book already exists
            
            connection.commit()
            print("✓ Sample books added")
            
            # Sample students
            sample_students = [
                ("John Doe", "john.doe@email.com", "1234567890", "123 Main St"),
                ("Jane Smith", "jane.smith@email.com", "0987654321", "456 Oak Ave"),
                ("Bob Johnson", "bob.johnson@email.com", "5555555555", "789 Pine Rd")
            ]
            
            for student in sample_students:
                try:
                    cursor.execute("""
                        INSERT INTO students (name, email, phone, address)
                        VALUES (%s, %s, %s, %s)
                    """, student)
                except Error:
                    pass  # Student already exists
            
            connection.commit()
            print("✓ Sample students added")
            
            print("\n" + "=" * 60)
            print("Database setup completed successfully!")
            print("=" * 60)
            print("\nYou can now run the main application:")
            print("  python library_management_system.py")
            print("\nDefault login credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\nStudent login (use email):")
            print("  john.doe@email.com")
            print("  jane.smith@email.com")
            print("  bob.johnson@email.com")
            print("=" * 60)
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("  1. MySQL server is running")
        print("  2. Credentials are correct")
        print("  3. User has necessary permissions")
        return False
    
    return True

if __name__ == "__main__":
    setup_database()
    input("\nPress Enter to exit...")
