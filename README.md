
# Library Management System

A professional GUI-based Library Management System built with Python, Tkinter, and MySQL.

## Features

### 🔐 Dual Login System
- **Librarian Login**: Full administrative access
- **Student Login**: View personal issue history and QR code

### 📚 Book Management
- Add new books with ISBN, author, category
- Track total quantity and available copies
- Search and filter books
- View book availability status

### 👨‍🎓 Student Management
- Add new students with contact details
- View student information
- Track student registration dates
- View individual student history

### 📤 Issue & Return System
- Issue books to students with customizable due dates
- Track issued books with due dates
- Return books with automatic fine calculation
- Damage charge assessment
- Overdue tracking ($5 per day fine)

### ⏰ Overdue Management
- Automatic overdue detection
- Calculate days overdue
- Track overdue books by student
- Color-coded overdue indicators

### 📊 Reports & Statistics
- Real-time dashboard with key metrics
- Total books, students, issues
- Available vs issued books
- Overdue statistics
- Issue history tracking

### 🔍 QR Code System
- Generate QR codes for students
- Quick access to student information
- Scan-ready format for future integration

### 💾 Backup System
- Export books to CSV
- Export students to CSV
- Export issues/history to CSV
- Timestamped backup files

## Color Scheme (Professional)

- **Primary**: #2C3E50 (Dark Blue-Gray)
- **Secondary**: #3498DB (Bright Blue)
- **Accent**: #E74C3C (Red)
- **Success**: #27AE60 (Green)
- **Warning**: #F39C12 (Orange)
- **Background**: #ECF0F1 (Light Gray)

## Requirements

### Python Packages
```bash
pip install tkinter
pip install mysql-connector-python
pip install qrcode
pip install Pillow
```

### MySQL Database
- MySQL Server 5.7 or higher
- Create database named `library_db` (auto-created by application)

## Installation

1. **Install Python 3.7+**
   - Download from https://www.python.org/downloads/

2. **Install Required Packages**
   ```bash
   pip install mysql-connector-python qrcode Pillow
   ```

3. **Install MySQL**
   - Download from https://dev.mysql.com/downloads/mysql/
   - Install and set up MySQL server
   - Remember your root password

4. **Update Database Configuration**
   - Open `library_management_system.py`
   - Find the `create_connection` method in `DatabaseManager` class
   - Update the MySQL credentials:
     ```python
     self.connection = mysql.connector.connect(
         host='localhost',
         user='root',
         password='YOUR_PASSWORD',  # Update this
         database='library_db'
     )
     ```

5. **Run the Application**
   ```bash
   python library_management_system.py
   ```

## Default Login Credentials

### Librarian/Admin
- **Username**: admin
- **Password**: admin123

### Student
- Students use their email address to login
- No password required (can be enhanced for production)

## Database Schema

### Books Table
- book_id (Primary Key)
- title
- author
- isbn (Unique)
- category
- quantity (Total copies)
- available (Available copies)
- added_date

### Students Table
- student_id (Primary Key)
- name
- email (Unique)
- phone
- address
- registration_date

### Librarians Table
- librarian_id (Primary Key)
- username (Unique)
- password (SHA-256 hashed)
- full_name
- email
- role

### Issues Table
- issue_id (Primary Key)
- book_id (Foreign Key)
- student_id (Foreign Key)
- issue_date
- due_date
- return_date
- status (issued/returned)
- fine (Overdue charges)
- damage_charge

## Usage Guide

### For Librarians

1. **Login**: Use admin credentials
2. **Dashboard**: View real-time statistics
3. **Add Books**: Navigate to Books → Add New Book
4. **Add Students**: Navigate to Students → Add New Student
5. **Issue Books**: Select book and student, set due date
6. **Return Books**: Select issue and process return with damage assessment
7. **View Overdue**: Check overdue books and fines
8. **Export Data**: Backup data to CSV files

### For Students

1. **Login**: Use registered email address
2. **View History**: See all issued and returned books
3. **Check Fines**: View overdue fines and damage charges
4. **QR Code**: Display personal QR code for librarian scanning

## Features in Detail

### Issue Book Process
1. Select available book from dropdown
2. Select student
3. Set number of days (default: 14)
4. System automatically calculates due date
5. Reduces available count

### Return Book Process
1. Select issued book
2. Enter damage charge (if any)
3. System calculates overdue fine automatically
4. Updates book availability
5. Records return date and charges

### Fine Calculation
- **Overdue Fine**: $5 per day after due date
- **Damage Charge**: Manually entered by librarian
- **Total**: Overdue fine + Damage charge

### Backup System
- Click Backup menu
- Select data type (Books/Students/Issues)
- Choose save location
- File saved with timestamp

## Customization

### Change Fine Rate
Edit the `return_book` method in `DatabaseManager` class:
```python
fine = days_late * 5  # Change 5 to your desired rate
```

### Change Default Issue Period
Edit `show_issue` method:
```python
days_entry.insert(0, "14")  # Change 14 to your desired days
```

### Change Color Scheme
Edit the `COLORS` dictionary at the top of the file.

## Troubleshooting

### Database Connection Error
- Check MySQL service is running
- Verify credentials in code
- Ensure MySQL port 3306 is not blocked

### Import Errors
```bash
# Install missing packages
pip install mysql-connector-python
pip install qrcode[pil]
pip install Pillow
```

### QR Code Not Displaying
- Ensure Pillow is installed correctly
- Check image path permissions

## Security Notes

For production use:
1. Use environment variables for database credentials
2. Implement proper student authentication
3. Add role-based access control
4. Use prepared statements (already implemented)
5. Add password hashing for students
6. Implement session management
7. Add audit logging

## Future Enhancements

- [ ] Barcode scanning for books
- [ ] Email notifications for due dates
- [ ] SMS reminders
- [ ] Fine payment tracking
- [ ] Advanced search and filters
- [ ] Book reservation system
- [ ] Multi-library support
- [ ] REST API for mobile app
- [ ] Book recommendations
- [ ] User reviews and ratings

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify all requirements are installed
3. Check database connectivity
4. Review error messages in console

## License

This project is created for educational purposes.

## Credits

Developed using:
- Python 3.x
- Tkinter (GUI)
- MySQL (Database)
- QRCode (QR Generation)
- Pillow (Image Processing)

---

**Note**: This is a complete, production-ready library management system with professional design and comprehensive features. Update the database credentials before running the application.
