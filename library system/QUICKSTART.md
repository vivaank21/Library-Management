# Quick Start Guide - Library Management System

## Step-by-Step Installation

### 1. Prerequisites
- Python 3.7 or higher installed
- MySQL Server installed and running
- Internet connection for package installation

### 2. Install Python Packages

Open terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install mysql-connector-python
pip install qrcode[pil]
pip install Pillow
```

### 3. Setup Database

**Option A: Automatic Setup (Recommended)**

Run the setup script:
```bash
python setup_database.py
```

Enter your MySQL credentials when prompted.

**Option B: Manual Setup**

1. Open MySQL Workbench or command line
2. Run these commands:

```sql
CREATE DATABASE library_db;
USE library_db;

-- Tables will be created automatically by the application
```

### 4. Configure Database Connection

Edit `library_management_system.py`:

Find line ~50 (in `create_connection` method):

```python
self.connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # ADD YOUR MYSQL PASSWORD HERE
    database='library_db'
)
```

### 5. Run the Application

```bash
python library_management_system.py
```

## First Login

### Librarian Login
- Username: `admin`
- Password: `admin123`

### Student Login (Sample Data)
- Email: `john.doe@email.com`
- Email: `jane.smith@email.com`
- Email: `bob.johnson@email.com`

## Common Issues & Solutions

### Issue 1: MySQL Connection Error
**Error**: "Can't connect to MySQL server"

**Solution**:
1. Check if MySQL is running:
   - Windows: Open Services, look for MySQL
   - Mac/Linux: `sudo service mysql status`
2. Verify MySQL credentials
3. Check if port 3306 is available

### Issue 2: Module Not Found
**Error**: "ModuleNotFoundError: No module named 'mysql'"

**Solution**:
```bash
pip install mysql-connector-python
```

### Issue 3: QR Code Error
**Error**: "No module named 'PIL'"

**Solution**:
```bash
pip install Pillow
pip install qrcode[pil]
```

### Issue 4: Database Creation Error
**Error**: "Access denied for user"

**Solution**:
1. Login to MySQL as root
2. Grant privileges:
```sql
GRANT ALL PRIVILEGES ON library_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## Basic Operations

### Adding a Book
1. Login as librarian
2. Click "📖 Books"
3. Click "➕ Add New Book"
4. Fill in details:
   - Title: Book name
   - Author: Author name
   - ISBN: International Standard Book Number
   - Category: Book category
   - Quantity: Number of copies
5. Click "Save"

### Adding a Student
1. Login as librarian
2. Click "👨‍🎓 Students"
3. Click "➕ Add New Student"
4. Fill in details:
   - Name: Student name
   - Email: Student email (used for login)
   - Phone: Contact number
   - Address: Student address
5. Click "Save"

### Issuing a Book
1. Login as librarian
2. Click "📤 Issue Book"
3. Select book from dropdown (shows availability)
4. Select student from dropdown
5. Set number of days (default: 14)
6. Click "Issue Book"

### Returning a Book
1. Login as librarian
2. Click "📥 Return Book"
3. Select issued book from list
4. Click "Return Selected Book"
5. Enter damage charge (if any)
6. Click "Process Return"
7. System automatically calculates overdue fine

### Viewing Reports
1. Login as librarian
2. Click "📊 Reports"
3. View statistics:
   - Total books
   - Available books
   - Total students
   - Issued books
   - Overdue books

### Backing Up Data
1. Login as librarian
2. Click "💾 Backup"
3. Choose data type:
   - Books
   - Students
   - Issues
4. Select save location
5. File saved with timestamp

## Features Overview

### Dashboard (🏠 Home)
- Real-time statistics cards
- Recent issue activity
- Color-coded metrics
- Quick overview

### Books Management (📖 Books)
- View all books in table format
- See availability status
- Add new books
- Search functionality

### Student Management (👨‍🎓 Students)
- View all students
- Add new students
- Double-click to view history
- QR code generation

### Issue System (📤 Issue Book)
- Smart book selection (only available books)
- Student selection
- Customizable due dates
- Real-time availability update

### Return System (📥 Return Book)
- View all issued books
- Overdue indicator
- Damage assessment
- Automatic fine calculation

### Overdue Tracking (⏰ Overdue)
- Color-coded overdue list
- Days overdue calculation
- Student information
- Fine calculation ($5/day)

### Reports (📊 Reports)
- Library collection stats
- User statistics
- Alert system
- Detailed breakdown

### Backup (💾 Backup)
- Export to CSV
- Books backup
- Students backup
- Issues history backup
- Timestamped files

### Student Dashboard
- View issued books
- Check due dates
- See fine amounts
- Personal QR code
- Complete issue history

## Keyboard Shortcuts

- **Double-click** on student: View history
- **Enter** in forms: Submit
- **Escape** in dialogs: Close

## Tips for Best Use

1. **Regular Backups**: Export data weekly
2. **Update Due Dates**: Adjust based on book type
3. **Check Overdue**: Review daily
4. **Damage Assessment**: Be consistent with charges
5. **Student QR Codes**: Print for quick scanning
6. **Search Books**: Use search feature for large collections
7. **Monitor Statistics**: Check dashboard regularly

## Security Best Practices

1. **Change Default Password**: Change admin password after first login
2. **Regular Backups**: Keep CSV backups secure
3. **Database Security**: Use strong MySQL passwords
4. **Access Control**: Don't share admin credentials
5. **Student Verification**: Verify student identity before issuing

## Getting Help

If you encounter issues:

1. Check this guide first
2. Review error messages
3. Check MySQL connection
4. Verify all packages installed
5. Check Python version (3.7+)

## Next Steps

After setup:

1. ✓ Change admin password
2. ✓ Add your books
3. ✓ Add your students
4. ✓ Configure backup schedule
5. ✓ Test issue/return process
6. ✓ Customize fine rates if needed
7. ✓ Print student QR codes

## Contact & Support

For additional help:
- Check README.md for detailed documentation
- Review database schema
- Check MySQL logs for database errors
- Review Python console for application errors

---

**Congratulations!** 🎉 You're ready to use the Library Management System!

Start by logging in as admin and exploring the features.
