-- ============================================================================
-- Library Management System Database
-- Complete SQL Dump with Structure and Sample Data
-- ============================================================================

-- Create and use database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- ============================================================================
-- Table: books
-- Stores information about all books in the library
-- ============================================================================

DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS books;

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(50) UNIQUE,
    category VARCHAR(100),
    quantity INT DEFAULT 1,
    available INT DEFAULT 1,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_category (category),
    INDEX idx_isbn (isbn)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Table: students
-- Stores information about registered students
-- ============================================================================

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Table: librarians
-- Stores librarian/admin accounts with hashed passwords
-- ============================================================================

DROP TABLE IF EXISTS librarians;

CREATE TABLE librarians (
    librarian_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(50) DEFAULT 'librarian',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Table: issues
-- Tracks book issues, returns, fines, and damages
-- ============================================================================

CREATE TABLE issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    student_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(50) DEFAULT 'issued',
    fine DECIMAL(10,2) DEFAULT 0,
    damage_charge DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_issue_date (issue_date),
    INDEX idx_due_date (due_date),
    INDEX idx_book_id (book_id),
    INDEX idx_student_id (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT SAMPLE DATA
-- ============================================================================

-- ============================================================================
-- Librarians/Admins (Password: admin123 - SHA256 hashed)
-- ============================================================================

INSERT INTO librarians (username, password, full_name, email, role) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrator', 'admin@library.com', 'admin'),
('librarian1', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'John Librarian', 'john@library.com', 'librarian'),
('librarian2', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Sarah Manager', 'sarah@library.com', 'librarian');

-- ============================================================================
-- Books - Fiction Category
-- ============================================================================

INSERT INTO books (title, author, isbn, category, quantity, available) VALUES
-- Classic Literature
('To Kill a Mockingbird', 'Harper Lee', '978-0061120084', 'Fiction', 5, 5),
('1984', 'George Orwell', '978-0451524935', 'Fiction', 4, 4),
('Pride and Prejudice', 'Jane Austen', '978-0141439518', 'Fiction', 3, 3),
('The Great Gatsby', 'F. Scott Fitzgerald', '978-0743273565', 'Fiction', 4, 4),
('Animal Farm', 'George Orwell', '978-0451526342', 'Fiction', 3, 3),
('Brave New World', 'Aldous Huxley', '978-0060850524', 'Fiction', 3, 3),
('The Catcher in the Rye', 'J.D. Salinger', '978-0316769174', 'Fiction', 2, 2),
('Lord of the Flies', 'William Golding', '978-0399501487', 'Fiction', 3, 3),
('Of Mice and Men', 'John Steinbeck', '978-0140177398', 'Fiction', 3, 3),
('The Hobbit', 'J.R.R. Tolkien', '978-0547928227', 'Fantasy', 5, 5),

-- Modern Fiction
('The Hunger Games', 'Suzanne Collins', '978-0439023481', 'Fiction', 4, 4),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', '978-0439708180', 'Fantasy', 6, 6),
('The Da Vinci Code', 'Dan Brown', '978-0307474278', 'Mystery', 3, 3),
('The Alchemist', 'Paulo Coelho', '978-0062315007', 'Fiction', 4, 4),
('Life of Pi', 'Yann Martel', '978-0156027328', 'Fiction', 2, 2),

-- ============================================================================
-- Books - Non-Fiction Category
-- ============================================================================

-- Science
('A Brief History of Time', 'Stephen Hawking', '978-0553380163', 'Science', 3, 3),
('Cosmos', 'Carl Sagan', '978-0345539434', 'Science', 2, 2),
('The Selfish Gene', 'Richard Dawkins', '978-0199291152', 'Science', 2, 2),
('Sapiens', 'Yuval Noah Harari', '978-0062316097', 'History', 5, 5),
('Educated', 'Tara Westover', '978-0399590504', 'Biography', 3, 3),

-- Self-Help
('Atomic Habits', 'James Clear', '978-0735211292', 'Self-Help', 4, 4),
('The 7 Habits of Highly Effective People', 'Stephen Covey', '978-1982137274', 'Self-Help', 3, 3),
('Think and Grow Rich', 'Napoleon Hill', '978-1585424337', 'Self-Help', 2, 2),
('How to Win Friends and Influence People', 'Dale Carnegie', '978-0671027032', 'Self-Help', 3, 3);

-- ============================================================================
-- Books - Programming & Technology
-- ============================================================================

INSERT INTO books (title, author, isbn, category, quantity, available) VALUES
('Python Programming for Beginners', 'John Smith', '978-1234567890', 'Programming', 6, 6),
('Clean Code', 'Robert C. Martin', '978-0132350884', 'Programming', 4, 4),
('The Pragmatic Programmer', 'Andrew Hunt', '978-0135957059', 'Programming', 3, 3),
('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033844', 'Computer Science', 5, 5),
('Design Patterns', 'Gang of Four', '978-0201633612', 'Programming', 3, 3),
('JavaScript: The Good Parts', 'Douglas Crockford', '978-0596517748', 'Programming', 4, 4),
('Database System Concepts', 'Abraham Silberschatz', '978-0078022159', 'Computer Science', 4, 4),
('Computer Networks', 'Andrew S. Tanenbaum', '978-0132126953', 'Computer Science', 3, 3),
('Artificial Intelligence: A Modern Approach', 'Stuart Russell', '978-0136042594', 'Computer Science', 4, 4),
('Operating System Concepts', 'Abraham Silberschatz', '978-1118063330', 'Computer Science', 4, 4),
('Python for Data Analysis', 'Wes McKinney', '978-1491957660', 'Programming', 5, 5),
('Machine Learning Yearning', 'Andrew Ng', '978-0999820001', 'Computer Science', 3, 3),
('Deep Learning', 'Ian Goodfellow', '978-0262035613', 'Computer Science', 3, 3),

-- ============================================================================
-- Books - Mathematics & Sciences
-- ============================================================================

('Calculus', 'James Stewart', '978-1285740621', 'Mathematics', 5, 5),
('Linear Algebra', 'Gilbert Strang', '978-0980232721', 'Mathematics', 4, 4),
('Discrete Mathematics', 'Kenneth Rosen', '978-0073383095', 'Mathematics', 4, 4),
('Probability and Statistics', 'Morris DeGroot', '978-0321500465', 'Mathematics', 3, 3),
('Physics for Scientists', 'Raymond Serway', '978-1133954057', 'Physics', 5, 5),
('Chemistry: The Central Science', 'Theodore Brown', '978-0134414232', 'Chemistry', 4, 4),
('Biology', 'Neil Campbell', '978-0134093413', 'Biology', 5, 5),

-- ============================================================================
-- Books - Business & Economics
-- ============================================================================

('The Lean Startup', 'Eric Ries', '978-0307887894', 'Business', 4, 4),
('Good to Great', 'Jim Collins', '978-0066620992', 'Business', 3, 3),
('Zero to One', 'Peter Thiel', '978-0804139298', 'Business', 3, 3),
('The Innovator''s Dilemma', 'Clayton Christensen', '978-1633691780', 'Business', 2, 2),
('Principles', 'Ray Dalio', '978-1501124020', 'Business', 3, 3),
('Economics', 'Paul Samuelson', '978-0073511290', 'Economics', 4, 4),
('Freakonomics', 'Steven Levitt', '978-0060731335', 'Economics', 3, 3);

-- ============================================================================
-- Students - Sample Data
-- ============================================================================

INSERT INTO students (name, email, phone, address) VALUES
-- Computer Science Students
('John Doe', 'john.doe@email.com', '1234567890', '123 Main Street, Apt 4B, New York, NY 10001'),
('Jane Smith', 'jane.smith@email.com', '0987654321', '456 Oak Avenue, Suite 200, Los Angeles, CA 90001'),
('Bob Johnson', 'bob.johnson@email.com', '5555555555', '789 Pine Road, Chicago, IL 60601'),
('Alice Williams', 'alice.williams@email.com', '4445556666', '321 Elm Street, Houston, TX 77001'),
('Charlie Brown', 'charlie.brown@email.com', '7778889999', '654 Maple Drive, Phoenix, AZ 85001'),

-- Engineering Students
('David Miller', 'david.miller@email.com', '1112223333', '987 Cedar Lane, Philadelphia, PA 19101'),
('Emma Davis', 'emma.davis@email.com', '2223334444', '147 Birch Court, San Antonio, TX 78201'),
('Frank Wilson', 'frank.wilson@email.com', '3334445555', '258 Walnut Way, San Diego, CA 92101'),
('Grace Martinez', 'grace.martinez@email.com', '4445556677', '369 Cherry Circle, Dallas, TX 75201'),
('Henry Anderson', 'henry.anderson@email.com', '5556667788', '741 Spruce Street, San Jose, CA 95101'),

-- Business Students
('Ivy Thomas', 'ivy.thomas@email.com', '6667778899', '852 Ash Boulevard, Austin, TX 78701'),
('Jack Taylor', 'jack.taylor@email.com', '7778889900', '963 Oak Park, Jacksonville, FL 32099'),
('Kate Moore', 'kate.moore@email.com', '8889990011', '159 Pine Plaza, Fort Worth, TX 76101'),
('Leo Jackson', 'leo.jackson@email.com', '9990001122', '357 Elm Estates, Columbus, OH 43201'),
('Mia White', 'mia.white@email.com', '1231231234', '486 Maple Manor, Charlotte, NC 28201'),

-- Science Students
('Nathan Harris', 'nathan.harris@email.com', '2342342345', '753 Cedar Creek, San Francisco, CA 94101'),
('Olivia Martin', 'olivia.martin@email.com', '3453453456', '864 Birch Bay, Indianapolis, IN 46201'),
('Peter Thompson', 'peter.thompson@email.com', '4564564567', '975 Walnut Woods, Seattle, WA 98101'),
('Quinn Garcia', 'quinn.garcia@email.com', '5675675678', '258 Cherry Chase, Denver, CO 80201'),
('Rachel Robinson', 'rachel.robinson@email.com', '6786786789', '369 Spruce Springs, Boston, MA 02101'),

-- Liberal Arts Students
('Samuel Clark', 'samuel.clark@email.com', '7897897890', '741 Ash Avenue, El Paso, TX 79901'),
('Tina Rodriguez', 'tina.rodriguez@email.com', '8908908901', '852 Oak Orchard, Detroit, MI 48201'),
('Uma Lewis', 'uma.lewis@email.com', '9019019012', '963 Pine Pointe, Memphis, TN 38101'),
('Victor Lee', 'victor.lee@email.com', '1011011011', '147 Elm End, Portland, OR 97201'),
('Wendy Walker', 'wendy.walker@email.com', '2022022022', '258 Maple Meadow, Oklahoma City, OK 73101'),

-- Graduate Students
('Xavier Hall', 'xavier.hall@email.com', '3033033033', '369 Cedar Court, Las Vegas, NV 89101'),
('Yara Allen', 'yara.allen@email.com', '4044044044', '741 Birch Bend, Louisville, KY 40201'),
('Zack Young', 'zack.young@email.com', '5055055055', '852 Walnut Walk, Baltimore, MD 21201'),
('Amy King', 'amy.king@email.com', '6066066066', '963 Cherry Crossing, Milwaukee, WI 53201'),
('Brian Wright', 'brian.wright@email.com', '7077077077', '147 Spruce Square, Albuquerque, NM 87101');

-- ============================================================================
-- Issues - Sample Active Issues
-- ============================================================================

INSERT INTO issues (book_id, student_id, issue_date, due_date, status) VALUES
-- Current issues (not overdue)
(1, 1, CURDATE() - INTERVAL 5 DAY, CURDATE() + INTERVAL 9 DAY, 'issued'),
(4, 2, CURDATE() - INTERVAL 3 DAY, CURDATE() + INTERVAL 11 DAY, 'issued'),
(10, 3, CURDATE() - INTERVAL 7 DAY, CURDATE() + INTERVAL 7 DAY, 'issued'),
(15, 5, CURDATE() - INTERVAL 2 DAY, CURDATE() + INTERVAL 12 DAY, 'issued'),
(20, 8, CURDATE() - INTERVAL 4 DAY, CURDATE() + INTERVAL 10 DAY, 'issued'),
(25, 12, CURDATE() - INTERVAL 6 DAY, CURDATE() + INTERVAL 8 DAY, 'issued'),
(30, 15, CURDATE() - INTERVAL 1 DAY, CURDATE() + INTERVAL 13 DAY, 'issued'),

-- Overdue issues (for testing overdue feature)
(2, 4, CURDATE() - INTERVAL 20 DAY, CURDATE() - INTERVAL 6 DAY, 'issued'),
(7, 6, CURDATE() - INTERVAL 18 DAY, CURDATE() - INTERVAL 4 DAY, 'issued'),
(12, 9, CURDATE() - INTERVAL 25 DAY, CURDATE() - INTERVAL 11 DAY, 'issued'),
(18, 11, CURDATE() - INTERVAL 22 DAY, CURDATE() - INTERVAL 8 DAY, 'issued');

-- Update book availability for issued books
UPDATE books SET available = available - 1 WHERE book_id IN (1, 2, 4, 7, 10, 12, 15, 18, 20, 25, 30);

-- ============================================================================
-- Issues - Sample Returned Books (History)
-- ============================================================================

INSERT INTO issues (book_id, student_id, issue_date, due_date, return_date, status, fine, damage_charge) VALUES
-- Returned on time
(3, 1, CURDATE() - INTERVAL 30 DAY, CURDATE() - INTERVAL 16 DAY, CURDATE() - INTERVAL 18 DAY, 'returned', 0, 0),
(5, 2, CURDATE() - INTERVAL 25 DAY, CURDATE() - INTERVAL 11 DAY, CURDATE() - INTERVAL 13 DAY, 'returned', 0, 0),
(8, 3, CURDATE() - INTERVAL 40 DAY, CURDATE() - INTERVAL 26 DAY, CURDATE() - INTERVAL 28 DAY, 'returned', 0, 0),

-- Returned late (with fines)
(6, 4, CURDATE() - INTERVAL 35 DAY, CURDATE() - INTERVAL 21 DAY, CURDATE() - INTERVAL 16 DAY, 'returned', 25.00, 0),
(9, 5, CURDATE() - INTERVAL 45 DAY, CURDATE() - INTERVAL 31 DAY, CURDATE() - INTERVAL 28 DAY, 'returned', 15.00, 0),
(11, 6, CURDATE() - INTERVAL 50 DAY, CURDATE() - INTERVAL 36 DAY, CURDATE() - INTERVAL 32 DAY, 'returned', 20.00, 0),

-- Returned with damage
(13, 7, CURDATE() - INTERVAL 28 DAY, CURDATE() - INTERVAL 14 DAY, CURDATE() - INTERVAL 15 DAY, 'returned', 0, 10.00),
(16, 10, CURDATE() - INTERVAL 38 DAY, CURDATE() - INTERVAL 24 DAY, CURDATE() - INTERVAL 22 DAY, 'returned', 10.00, 15.00),

-- More history
(14, 13, CURDATE() - INTERVAL 60 DAY, CURDATE() - INTERVAL 46 DAY, CURDATE() - INTERVAL 47 DAY, 'returned', 0, 0),
(17, 14, CURDATE() - INTERVAL 55 DAY, CURDATE() - INTERVAL 41 DAY, CURDATE() - INTERVAL 43 DAY, 'returned', 0, 0),
(19, 16, CURDATE() - INTERVAL 48 DAY, CURDATE() - INTERVAL 34 DAY, CURDATE() - INTERVAL 36 DAY, 'returned', 0, 0),
(21, 18, CURDATE() - INTERVAL 42 DAY, CURDATE() - INTERVAL 28 DAY, CURDATE() - INTERVAL 30 DAY, 'returned', 0, 0),
(23, 20, CURDATE() - INTERVAL 65 DAY, CURDATE() - INTERVAL 51 DAY, CURDATE() - INTERVAL 52 DAY, 'returned', 0, 0),
(26, 22, CURDATE() - INTERVAL 70 DAY, CURDATE() - INTERVAL 56 DAY, CURDATE() - INTERVAL 58 DAY, 'returned', 0, 0),
(28, 25, CURDATE() - INTERVAL 75 DAY, CURDATE() - INTERVAL 61 DAY, CURDATE() - INTERVAL 62 DAY, 'returned', 0, 0);

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- View: Current Issues with Details
CREATE OR REPLACE VIEW current_issues AS
SELECT 
    i.issue_id,
    b.title AS book_title,
    b.author AS book_author,
    s.name AS student_name,
    s.email AS student_email,
    i.issue_date,
    i.due_date,
    DATEDIFF(CURDATE(), i.due_date) AS days_overdue,
    CASE 
        WHEN CURDATE() > i.due_date THEN 'Overdue'
        ELSE 'On Time'
    END AS status_text
FROM issues i
JOIN books b ON i.book_id = b.book_id
JOIN students s ON i.student_id = s.student_id
WHERE i.status = 'issued'
ORDER BY i.due_date;

-- View: Overdue Books
CREATE OR REPLACE VIEW overdue_books AS
SELECT 
    i.issue_id,
    b.title AS book_title,
    s.name AS student_name,
    s.email AS student_email,
    s.phone AS student_phone,
    i.issue_date,
    i.due_date,
    DATEDIFF(CURDATE(), i.due_date) AS days_overdue,
    DATEDIFF(CURDATE(), i.due_date) * 5 AS calculated_fine
FROM issues i
JOIN books b ON i.book_id = b.book_id
JOIN students s ON i.student_id = s.student_id
WHERE i.status = 'issued' AND i.due_date < CURDATE()
ORDER BY days_overdue DESC;

-- View: Library Statistics
CREATE OR REPLACE VIEW library_stats AS
SELECT 
    (SELECT COUNT(*) FROM books) AS total_books,
    (SELECT SUM(quantity) FROM books) AS total_copies,
    (SELECT SUM(available) FROM books) AS available_copies,
    (SELECT COUNT(*) FROM students) AS total_students,
    (SELECT COUNT(*) FROM issues WHERE status = 'issued') AS books_issued,
    (SELECT COUNT(*) FROM issues WHERE status = 'issued' AND due_date < CURDATE()) AS books_overdue,
    (SELECT SUM(fine + damage_charge) FROM issues WHERE status = 'returned') AS total_fines_collected;

-- View: Popular Books
CREATE OR REPLACE VIEW popular_books AS
SELECT 
    b.book_id,
    b.title,
    b.author,
    b.category,
    COUNT(i.issue_id) AS times_issued
FROM books b
LEFT JOIN issues i ON b.book_id = i.book_id
GROUP BY b.book_id, b.title, b.author, b.category
ORDER BY times_issued DESC;

-- View: Student Activity
CREATE OR REPLACE VIEW student_activity AS
SELECT 
    s.student_id,
    s.name,
    s.email,
    COUNT(i.issue_id) AS total_issues,
    SUM(CASE WHEN i.status = 'issued' THEN 1 ELSE 0 END) AS current_issues,
    SUM(i.fine + i.damage_charge) AS total_charges
FROM students s
LEFT JOIN issues i ON s.student_id = i.student_id
GROUP BY s.student_id, s.name, s.email
ORDER BY total_issues DESC;

-- ============================================================================
-- Stored Procedures
-- ============================================================================

-- Procedure: Get Student History
DELIMITER //

CREATE PROCEDURE GetStudentHistory(IN p_student_id INT)
BEGIN
    SELECT 
        i.issue_id,
        b.title AS book_title,
        b.author,
        i.issue_date,
        i.due_date,
        i.return_date,
        i.status,
        i.fine,
        i.damage_charge,
        (i.fine + i.damage_charge) AS total_charges
    FROM issues i
    JOIN books b ON i.book_id = b.book_id
    WHERE i.student_id = p_student_id
    ORDER BY i.issue_date DESC;
END //

DELIMITER ;

-- Procedure: Calculate Fine
DELIMITER //

CREATE PROCEDURE CalculateFine(IN p_issue_id INT)
BEGIN
    DECLARE v_due_date DATE;
    DECLARE v_return_date DATE;
    DECLARE v_days_late INT;
    DECLARE v_fine DECIMAL(10,2);
    
    SELECT due_date, return_date 
    INTO v_due_date, v_return_date
    FROM issues 
    WHERE issue_id = p_issue_id;
    
    IF v_return_date > v_due_date THEN
        SET v_days_late = DATEDIFF(v_return_date, v_due_date);
        SET v_fine = v_days_late * 5.00;
    ELSE
        SET v_fine = 0;
    END IF;
    
    SELECT v_fine AS calculated_fine, v_days_late AS days_late;
END //

DELIMITER ;

-- ============================================================================
-- Triggers
-- ============================================================================

-- Trigger: Update book availability when book is issued
DELIMITER //

CREATE TRIGGER after_issue_insert
AFTER INSERT ON issues
FOR EACH ROW
BEGIN
    IF NEW.status = 'issued' THEN
        UPDATE books 
        SET available = available - 1 
        WHERE book_id = NEW.book_id AND available > 0;
    END IF;
END //

DELIMITER ;

-- Trigger: Update book availability when book is returned
DELIMITER //

CREATE TRIGGER after_issue_update
AFTER UPDATE ON issues
FOR EACH ROW
BEGIN
    IF OLD.status = 'issued' AND NEW.status = 'returned' THEN
        UPDATE books 
        SET available = available + 1 
        WHERE book_id = NEW.book_id;
    END IF;
END //

DELIMITER ;

-- ============================================================================
-- Indexes for Performance
-- ============================================================================

-- Already created in table definitions, but listing here for reference:
-- INDEX idx_title on books(title)
-- INDEX idx_author on books(author)
-- INDEX idx_category on books(category)
-- INDEX idx_isbn on books(isbn)
-- INDEX idx_email on students(email)
-- INDEX idx_name on students(name)
-- INDEX idx_username on librarians(username)
-- INDEX idx_status on issues(status)
-- INDEX idx_issue_date on issues(issue_date)
-- INDEX idx_due_date on issues(due_date)
-- INDEX idx_book_id on issues(book_id)
-- INDEX idx_student_id on issues(student_id)

-- ============================================================================
-- Grant Permissions (Adjust as needed)
-- ============================================================================

-- GRANT ALL PRIVILEGES ON library_db.* TO 'library_user'@'localhost' IDENTIFIED BY 'your_password';
-- FLUSH PRIVILEGES;

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Verify data insertion
SELECT 'Books Count:' AS Info, COUNT(*) AS Count FROM books
UNION ALL
SELECT 'Students Count:', COUNT(*) FROM students
UNION ALL
SELECT 'Librarians Count:', COUNT(*) FROM librarians
UNION ALL
SELECT 'Active Issues:', COUNT(*) FROM issues WHERE status = 'issued'
UNION ALL
SELECT 'Returned Books:', COUNT(*) FROM issues WHERE status = 'returned'
UNION ALL
SELECT 'Overdue Books:', COUNT(*) FROM issues WHERE status = 'issued' AND due_date < CURDATE();

-- Show library statistics
SELECT * FROM library_stats;

-- Show current issues
SELECT * FROM current_issues LIMIT 10;

-- Show overdue books
SELECT * FROM overdue_books;

-- ============================================================================
-- END OF DATABASE DUMP
-- ============================================================================

-- Database created successfully!
-- Default Admin Login:
--   Username: admin
--   Password: admin123
--
-- Sample Student Logins (email only):
--   john.doe@email.com
--   jane.smith@email.com
--   bob.johnson@email.com
-- ============================================================================
