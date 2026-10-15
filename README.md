# 🎓 Student Record Management System

A single-file, menu-driven command-line application for managing student records. It stores data in a local **SQLite** database, validates every input, and handles errors (including a corrupted database) gracefully.

---

## ✨ Features

- **Add, view, search, update, and delete** student records (full CRUD)
- **Persistent storage** – data is saved in `students.db`, created automatically next to the script
- **Strict input validation** for roll number, name, email, GPA, and course, with friendly error messages and re-prompting
- **Partial, case-insensitive search** by roll number or name
- **Safe updates** – press Enter to keep the current value of any field
- **Delete confirmation** – asks `[y/N]` before removing a record
- **Duplicate protection** – roll numbers are unique (primary key)
- **Database safety**
  - Integrity check on startup
  - Automatic commit on success and rollback on failure
  - Corrupted databases are **moved aside, never deleted**, and a fresh one is created on request
- **Clean table output** with aligned columns and a record count
- **Graceful exit handling** – `Ctrl+C` cancels the current action; `Ctrl+D`/`Ctrl+Z` exits cleanly
- **Zero dependencies** – uses only the Python standard library

---

## 🛠️ Tech Stack

| Component | Details |
|-----------|---------|
| **Language** | Python 3.8+ |
| **Database** | SQLite (via the built-in `sqlite3` module) |
| **Libraries** | Standard library only: `sqlite3`, `re`, `math`, `time`, `pathlib`, `dataclasses`, `contextlib` |
| **Interface** | Command-line, menu-driven |
| **Platform** | Windows, macOS, Linux |
| **Dependencies** | None — no `pip install` required |

---

## ⚙️ Setup

### 1. Prerequisites

Check that Python 3.8 or newer is installed:

```bash
python --version
```

If it is not, download it from [python.org](https://www.python.org/downloads/).

### 2. Get the project

```bash
git clone <your-repository-url>
cd <project-folder>
```

Or download `student_records.py` into any folder.

### 3. Run

```bash
python student_records.py
```

The database file `students.db` is created automatically on first run.

---

## 🚀 Usage

When the program starts, you will see this menu:

```text
==== Student Record Management ====
 1. Add student
 2. View all students
 3. Search (roll no. or name)
 4. Update student
 5. Delete student
 0. Exit
```

Type the option number and press Enter.

### Example session

```text
Choose an option: 1

-- Add student (Ctrl+C to cancel) --
Roll no : 24bib001
Name    : Sihana Fathima
Email   : sihana@example.com
GPA     : 8.5
Course  : B.Sc Computer Science
  OK Student added.
Roll No     Name                    Email                         GPA   Course
--------------------------------------------------------------------------------
24BIB001    Sihana Fathima          sihana@example.com            8.50  B.Sc Computer Science

  1 record(s)
```

---

## ✅ Validation Rules

| Field | Rule | Notes |
|-------|------|-------|
| **Roll No** | 3–15 characters: letters, digits, hyphens; cannot start with a hyphen | Automatically converted to UPPERCASE (e.g. `24BIB001`) |
| **Name** | 2–60 characters; letters, spaces, `.`, `'`, `-` | Extra spaces are collapsed; needs at least 2 letters |
| **Email** | Valid email format, up to 254 characters | Automatically converted to lowercase |
| **GPA** | Number from 0 to 10 | Rounded to 2 decimal places; `nan` and `inf` are rejected |
| **Course** | 2–50 characters | Extra spaces are collapsed |

---

## 🗄️ Database Schema

```sql
CREATE TABLE IF NOT EXISTS students (
    roll_no TEXT PRIMARY KEY,
    name    TEXT NOT NULL,
    email   TEXT NOT NULL,
    gpa     REAL NOT NULL CHECK (gpa >= 0),
    course  TEXT NOT NULL
)
```

---

## 🧱 Project Structure

```text
.
├── student_records.py   # The entire application
├── students.db          # SQLite database (auto-created)
└── README.md            # Documentation
```

### Code organization (inside `student_records.py`)

| Section | Purpose |
|---------|---------|
| `Student` dataclass | Holds one student's data |
| Validation functions | `validate_roll_no`, `validate_name`, `validate_email`, `validate_gpa`, `validate_course` |
| Custom exceptions | `ValidationError`, `StorageError`, `DuplicateStudentError`, `StudentNotFoundError`, `CorruptDatabaseError` |
| `StudentRepository` | All database operations (add, get, list, search, update, delete) |
| Menu functions | User-facing actions and table printing |
| `main()` | Program loop and error handling |

---

## 🔒 Safety & Error Handling

- **Parameterized SQL queries** prevent SQL injection.
- **Transactions**: changes are committed only if the operation succeeds, otherwise rolled back.
- **Corruption recovery**: if the database fails its integrity check, the program offers to rename the bad file to `students.db.corrupt-<timestamp>` and start fresh. Nothing is deleted.
- **Locked database**: waits up to 5 seconds before reporting an error.

---

## 🔮 Future Improvements

- Export records to CSV or Excel
- Sort and filter by GPA or course
- Unit tests with `pytest`
- Optional GUI or web interface

---

## 🤝 Contributing

Suggestions and improvements are welcome. Fork the repository, create a feature branch, and open a pull request.

## 📜 License

This project is released under the MIT License.

---

**Author:** SIHANA FATHIMA AK

