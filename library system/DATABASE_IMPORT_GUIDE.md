# Database Import Guide

## 📦 Complete Database Package

The `library_db.sql` file contains:
- ✅ Complete database structure (4 tables)
- ✅ 50+ sample books across multiple categories
- ✅ 30 sample students
- ✅ 3 librarian accounts
- ✅ Sample issue/return transactions
- ✅ Views for common queries
- ✅ Stored procedures
- ✅ Triggers for automatic updates
- ✅ Performance indexes

## 🚀 Quick Import Methods

### Method 1: MySQL Command Line (Recommended)

```bash
# Navigate to the directory containing library_db.sql
cd /path/to/your/files

# Import the database
mysql -u root -p < library_db.sql

# Enter your MySQL password when prompted
```

### Method 2: MySQL Workbench (GUI)

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Go to **Server** → **Data Import**
4. Select **Import from Self-Contained File**
5. Click **Browse** and select `library_db.sql`
6. Click **Start Import**
7. Wait for completion message

### Method 3: phpMyAdmin (Web Interface)

1. Open phpMyAdmin in your browser
2. Click on **Import** tab at the top
3. Click **Choose File** and select `library_db.sql`
4. Scroll down and click **Go**
5. Wait for "Import has been successfully finished"

### Method 4: Direct MySQL Client

```bash
# Login to MySQL
mysql -u root -p

# Source the SQL file
source /path/to/library_db.sql

# Or use the full path
source C:/Users/YourName/Downloads/library_db.sql

# Exit MySQL
exit;
```

## 🔍 Verification

After importing, verify the data:

```sql
-- Connect to database
USE library_db;

-- Check tables
SHOW TABLES;

-- Check counts
SELECT 'Books' AS Table_Name, COUNT(*) AS Count FROM books
UNION ALL
SELECT 'Students', COUNT(*) FROM students
UNION ALL
SELECT 'Librarians', COUNT(*) FROM librarians
UNION ALL
SELECT 'Issues', COUNT(*) FROM issues;

-- View statistics
SELECT * FROM library_stats;

-- View current issues
SELECT * FROM current_issues;

-- View overdue books
SELECT * FROM overdue_books;
```

Expected Results:
- **Books**: 50+ entries
- **Students**: 30 entries
- **Librarians**: 3 entries
- **Issues**: 20+ entries

## 📊 Database Structure

### Tables Created:

1. **books** - Library book catalog
   - book_id, title, author, isbn, category
   - quantity, available, added_date

2. **students** - Registered students
   - student_id, name, email, phone
   - address, registration_date

3. **librarians** - Admin/Librarian accounts
   - librarian_id, username, password (hashed)
   - full_name, email, role

4. **issues** - Book transactions
   - issue_id, book_id, student_id
   - issue_date, due_date, return_date
   - status, fine, damage_charge

### Views Created:

1. **current_issues** - All currently issued books
2. **overdue_books** - Books past due date
3. **library_stats** - Dashboard statistics
4. **popular_books** - Most issued books
5. **student_activity** - Student borrowing history

### Stored Procedures:

1. **GetStudentHistory(student_id)** - Get all issues for a student
2. **CalculateFine(issue_id)** - Calculate overdue fine

### Triggers:

1. **after_issue_insert** - Decrements available count
2. **after_issue_update** - Increments available count on return

## 🔐 Default Login Credentials

### Admin/Librarian Accounts:

| Username   | Password  | Name              | Role      |
|------------|-----------|-------------------|-----------|
| admin      | admin123  | Administrator     | admin     |
| librarian1 | admin123  | John Librarian    | librarian |
| librarian2 | admin123  | Sarah Manager     | librarian |

### Student Accounts (Email only - no password):

| Name          | Email                    |
|---------------|--------------------------|
| John Doe      | john.doe@email.com       |
| Jane Smith    | jane.smith@email.com     |
| Bob Johnson   | bob.johnson@email.com    |
| Alice Williams| alice.williams@email.com |
| Charlie Brown | charlie.brown@email.com  |
| ...and 25 more students |

## 📚 Sample Data Included

### Books by Category:

