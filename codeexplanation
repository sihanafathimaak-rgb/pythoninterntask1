STUDENT RECORD MANAGEMENT SYSTEM
Technical Documentation and Code Explanation
Python • SQLite • Command-Line Application
1. Project Overview
The Student Record Management System is a command-line application developed in Python. It allows users to add, view, search, update, and delete student records. SQLite provides local persistent storage, while input validation and exception handling improve data consistency and reliability.
2. Objectives
    • Implement the core Create, Read, Update, and Delete (CRUD) operations.
    • Store student information persistently in a local relational database.
    • Validate user input before storing or updating records.
    • Separate data-access operations from command-line interaction.
    • Handle common data and database errors with clear messages.
3. Technologies and Modules
Python: Implements application logic, validation, menu handling, and record operations.
sqlite3: Connects Python to SQLite and executes SQL statements.
re: Uses regular expressions to validate roll-number and email formats.
math: Checks that GPA values are finite numbers.
time: Creates timestamped backup names when a database is identified as corrupted.
dataclasses.dataclass: Defines a concise data model for student records.
contextlib.contextmanager: Creates a managed database-session context.
pathlib.Path: Builds file-system paths in a platform-independent way.
4. Application Configuration
`DB_FILE` identifies the `students.db` file in the same directory as the Python script. `MAX_GPA` sets the upper GPA limit to 10.0 by default. It can be changed to 4.0 if the application is intended for a four-point scale.
5. Student Data Model
The `Student` dataclass represents one student using five fields: `roll_no`, `name`, `email`, `gpa`, and `course`. A Student object groups the values for a single record and makes it easier to pass student data between the interface and repository.
6. Input Validation
The custom `ValidationError` exception is used when user input does not satisfy a validation rule. The `ask()` helper catches this exception, displays the message, and asks for input again.
`validate_roll_no(raw)` — Trims surrounding whitespace, converts the value to uppercase, and checks it against `ROLL_RE`. The accepted format is 3–15 characters containing letters, digits, or hyphens.
`validate_name(raw)` — Normalizes repeated whitespace and checks that the name is 2–60 characters long. It permits alphabetic characters and selected punctuation.
`validate_email(raw)` — Trims whitespace, converts the address to lowercase, and checks it against a regular-expression pattern. This is a format check, not proof that the address exists.
`validate_gpa(raw)` — Converts input to a floating-point number, rejects non-numeric and non-finite values, enforces the configured range, and rounds the result to two decimal places.
`validate_course(raw)` — Normalizes whitespace and checks that the course name contains 2–50 characters.
7. Database Schema
The `SCHEMA` SQL statement creates the `students` table if it does not already exist. `roll_no` is the primary key, which prevents duplicate roll numbers. The `NOT NULL` constraints require values for the main fields, and the GPA check constraint rejects negative values at the database level. Application validation additionally enforces the configured upper limit.
8. Repository Layer
The `StudentRepository` class encapsulates database access. This separation keeps SQL operations out of most of the command-line functions and makes the program easier to maintain.
`__init__(db_path)` — Stores the database path and initializes or checks the database.
`_session()` — Opens a SQLite connection, configures rows to be addressable by column name, commits successful operations, rolls back recognized errors, and closes the connection.
`_init_db()` — Runs `PRAGMA quick_check`, creates the table if necessary, and checks that the expected table can be queried.
`reset_corrupt_database()` — Moves a damaged database file to a timestamped backup name rather than deleting it, then initializes a fresh database.
`_row(row)` — Converts a database row into a `Student` object.
`add(student)` — Executes an `INSERT` statement using parameter placeholders. Duplicate primary keys are converted to `DuplicateStudentError`.
`get(roll_no)` — Retrieves one record by exact roll number. If no record exists, it raises `StudentNotFoundError`.
`list_all()` — Retrieves all records ordered by roll number and converts each row into a `Student` object.
`search(query)` — Performs a case-insensitive partial match against roll numbers and student names.
`update(roll_no, **changes)` — Confirms that the student exists and applies the supplied field values with an SQL `UPDATE` statement.
`delete(roll_no)` — Deletes the record matching the supplied roll number and raises an error if no record was deleted.
9. Exception Types
`StorageError` is the base exception for storage-related problems. `DuplicateStudentError` identifies an existing roll number, `StudentNotFoundError` indicates that a requested record does not exist, and `CorruptDatabaseError` reports database integrity or corruption issues. The interface catches storage errors and displays readable messages.
10. Command-Line Interface
`MENU` — Stores the menu text displayed to the user.
`ask(prompt, validator, keep=None)` — Reads input and applies a validation function. Invalid input triggers an error message and another prompt. During updates, pressing Enter can preserve the current value when `keep` is supplied.
`print_table(students)` — Displays a formatted table or a no-records message, then prints the number of records.
`add_student(repo)` — Collects and validates a new student's fields, checks for an existing roll number, creates a `Student` object, and saves it.
`view_all(repo)` — Fetches all records and passes them to `print_table()`.
`search_students(repo)` — Reads a search term, rejects empty input, and displays matching records.
`update_student(repo)` — Loads the current record, displays existing values, accepts replacement values, and retains values for fields left blank.
`delete_student(repo)` — Finds the record and requests confirmation. The record is deleted only when the user enters `y`.
`ACTIONS` — Maps menu choices to their corresponding functions, allowing the main loop to dispatch user selections.
11. Application Startup and Main Loop
`open_repository()` opens the database and handles storage errors. If the database is corrupted, it asks whether the user wants to preserve the damaged file as a backup and start a fresh database. `main()` opens the repository, repeatedly displays the menu, and calls the selected action. Option `0` exits the program. `KeyboardInterrupt` and `EOFError` are handled to support cancellation or end-of-input. The `if __name__ == '__main__':` guard starts the menu only when the script is executed directly.
12. Typical Execution Flow
    1. The application opens or initializes `students.db`.
    2. The menu is displayed and the user selects an operation.
    3. The interface collects and validates the required input.
    4. The repository executes the relevant SQL operation.
    5. SQLite commits successful changes so records persist between runs.
    6. The interface displays the result or an error message.
13. Running the Application
Install Python, open a terminal in the folder containing `student_records.py`, and run `python student_records.py`. The program uses Python's standard library, so no third-party package installation is required.
14. Important Implementation Notes
    • The sample-data list and first-run sample insertion block must be removed if the intended behavior is to start with an empty database.
    • Removing sample insertion code does not remove sample records that already exist in an older `students.db` file.
    • The database schema enforces non-negative GPA, while Python validation enforces the configured upper limit.
    • The `update()` method should ideally guard against an empty `changes` dictionary before building its SQL statement.
    • For a public repository, avoid committing a local database containing real or private student information.
15. Possible Future Enhancements
    • Add automated tests for validation and CRUD behavior.
    • Provide CSV import and export.
    • Add sorting and more advanced search filters.
    • Build a graphical or web interface.
    • Introduce authentication and role-based permissions.
    • Make the GPA scale configurable through application settings.
