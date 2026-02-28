"""
Library Management System
A professional GUI application for managing library operations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import hashlib
import qrcode
from PIL import Image, ImageTk
import io
import csv
from datetime import datetime, timedelta
import os

# Professional Color Scheme
COLORS = {
    'primary': '#2C3E50',      # Dark blue-gray
    'secondary': '#3498DB',    # Bright blue
    'accent': '#E74C3C',       # Red
    'success': '#27AE60',      # Green
    'warning': '#F39C12',      # Orange
    'bg_light': '#ECF0F1',     # Light gray
    'bg_white': '#FFFFFF',     # White
    'text_dark': '#2C3E50',    # Dark text
    'text_light': '#7F8C8D',   # Light gray text
    'hover': '#5DADE2'         # Light blue
}

class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self):
        self.connection = None
        self.create_connection()
        self.create_tables()
        self.create_default_admin()
    
    def create_connection(self):
        """Create database connection"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',  # Update with your MySQL password
                database='library_db'
            )
            if self.connection.is_connected():
                print("✓ Connected to MySQL database")
        except Error as e:
            if "Unknown database" in str(e):
                # Create database if it doesn't exist
                try:
                    temp_conn = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password=''
                    )
                    cursor = temp_conn.cursor()
                    cursor.execute("CREATE DATABASE library_db")
                    cursor.close()
                    temp_conn.close()
                    self.create_connection()
                except Error as db_error:
                    messagebox.showerror("Database Error", f"Could not create database: {db_error}")
            else:
                messagebox.showerror("Connection Error", f"Error connecting to MySQL: {e}")
    
    def create_tables(self):
        """Create necessary tables"""
        if not self.connection:
            return
        
        cursor = self.connection.cursor()
        
        # Books table
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
        
        # Students table
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
        
        # Librarians table
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
        
        # Issues table
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
        
        self.connection.commit()
        cursor.close()
    
    def create_default_admin(self):
        """Create default admin account"""
        if not self.connection:
            return
        
        cursor = self.connection.cursor()
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        
        try:
            cursor.execute("""
                INSERT INTO librarians (username, password, full_name, role)
                VALUES (%s, %s, %s, %s)
            """, ('admin', password_hash, 'Administrator', 'admin'))
            self.connection.commit()
        except Error:
            pass  # Admin already exists
        finally:
            cursor.close()
    
    def verify_login(self, username, password, user_type):
        """Verify user login credentials"""
        if not self.connection:
            return False, None
        
        cursor = self.connection.cursor(dictionary=True)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user_type == 'librarian':
            cursor.execute("""
                SELECT * FROM librarians 
                WHERE username = %s AND password = %s
            """, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            return (True, user) if user else (False, None)
        else:
            cursor.execute("""
                SELECT * FROM students 
                WHERE email = %s
            """, (username,))
            user = cursor.fetchone()
            cursor.close()
            # For students, we'll use email as login, no password for simplicity
            return (True, user) if user else (False, None)
    
    def add_book(self, title, author, isbn, category, quantity):
        """Add a new book"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO books (title, author, isbn, category, quantity, available)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, author, isbn, category, quantity, quantity))
            self.connection.commit()
            cursor.close()
            return True, "Book added successfully!"
        except Error as e:
            cursor.close()
            return False, f"Error: {e}"
    
    def add_student(self, name, email, phone, address):
        """Add a new student"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO students (name, email, phone, address)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, address))
            self.connection.commit()
            cursor.close()
            return True, "Student added successfully!"
        except Error as e:
            cursor.close()
            return False, f"Error: {e}"
    
    def get_all_books(self):
        """Get all books"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books ORDER BY title")
        books = cursor.fetchall()
        cursor.close()
        return books
    
    def get_all_students(self):
        """Get all students"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY name")
        students = cursor.fetchall()
        cursor.close()
        return students
    
    def issue_book(self, book_id, student_id, days=14):
        """Issue a book to a student"""
        cursor = self.connection.cursor()
        try:
            # Check book availability
            cursor.execute("SELECT available FROM books WHERE book_id = %s", (book_id,))
            result = cursor.fetchone()
            
            if result and result[0] > 0:
                issue_date = datetime.now().date()
                due_date = issue_date + timedelta(days=days)
                
                cursor.execute("""
                    INSERT INTO issues (book_id, student_id, issue_date, due_date, status)
                    VALUES (%s, %s, %s, %s, 'issued')
                """, (book_id, student_id, issue_date, due_date))
                
                cursor.execute("""
                    UPDATE books SET available = available - 1 
                    WHERE book_id = %s
                """, (book_id,))
                
                self.connection.commit()
                cursor.close()
                return True, "Book issued successfully!"
            else:
                cursor.close()
                return False, "Book not available!"
        except Error as e:
            cursor.close()
            return False, f"Error: {e}"
    
    def return_book(self, issue_id, damage_charge=0):
        """Return a book"""
        cursor = self.connection.cursor()
        try:
            # Get issue details
            cursor.execute("""
                SELECT book_id, due_date FROM issues 
                WHERE issue_id = %s AND status = 'issued'
            """, (issue_id,))
            result = cursor.fetchone()
            
            if result:
                book_id, due_date = result
                return_date = datetime.now().date()
                
                # Calculate fine for overdue
                fine = 0
                if return_date > due_date:
                    days_late = (return_date - due_date).days
                    fine = days_late * 5  # $5 per day
                
                cursor.execute("""
                    UPDATE issues 
                    SET return_date = %s, status = 'returned', 
                        fine = %s, damage_charge = %s
                    WHERE issue_id = %s
                """, (return_date, fine, damage_charge, issue_id))
                
                cursor.execute("""
                    UPDATE books SET available = available + 1 
                    WHERE book_id = %s
                """, (book_id,))
                
                self.connection.commit()
                cursor.close()
                
                total_charge = fine + damage_charge
                msg = f"Book returned! Fine: ${fine}, Damage: ${damage_charge}, Total: ${total_charge}"
                return True, msg
            else:
                cursor.close()
                return False, "Issue record not found!"
        except Error as e:
            cursor.close()
            return False, f"Error: {e}"
    
    def get_issued_books(self):
        """Get all currently issued books"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.issue_id, b.title, b.author, s.name as student_name,
                   i.issue_date, i.due_date, i.status
            FROM issues i
            JOIN books b ON i.book_id = b.book_id
            JOIN students s ON i.student_id = s.student_id
            WHERE i.status = 'issued'
            ORDER BY i.issue_date DESC
        """)
        issues = cursor.fetchall()
        cursor.close()
        return issues
    
    def get_overdue_books(self):
        """Get overdue books"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.issue_id, b.title, s.name as student_name,
                   i.issue_date, i.due_date,
                   DATEDIFF(CURDATE(), i.due_date) as days_overdue
            FROM issues i
            JOIN books b ON i.book_id = b.book_id
            JOIN students s ON i.student_id = s.student_id
            WHERE i.status = 'issued' AND i.due_date < CURDATE()
            ORDER BY days_overdue DESC
        """)
        overdue = cursor.fetchall()
        cursor.close()
        return overdue
    
    def get_student_history(self, student_id):
        """Get issue history for a student"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.issue_id, b.title, b.author, i.issue_date, 
                   i.due_date, i.return_date, i.status, i.fine, i.damage_charge
            FROM issues i
            JOIN books b ON i.book_id = b.book_id
            WHERE i.student_id = %s
            ORDER BY i.issue_date DESC
        """, (student_id,))
        history = cursor.fetchall()
        cursor.close()
        return history
    
    def get_statistics(self):
        """Get library statistics"""
        cursor = self.connection.cursor(dictionary=True)
        
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as count FROM books")
        stats['total_books'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT SUM(quantity) as count FROM books")
        stats['total_copies'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT SUM(available) as count FROM books")
        stats['available_books'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM students")
        stats['total_students'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM issues WHERE status = 'issued'")
        stats['issued_books'] = cursor.fetchone()['count']
        
        cursor.execute("""
            SELECT COUNT(*) as count FROM issues 
            WHERE status = 'issued' AND due_date < CURDATE()
        """)
        stats['overdue_books'] = cursor.fetchone()['count']
        
        cursor.close()
        return stats
    
    def export_to_csv(self, table_name, filename):
        """Export table data to CSV"""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            if table_name == 'books':
                cursor.execute("SELECT * FROM books")
            elif table_name == 'students':
                cursor.execute("SELECT * FROM students")
            elif table_name == 'issues':
                cursor.execute("""
                    SELECT i.issue_id, b.title, s.name as student_name,
                           i.issue_date, i.due_date, i.return_date, 
                           i.status, i.fine, i.damage_charge
                    FROM issues i
                    JOIN books b ON i.book_id = b.book_id
                    JOIN students s ON i.student_id = s.student_id
                """)
            
            data = cursor.fetchall()
            
            if data:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                
                cursor.close()
                return True, f"Data exported to {filename}"
            else:
                cursor.close()
                return False, "No data to export"
        except Error as e:
            cursor.close()
            return False, f"Export error: {e}"


class ModernButton(tk.Button):
    """Custom styled button"""
    
    def __init__(self, parent, text, command, bg_color=COLORS['secondary'], **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            **kwargs
        )
        self.bg_color = bg_color
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self.config(bg=COLORS['hover'])
    
    def on_leave(self, e):
        self.config(bg=self.bg_color)


class LoginWindow:
    """Login window for librarians and students"""
    
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager
        self.root.title("Library Management System - Login")
        self.root.geometry("1000x600")
        self.root.configure(bg=COLORS['bg_light'])
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Left side - Image/Branding
        left_frame = tk.Frame(main_frame, bg=COLORS['primary'], width=400)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        # Logo and title
        logo_frame = tk.Frame(left_frame, bg=COLORS['primary'])
        logo_frame.pack(expand=True)
        
        title_label = tk.Label(
            logo_frame,
            text="📚",
            font=('Segoe UI', 80),
            bg=COLORS['primary'],
            fg='white'
        )
        title_label.pack(pady=20)
        
        title = tk.Label(
            logo_frame,
            text="Library Management\nSystem",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['primary'],
            fg='white',
            justify='center'
        )
        title.pack()
        
        subtitle = tk.Label(
            logo_frame,
            text="Manage your library with ease",
            font=('Segoe UI', 12),
            bg=COLORS['primary'],
            fg=COLORS['bg_light']
        )
        subtitle.pack(pady=10)
        
        # Right side - Login form
        right_frame = tk.Frame(main_frame, bg=COLORS['bg_white'])
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Login form container
        form_frame = tk.Frame(right_frame, bg=COLORS['bg_white'])
        form_frame.pack(expand=True, padx=40, pady=40)
        
        # Title
        login_title = tk.Label(
            form_frame,
            text="Welcome Back!",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark']
        )
        login_title.pack(pady=(0, 10))
        
        subtitle = tk.Label(
            form_frame,
            text="Please login to continue",
            font=('Segoe UI', 11),
            bg=COLORS['bg_white'],
            fg=COLORS['text_light']
        )
        subtitle.pack(pady=(0, 30))
        
        # User type selection
        type_frame = tk.Frame(form_frame, bg=COLORS['bg_white'])
        type_frame.pack(fill='x', pady=10)
        
        self.user_type = tk.StringVar(value='librarian')
        
        librarian_rb = tk.Radiobutton(
            type_frame,
            text="Librarian",
            variable=self.user_type,
            value='librarian',
            font=('Segoe UI', 11),
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark'],
            selectcolor=COLORS['bg_light'],
            activebackground=COLORS['bg_white']
        )
        librarian_rb.pack(side='left', padx=10)
        
        student_rb = tk.Radiobutton(
            type_frame,
            text="Student",
            variable=self.user_type,
            value='student',
            font=('Segoe UI', 11),
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark'],
            selectcolor=COLORS['bg_light'],
            activebackground=COLORS['bg_white']
        )
        student_rb.pack(side='left', padx=10)
        
        # Username
        username_label = tk.Label(
            form_frame,
            text="Username / Email",
            font=('Segoe UI', 11),
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark'],
            anchor='w'
        )
        username_label.pack(fill='x', pady=(20, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1
        )
        self.username_entry.pack(fill='x', ipady=8)
        
        # Password (only for librarians)
        self.password_label = tk.Label(
            form_frame,
            text="Password",
            font=('Segoe UI', 11),
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark'],
            anchor='w'
        )
        self.password_label.pack(fill='x', pady=(15, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 12),
            show='●',
            relief='solid',
            bd=1
        )
        self.password_entry.pack(fill='x', ipady=8)
        
        # Login button
        login_btn = ModernButton(
            form_frame,
            text="Login",
            command=self.login,
            bg_color=COLORS['secondary']
        )
        login_btn.pack(fill='x', pady=(30, 10))
        
        # Info text
        info_label = tk.Label(
            form_frame,
            text="Default Admin: username=admin, password=admin123",
            font=('Segoe UI', 9),
            bg=COLORS['bg_white'],
            fg=COLORS['text_light']
        )
        info_label.pack(pady=10)
        
        # Update form based on user type
        self.user_type.trace('w', self.update_form)
    
    def update_form(self, *args):
        """Update form based on user type"""
        if self.user_type.get() == 'student':
            self.password_label.pack_forget()
            self.password_entry.pack_forget()
        else:
            self.password_label.pack(fill='x', pady=(15, 5))
            self.password_entry.pack(fill='x', ipady=8)
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user_type = self.user_type.get()
        
        if not username:
            messagebox.showerror("Error", "Please enter username/email")
            return
        
        if user_type == 'librarian' and not password:
            messagebox.showerror("Error", "Please enter password")
            return
        
        success, user = self.db.verify_login(username, password, user_type)
        
        if success:
            self.root.withdraw()
            if user_type == 'librarian':
                DashboardWindow(self.root, self.db, user)
            else:
                StudentDashboard(self.root, self.db, user)
        else:
            messagebox.showerror("Error", "Invalid credentials!")


class DashboardWindow:
    """Main dashboard for librarians"""
    
    def __init__(self, parent, db_manager, user):
        self.parent = parent
        self.db = db_manager
        self.user = user
        
        self.root = tk.Toplevel(parent)
        self.root.title("Library Management System - Dashboard")
        self.root.geometry("1400x800")
        self.root.configure(bg=COLORS['bg_light'])
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.create_widgets()
        self.show_home()
    
    def create_widgets(self):
        # Top bar
        top_bar = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        top_bar.pack(fill='x')
        
        # Logo and title
        logo_label = tk.Label(
            top_bar,
            text="📚 Library Management System",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['primary'],
            fg='white'
        )
        logo_label.pack(side='left', padx=20, pady=15)
        
        # User info
        user_label = tk.Label(
            top_bar,
            text=f"Welcome, {self.user['full_name']}",
            font=('Segoe UI', 12),
            bg=COLORS['primary'],
            fg='white'
        )
        user_label.pack(side='right', padx=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_container.pack(fill='both', expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_container, bg=COLORS['primary'], width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Menu buttons
        menu_items = [
            ("🏠 Home", self.show_home),
            ("📖 Books", self.show_books),
            ("👨‍🎓 Students", self.show_students),
            ("📤 Issue Book", self.show_issue),
            ("📥 Return Book", self.show_return),
            ("⏰ Overdue", self.show_overdue),
            ("📊 Reports", self.show_reports),
            ("💾 Backup", self.show_backup),
            ("🚪 Logout", self.logout)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                command=command,
                bg=COLORS['primary'],
                fg='white',
                font=('Segoe UI', 12),
                relief='flat',
                cursor='hand2',
                anchor='w',
                padx=20,
                pady=15
            )
            btn.pack(fill='x')
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=COLORS['secondary']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=COLORS['primary']))
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg=COLORS['bg_light'])
        self.content_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Show home dashboard with statistics"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Dashboard Overview",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 30))
        
        # Statistics cards
        stats = self.db.get_statistics()
        
        cards_frame = tk.Frame(self.content_frame, bg=COLORS['bg_light'])
        cards_frame.pack(fill='x', pady=20)
        
        stat_items = [
            ("Total Books", stats['total_books'], COLORS['secondary'], "📚"),
            ("Total Copies", stats['total_copies'], COLORS['success'], "📖"),
            ("Available", stats['available_books'], COLORS['warning'], "✓"),
            ("Students", stats['total_students'], COLORS['accent'], "👥"),
            ("Issued", stats['issued_books'], "#9B59B6", "📤"),
            ("Overdue", stats['overdue_books'], "#E74C3C", "⏰")
        ]
        
        for i, (title, value, color, icon) in enumerate(stat_items):
            card = tk.Frame(cards_frame, bg=color, relief='flat')
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='ew')
            
            icon_label = tk.Label(
                card,
                text=icon,
                font=('Segoe UI', 40),
                bg=color,
                fg='white'
            )
            icon_label.pack(pady=(20, 10))
            
            value_label = tk.Label(
                card,
                text=str(value),
                font=('Segoe UI', 32, 'bold'),
                bg=color,
                fg='white'
            )
            value_label.pack()
            
            title_label = tk.Label(
                card,
                text=title,
                font=('Segoe UI', 12),
                bg=color,
                fg='white'
            )
            title_label.pack(pady=(5, 20))
        
        # Configure grid weights
        for i in range(3):
            cards_frame.columnconfigure(i, weight=1)
        
        # Recent activities
        activities_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'], relief='solid', bd=1)
        activities_frame.pack(fill='both', expand=True, pady=20)
        
        activities_title = tk.Label(
            activities_frame,
            text="Recent Issues",
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark']
        )
        activities_title.pack(pady=15, padx=20, anchor='w')
        
        # Get recent issues
        issues = self.db.get_issued_books()[:5]
        
        for issue in issues:
            issue_frame = tk.Frame(activities_frame, bg=COLORS['bg_light'])
            issue_frame.pack(fill='x', padx=20, pady=5)
            
            info_text = f"📖 {issue['title']} - {issue['student_name']} (Due: {issue['due_date']})"
            info_label = tk.Label(
                issue_frame,
                text=info_text,
                font=('Segoe UI', 11),
                bg=COLORS['bg_light'],
                fg=COLORS['text_dark'],
                anchor='w'
            )
            info_label.pack(fill='x', padx=10, pady=8)
    
    def show_books(self):
        """Show books management"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Books Management",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 20))
        
        # Add book button
        btn_frame = tk.Frame(self.content_frame, bg=COLORS['bg_light'])
        btn_frame.pack(fill='x', pady=10)
        
        add_btn = ModernButton(
            btn_frame,
            text="➕ Add New Book",
            command=self.add_book_dialog,
            bg_color=COLORS['success']
        )
        add_btn.pack(side='left')
        
        # Search
        search_frame = tk.Frame(self.content_frame, bg=COLORS['bg_light'])
        search_frame.pack(fill='x', pady=10)
        
        search_label = tk.Label(
            search_frame,
            text="Search:",
            font=('Segoe UI', 11),
            bg=COLORS['bg_light']
        )
        search_label.pack(side='left', padx=5)
        
        search_entry = tk.Entry(search_frame, font=('Segoe UI', 11), width=40)
        search_entry.pack(side='left', padx=5)
        
        # Books table
        table_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'])
        table_frame.pack(fill='both', expand=True, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Title', 'Author', 'ISBN', 'Category', 'Total', 'Available')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill='both', expand=True)
        
        # Load books
        books = self.db.get_all_books()
        for book in books:
            tree.insert('', 'end', values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['isbn'],
                book['category'],
                book['quantity'],
                book['available']
            ))
    
    def add_book_dialog(self):
        """Dialog to add a new book"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("500x450")
        dialog.configure(bg=COLORS['bg_white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Form
        form_frame = tk.Frame(dialog, bg=COLORS['bg_white'])
        form_frame.pack(padx=30, pady=30, fill='both', expand=True)
        
        # Title
        tk.Label(form_frame, text="Title:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=0, column=0, sticky='w', pady=10)
        title_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        title_entry.grid(row=0, column=1, pady=10)
        
        # Author
        tk.Label(form_frame, text="Author:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=1, column=0, sticky='w', pady=10)
        author_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        author_entry.grid(row=1, column=1, pady=10)
        
        # ISBN
        tk.Label(form_frame, text="ISBN:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=2, column=0, sticky='w', pady=10)
        isbn_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        isbn_entry.grid(row=2, column=1, pady=10)
        
        # Category
        tk.Label(form_frame, text="Category:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=3, column=0, sticky='w', pady=10)
        category_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        category_entry.grid(row=3, column=1, pady=10)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=4, column=0, sticky='w', pady=10)
        quantity_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        quantity_entry.grid(row=4, column=1, pady=10)
        
        def save_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            isbn = isbn_entry.get().strip()
            category = category_entry.get().strip()
            
            try:
                quantity = int(quantity_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid quantity")
                return
            
            if not all([title, author, isbn, category]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            success, message = self.db.add_book(title, author, isbn, category, quantity)
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.show_books()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_white'])
        btn_frame.grid(row=5, column=0, columnspan=2, pady=30)
        
        ModernButton(btn_frame, "Save", save_book, bg_color=COLORS['success']).pack(side='left', padx=5)
        ModernButton(btn_frame, "Cancel", dialog.destroy, bg_color=COLORS['accent']).pack(side='left', padx=5)
    
    def show_students(self):
        """Show students management"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Students Management",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 20))
        
        # Add student button
        btn_frame = tk.Frame(self.content_frame, bg=COLORS['bg_light'])
        btn_frame.pack(fill='x', pady=10)
        
        add_btn = ModernButton(
            btn_frame,
            text="➕ Add New Student",
            command=self.add_student_dialog,
            bg_color=COLORS['success']
        )
        add_btn.pack(side='left')
        
        # Students table
        table_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'])
        table_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('ID', 'Name', 'Email', 'Phone', 'Registration Date')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill='both', expand=True)
        
        # Load students
        students = self.db.get_all_students()
        for student in students:
            tree.insert('', 'end', values=(
                student['student_id'],
                student['name'],
                student['email'],
                student['phone'],
                student['registration_date']
            ))
        
        # Double click to view history
        def on_double_click(event):
            item = tree.selection()[0]
            student_id = tree.item(item, 'values')[0]
            self.show_student_history(student_id)
        
        tree.bind('<Double-1>', on_double_click)
    
    def add_student_dialog(self):
        """Dialog to add a new student"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS['bg_white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Form
        form_frame = tk.Frame(dialog, bg=COLORS['bg_white'])
        form_frame.pack(padx=30, pady=30, fill='both', expand=True)
        
        # Name
        tk.Label(form_frame, text="Name:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=0, column=0, sticky='w', pady=10)
        name_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        name_entry.grid(row=0, column=1, pady=10)
        
        # Email
        tk.Label(form_frame, text="Email:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=1, column=0, sticky='w', pady=10)
        email_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        email_entry.grid(row=1, column=1, pady=10)
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=2, column=0, sticky='w', pady=10)
        phone_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        phone_entry.grid(row=2, column=1, pady=10)
        
        # Address
        tk.Label(form_frame, text="Address:", font=('Segoe UI', 11), bg=COLORS['bg_white']).grid(row=3, column=0, sticky='w', pady=10)
        address_entry = tk.Text(form_frame, font=('Segoe UI', 11), width=30, height=4)
        address_entry.grid(row=3, column=1, pady=10)
        
        def save_student():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get('1.0', 'end').strip()
            
            if not all([name, email, phone]):
                messagebox.showerror("Error", "Please fill required fields")
                return
            
            success, message = self.db.add_student(name, email, phone, address)
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.show_students()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_white'])
        btn_frame.grid(row=4, column=0, columnspan=2, pady=30)
        
        ModernButton(btn_frame, "Save", save_student, bg_color=COLORS['success']).pack(side='left', padx=5)
        ModernButton(btn_frame, "Cancel", dialog.destroy, bg_color=COLORS['accent']).pack(side='left', padx=5)
    
    def show_issue(self):
        """Show issue book interface"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Issue Book",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 20))
        
        # Form
        form_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'], relief='solid', bd=1)
        form_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        inner_frame = tk.Frame(form_frame, bg=COLORS['bg_white'])
        inner_frame.pack(padx=50, pady=50)
        
        # Book selection
        tk.Label(inner_frame, text="Select Book:", font=('Segoe UI', 12, 'bold'), bg=COLORS['bg_white']).grid(row=0, column=0, sticky='w', pady=15)
        
        books = self.db.get_all_books()
        book_options = [f"{b['book_id']} - {b['title']} (Available: {b['available']})" for b in books if b['available'] > 0]
        
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(inner_frame, textvariable=book_var, values=book_options, font=('Segoe UI', 11), width=40, state='readonly')
        book_combo.grid(row=0, column=1, pady=15, padx=10)
        
        # Student selection
        tk.Label(inner_frame, text="Select Student:", font=('Segoe UI', 12, 'bold'), bg=COLORS['bg_white']).grid(row=1, column=0, sticky='w', pady=15)
        
        students = self.db.get_all_students()
        student_options = [f"{s['student_id']} - {s['name']} ({s['email']})" for s in students]
        
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(inner_frame, textvariable=student_var, values=student_options, font=('Segoe UI', 11), width=40, state='readonly')
        student_combo.grid(row=1, column=1, pady=15, padx=10)
        
        # Days
        tk.Label(inner_frame, text="Days:", font=('Segoe UI', 12, 'bold'), bg=COLORS['bg_white']).grid(row=2, column=0, sticky='w', pady=15)
        days_entry = tk.Entry(inner_frame, font=('Segoe UI', 11), width=42)
        days_entry.insert(0, "14")
        days_entry.grid(row=2, column=1, pady=15, padx=10)
        
        def issue_book():
            book_selection = book_var.get()
            student_selection = student_var.get()
            
            if not book_selection or not student_selection:
                messagebox.showerror("Error", "Please select book and student")
                return
            
            try:
                book_id = int(book_selection.split(' - ')[0])
                student_id = int(student_selection.split(' - ')[0])
                days = int(days_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid input")
                return
            
            success, message = self.db.issue_book(book_id, student_id, days)
            
            if success:
                messagebox.showinfo("Success", message)
                self.show_issue()
            else:
                messagebox.showerror("Error", message)
        
        # Issue button
        ModernButton(inner_frame, "Issue Book", issue_book, bg_color=COLORS['success']).grid(row=3, column=0, columnspan=2, pady=30)
        
        # Current issues table
        table_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'])
        table_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(table_frame, text="Currently Issued Books", font=('Segoe UI', 14, 'bold'), bg=COLORS['bg_white']).pack(pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('Issue ID', 'Book', 'Student', 'Issue Date', 'Due Date')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set, height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load issued books
        issues = self.db.get_issued_books()
        for issue in issues:
            tree.insert('', 'end', values=(
                issue['issue_id'],
                issue['title'],
                issue['student_name'],
                issue['issue_date'],
                issue['due_date']
            ))
    
    def show_return(self):
        """Show return book interface"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Return Book",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 20))
        
        # Issued books table
        table_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'])
        table_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('Issue ID', 'Book', 'Author', 'Student', 'Issue Date', 'Due Date', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load issued books
        issues = self.db.get_issued_books()
        for issue in issues:
            # Check if overdue
            due_date = issue['due_date']
            today = datetime.now().date()
            status = "Overdue" if today > due_date else "On Time"
            
            tree.insert('', 'end', values=(
                issue['issue_id'],
                issue['title'],
                issue['author'],
                issue['student_name'],
                issue['issue_date'],
                issue['due_date'],
                status
            ))
        
        def return_book():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select an issue to return")
                return
            
            issue_id = tree.item(selection[0], 'values')[0]
            
            # Ask for damage charge
            damage_dialog = tk.Toplevel(self.root)
            damage_dialog.title("Return Book")
            damage_dialog.geometry("400x250")
            damage_dialog.configure(bg=COLORS['bg_white'])
            damage_dialog.transient(self.root)
            damage_dialog.grab_set()
            
            # Center dialog
            damage_dialog.update_idletasks()
            x = (damage_dialog.winfo_screenwidth() // 2) - (damage_dialog.winfo_width() // 2)
            y = (damage_dialog.winfo_screenheight() // 2) - (damage_dialog.winfo_height() // 2)
            damage_dialog.geometry(f'+{x}+{y}')
            
            tk.Label(damage_dialog, text="Is the book damaged?", font=('Segoe UI', 14, 'bold'), bg=COLORS['bg_white']).pack(pady=20)
            
            tk.Label(damage_dialog, text="Damage Charge ($):", font=('Segoe UI', 11), bg=COLORS['bg_white']).pack(pady=10)
            damage_entry = tk.Entry(damage_dialog, font=('Segoe UI', 11))
            damage_entry.insert(0, "0")
            damage_entry.pack(pady=10)
            
            def process_return():
                try:
                    damage_charge = float(damage_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid damage charge")
                    return
                
                success, message = self.db.return_book(issue_id, damage_charge)
                
                if success:
                    messagebox.showinfo("Success", message)
                    damage_dialog.destroy()
                    self.show_return()
                else:
                    messagebox.showerror("Error", message)
            
            ModernButton(damage_dialog, "Process Return", process_return, bg_color=COLORS['success']).pack(pady=20)
        
        # Return button
        btn_frame = tk.Frame(self.content_frame, bg=COLORS['bg_light'])
        btn_frame.pack(fill='x', pady=10)
        
        ModernButton(btn_frame, "Return Selected Book", return_book, bg_color=COLORS['success']).pack(side='left')
    
    def show_overdue(self):
        """Show overdue books"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Overdue Books",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 20))
        
        # Overdue books table
        table_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'])
        table_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('Issue ID', 'Book', 'Student', 'Issue Date', 'Due Date', 'Days Overdue')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load overdue books
        overdue = self.db.get_overdue_books()
        for item in overdue:
            tree.insert('', 'end', values=(
                item['issue_id'],
                item['title'],
                item['student_name'],
                item['issue_date'],
                item['due_date'],
                item['days_overdue']
            ), tags=('overdue',))
        
        # Color overdue items red
        tree.tag_configure('overdue', background='#FADBD8', foreground=COLORS['accent'])
        
        if not overdue:
            tk.Label(
                self.content_frame,
                text="✓ No overdue books!",
                font=('Segoe UI', 16, 'bold'),
                bg=COLORS['bg_light'],
                fg=COLORS['success']
            ).pack(pady=50)
    
    def show_reports(self):
        """Show reports and charts"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Reports & Statistics",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 30))
        
        stats = self.db.get_statistics()
        
        # Create a more detailed report
        report_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'], relief='solid', bd=1)
        report_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Report sections
        sections = [
            ("📚 Library Collection", [
                ("Total Book Titles", stats['total_books']),
                ("Total Book Copies", stats['total_copies']),
                ("Available Books", stats['available_books']),
                ("Books Issued", stats['issued_books'])
            ]),
            ("👥 User Statistics", [
                ("Total Students", stats['total_students']),
                ("Active Borrowers", stats['issued_books'])
            ]),
            ("⚠️ Alerts", [
                ("Overdue Books", stats['overdue_books']),
                ("Books Out", stats['issued_books'])
            ])
        ]
        
        for section_title, items in sections:
            section_frame = tk.Frame(report_frame, bg=COLORS['bg_white'])
            section_frame.pack(fill='x', padx=30, pady=20)
            
            tk.Label(
                section_frame,
                text=section_title,
                font=('Segoe UI', 16, 'bold'),
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark'],
                anchor='w'
            ).pack(fill='x', pady=(0, 15))
            
            for label, value in items:
                item_frame = tk.Frame(section_frame, bg=COLORS['bg_light'])
                item_frame.pack(fill='x', pady=5)
                
                tk.Label(
                    item_frame,
                    text=label,
                    font=('Segoe UI', 12),
                    bg=COLORS['bg_light'],
                    fg=COLORS['text_dark'],
                    anchor='w'
                ).pack(side='left', padx=15, pady=10)
                
                tk.Label(
                    item_frame,
                    text=str(value),
                    font=('Segoe UI', 12, 'bold'),
                    bg=COLORS['bg_light'],
                    fg=COLORS['secondary'],
                    anchor='e'
                ).pack(side='right', padx=15, pady=10)
    
    def show_backup(self):
        """Show backup options"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Backup & Export",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 30))
        
        # Backup frame
        backup_frame = tk.Frame(self.content_frame, bg=COLORS['bg_white'], relief='solid', bd=1)
        backup_frame.pack(fill='both', expand=True, padx=100, pady=50)
        
        inner_frame = tk.Frame(backup_frame, bg=COLORS['bg_white'])
        inner_frame.pack(padx=50, pady=50)
        
        tk.Label(
            inner_frame,
            text="Export Data to CSV",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark']
        ).pack(pady=(0, 30))
        
        def export_data(table_name):
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                success, message = self.db.export_to_csv(table_name, filename)
                if success:
                    messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", message)
        
        # Export buttons
        buttons = [
            ("📚 Export Books", lambda: export_data('books')),
            ("👥 Export Students", lambda: export_data('students')),
            ("📋 Export Issues", lambda: export_data('issues'))
        ]
        
        for text, command in buttons:
            ModernButton(
                inner_frame,
                text,
                command,
                bg_color=COLORS['success']
            ).pack(pady=10, fill='x')
    
    def show_student_history(self, student_id):
        """Show QR code and history for a student"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Student History")
        dialog.geometry("800x600")
        dialog.configure(bg=COLORS['bg_white'])
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Title
        tk.Label(
            dialog,
            text="Student Issue History",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['bg_white']
        ).pack(pady=20)
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(f"Student ID: {student_id}")
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color=COLORS['primary'], back_color="white")
        qr_img = qr_img.resize((200, 200))
        
        # Convert to PhotoImage
        qr_photo = ImageTk.PhotoImage(qr_img)
        
        qr_label = tk.Label(dialog, image=qr_photo, bg=COLORS['bg_white'])
        qr_label.image = qr_photo  # Keep a reference
        qr_label.pack(pady=10)
        
        # History table
        table_frame = tk.Frame(dialog, bg=COLORS['bg_white'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('Book', 'Issue Date', 'Due Date', 'Return Date', 'Status', 'Fine')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill='both', expand=True)
        
        # Load history
        history = self.db.get_student_history(student_id)
        for record in history:
            tree.insert('', 'end', values=(
                record['title'],
                record['issue_date'],
                record['due_date'],
                record['return_date'] or 'N/A',
                record['status'],
                f"${record['fine'] + record['damage_charge']}"
            ))
    
    def logout(self):
        """Logout and return to login screen"""
        self.root.destroy()
        self.parent.deiconify()
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askokcancel("Quit", "Do you want to logout?"):
            self.logout()


class StudentDashboard:
    """Dashboard for students to view their issued books"""
    
    def __init__(self, parent, db_manager, user):
        self.parent = parent
        self.db = db_manager
        self.user = user
        
        self.root = tk.Toplevel(parent)
        self.root.title("Student Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['bg_light'])
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Top bar
        top_bar = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        top_bar.pack(fill='x')
        
        tk.Label(
            top_bar,
            text=f"Welcome, {self.user['name']}!",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['primary'],
            fg='white'
        ).pack(side='left', padx=20, pady=15)
        
        ModernButton(
            top_bar,
            "Logout",
            self.logout,
            bg_color=COLORS['accent']
        ).pack(side='right', padx=20)
        
        # Content
        content = tk.Frame(self.root, bg=COLORS['bg_light'])
        content.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Title
        tk.Label(
            content,
            text="My Issued Books",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        ).pack(pady=(0, 20))
        
        # QR Code
        qr_frame = tk.Frame(content, bg=COLORS['bg_white'], relief='solid', bd=1)
        qr_frame.pack(pady=20)
        
        tk.Label(
            qr_frame,
            text="My QR Code",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['bg_white']
        ).pack(pady=10)
        
        # Generate QR
        qr = qrcode.QRCode(version=1, box_size=8, border=4)
        qr.add_data(f"Student ID: {self.user['student_id']}\nName: {self.user['name']}\nEmail: {self.user['email']}")
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color=COLORS['primary'], back_color="white")
        qr_img = qr_img.resize((150, 150))
        qr_photo = ImageTk.PhotoImage(qr_img)
        
        qr_label = tk.Label(qr_frame, image=qr_photo, bg=COLORS['bg_white'])
        qr_label.image = qr_photo
        qr_label.pack(pady=10, padx=20)
        
        # History table
        table_frame = tk.Frame(content, bg=COLORS['bg_white'])
        table_frame.pack(fill='both', expand=True, pady=20)
        
        tk.Label(
            table_frame,
            text="Issue History",
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['bg_white']
        ).pack(pady=15)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('Book', 'Author', 'Issue Date', 'Due Date', 'Return Date', 'Status', 'Charges')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load history
        history = self.db.get_student_history(self.user['student_id'])
        for record in history:
            charges = record['fine'] + record['damage_charge']
            tree.insert('', 'end', values=(
                record['title'],
                record['author'],
                record['issue_date'],
                record['due_date'],
                record['return_date'] or 'Not Returned',
                record['status'].upper(),
                f"${charges:.2f}"
            ))
    
    def logout(self):
        """Logout"""
        self.root.destroy()
        self.parent.deiconify()
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askokcancel("Quit", "Do you want to logout?"):
            self.logout()


def main():
    """Main function"""
    # Create database manager
    db = DatabaseManager()
    
    # Create main window
    root = tk.Tk()
    root.deiconify()  # Show main window

    
    # Show login window
    LoginWindow(root, db)
    
    root.mainloop()


if __name__ == "__main__":
    main()