- **Fiction**: 15 books (classics + modern)
- **Programming**: 13 books (Python, Java, etc.)
- **Computer Science**: 8 books (AI, algorithms, etc.)
- **Mathematics**: 4 books
- **Science**: 3 books
- **Business**: 7 books
- **Self-Help**: 4 books

### Sample Transactions:

- **Active Issues**: 11 books currently issued
- **Overdue**: 4 books past due date (for testing)
- **Returned History**: 14 completed transactions
- **With Fines**: Several transactions with overdue fines
- **With Damage**: Some transactions with damage charges

## 🛠️ Troubleshooting

### Error: "Database already exists"
```sql
-- Drop existing database first
DROP DATABASE IF EXISTS library_db;

-- Then re-run the import
source library_db.sql;
```

### Error: "Access denied"
```sql
-- Grant permissions
GRANT ALL PRIVILEGES ON library_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Unknown database"
```sql
-- Make sure you're connected to MySQL
mysql -u root -p

-- Then source the file
source /path/to/library_db.sql;
```

### Error: "Table already exists"
```sql
-- The script handles this with DROP TABLE IF EXISTS
-- If issues persist, manually drop tables:
USE library_db;
DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS librarians;

-- Then re-import
```

## 🔄 Re-importing Database

To start fresh:

```sql
-- Method 1: Drop and recreate
DROP DATABASE IF EXISTS library_db;
source library_db.sql;

-- Method 2: Clear data only
USE library_db;
DELETE FROM issues;
DELETE FROM books;
DELETE FROM students;
DELETE FROM librarians;

-- Then re-import
```

## 📝 Customization

### Change Default Password:

```sql
-- Update admin password (SHA256 hash of 'newpassword')
UPDATE librarians 
SET password = SHA2('newpassword', 256) 
WHERE username = 'admin';
```

### Add More Sample Data:

```sql
-- Add books
INSERT INTO books (title, author, isbn, category, quantity, available)
VALUES ('Your Book', 'Author Name', '978-1234567890', 'Category', 3, 3);

-- Add students
INSERT INTO students (name, email, phone, address)
VALUES ('Student Name', 'email@example.com', '1234567890', 'Address');
```

### Modify Fine Rate:

The fine calculation is done in the Python application:
- Edit `library_management_system.py`
- Find: `fine = days_late * 5`
- Change `5` to your desired rate

## 💡 Pro Tips

1. **Backup First**: Before importing, backup any existing database
   ```bash
   mysqldump -u root -p library_db > backup.sql
   ```

2. **Check Permissions**: Ensure MySQL user has CREATE and INSERT privileges

3. **Character Encoding**: The database uses utf8mb4 for international characters

4. **Auto-increment**: IDs start from 1 and increment automatically

5. **Foreign Keys**: ON DELETE CASCADE means deleting a book/student deletes their issues

## 🎯 Next Steps After Import

1. ✅ Verify import was successful
2. ✅ Test login with admin credentials
3. ✅ Update MySQL password in Python app
4. ✅ Run the application: `python library_management_system.py`
5. ✅ Explore the sample data
6. ✅ Add your own books and students
7. ✅ Test issue/return functionality

## 📧 Sample Usage Scenarios

### Test Scenario 1: Issue a Book
1. Login as admin
2. Go to "Issue Book"
3. Select book: "Python Programming for Beginners"
4. Select student: John Doe
5. Issue for 14 days

### Test Scenario 2: Return Overdue Book
1. Go to "Return Book"
2. Select an overdue issue
3. Add damage charge if needed
4. See automatic fine calculation

### Test Scenario 3: View Student History
1. Go to "Students"
2. Double-click on "John Doe"
3. View QR code and issue history

### Test Scenario 4: Check Overdue
1. Go to "Overdue"
2. See list of overdue books
3. Note the calculated fines

### Test Scenario 5: Export Data
1. Go to "Backup"
2. Export Books/Students/Issues
3. Open CSV file in Excel

## 🔒 Security Notes

- Passwords are SHA256 hashed
- Use strong passwords in production
- Consider adding student password authentication
- Regular backups recommended
- Limit database user permissions

---

**Database Ready!** 🎉

You now have a fully populated library database with realistic sample data for testing all features of the Library Management System.
