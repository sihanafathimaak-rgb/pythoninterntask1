Student Record Management System
A menu-driven student record management application built with Python and SQLite. It allows users to create, view, search, update, and delete student records through a simple command-line interface.
Features
Add student records with roll number, name, email, GPA, and course.
View all students in a formatted table.
Search students using a full or partial roll number or name.
Update student details while keeping any fields left blank unchanged.
Delete student records after confirmation.
Input validation for roll number, name, email, GPA, and course.
Persistent storage using SQLite, so records remain after the program closes.
Error handling for duplicate roll numbers, missing students, and database errors.
Tech Stack
Python
SQLite (sqlite3)
Regular expressions (re)
Dataclasses (dataclasses)
Context managers (contextlib)
Project Structure
Student-Record-Management/
├── student_records.py
└── students.db              # Created automatically when the app runs
students.db is generated automatically. Do not commit your personal/local database unless you intentionally want to share its contents. Add it to .gitignore for a clean repository.
Requirements
Python 3.9 or later recommended
No third-party Python packages are required; the project uses Python's standard library.
Run the Project
Clone or download this repository.
Open a terminal in the project folder.
Run:
python student_records.py
Select an option from the menu:
1 — Add student
2 — View all students
3 — Search
4 — Update student
5 — Delete student
0 — Exit
Data Storage
The application stores records in students.db, in a table named students. The database file is created next to student_records.py.
The version configured for an empty database should not insert sample records automatically. If an older students.db already contains records, those records remain until they are removed from the database.
Validation Rules
Roll number: 3–15 characters; letters, digits, and hyphens. It is converted to uppercase.
Name: 2–60 characters; letters and common punctuation.
Email: checked against a basic email-format pattern and stored in lowercase.
GPA: numeric value from 0 to 10 by default, rounded to two decimal places.
Course: 2–50 characters.
Important Notes
Roll numbers are unique because roll_no is the table's primary key.
Search is case-insensitive and supports partial matches in roll number or name.
The app is a command-line learning project; it is not a web application.
Back up students.db before manually deleting or changing database files.
Future Improvements
Add unit tests.
Add sorting and filtering options.
Export student records to CSV.
Add a graphical or web-based interface.
Add user authentication and role-based access.
Support configurable GPA scales.
Author
Sihana Fathima A.K.
A Python project demonstrating CRUD operations, input validation, SQLite database handling, and command-line application design.
