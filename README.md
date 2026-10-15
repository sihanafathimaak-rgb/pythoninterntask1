Student Record Management System

A Python-based application for managing student records using SQLite database storage.

Features

- Add new student records
- View all student details
- Search students by roll number or name
- Update existing student information
- Delete student records with confirmation
- Validate student input details
- Store data persistently using SQLite
- Handle duplicate records and database errors

Tech Stack

- Programming Language: Python
- Database: SQLite
- Libraries: "sqlite3", "re", "math", "dataclasses", "pathlib"
- Development Tool: Visual Studio Code
- Version Control: Git and GitHub

Project Structure

Student-Record-Management/
├── student_records.py
├── README.md
└── students.db

"students.db" is created automatically when the application runs.

Setup Instructions

Prerequisites

- Python 3.9 or later
- Visual Studio Code (recommended)

Installation and Execution

1. Clone or download this repository.
2. Open the project folder in Visual Studio Code.
3. Open the terminal in the project directory.
4. Run the following command:

python student_records.py

5. Select an option from the menu to manage student records.

Menu Options

Option| Description
1| Add Student
2| View All Students
3| Search Student
4| Update Student
5| Delete Student
0| Exit Application

Database

The application uses SQLite to store student details, including roll number, name, email, GPA, and course. Records remain saved between program executions.

Future Enhancements

- Export records to CSV
- Add automated unit testing
- Implement a graphical user interface
- Add advanced search and sorting

Author

Sihana Fathima A.K.

Developed as a Python project to practise database management, CRUD operations, input validation, and exception handling.
