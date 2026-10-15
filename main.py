"""Student Record Management System - single file version.
Run:  python student_records.py
Data is saved in students.db (created automatically next to this file).
"""
import math
import re
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

DB_FILE = Path(__file__).parent / "students.db"
MAX_GPA = 10.0


@dataclass
class Student:
    roll_no: str
    name: str
    email: str
    gpa: float
    course: str


class ValidationError(ValueError):
    pass


EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
ROLL_RE = re.compile(r"^[A-Z0-9][A-Z0-9-]{2,14}$")


def validate_roll_no(raw):
    value = raw.strip().upper()
    if not ROLL_RE.match(value):
        raise ValidationError("Roll number must be 3-15 characters: letters, digits or hyphens (e.g. 24BIB001).")
    return value


def validate_name(raw):
    value = " ".join(raw.split())
    if not 2 <= len(value) <= 60:
        raise ValidationError("Name must be 2-60 characters long.")
    if not all(c.isalpha() or c in " .'-" for c in value) or sum(c.isalpha() for c in value) < 2:
        raise ValidationError("Name may contain only letters, spaces, . ' and -.")
    return value


def validate_email(raw):
    value = raw.strip().lower()
    if len(value) > 254 or not EMAIL_RE.match(value):
        raise ValidationError("Enter a valid email address (e.g. name@example.com).")
    return value


def validate_gpa(raw):
    try:
        value = float(raw.strip())
    except ValueError:
        raise ValidationError("GPA must be a number (e.g. 8.5).") from None
    if not math.isfinite(value) or not 0.0 <= value <= MAX_GPA:
        raise ValidationError(f"GPA must be between 0 and {MAX_GPA:g}.")
    return round(value, 2)


def validate_course(raw):
    value = " ".join(raw.split())
    if not 2 <= len(value) <= 50:
        raise ValidationError("Course must be 2-50 characters long.")
    return value


class StorageError(Exception):
    pass


class DuplicateStudentError(StorageError):
    pass


class StudentNotFoundError(StorageError):
    pass


class CorruptDatabaseError(StorageError):
    pass


SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    roll_no TEXT PRIMARY KEY,
    name    TEXT NOT NULL,
    email   TEXT NOT NULL,
    gpa     REAL NOT NULL CHECK (gpa >= 0),
    course  TEXT NOT NULL
)
"""


class StudentRepository:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self._init_db()

    @contextmanager
    def _session(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except StorageError:
            if conn:
                conn.rollback()
            raise
        except sqlite3.OperationalError as exc:
            raise StorageError(f"Database error: {exc}") from exc
        except sqlite3.DatabaseError as exc:
            raise CorruptDatabaseError(f"Database file is corrupted: {exc}") from exc
        finally:
            if conn:
                conn.close()

    def _init_db(self):
        with self._session() as conn:
            result = conn.execute("PRAGMA quick_check").fetchone()
            if result is None or result[0] != "ok":
                raise CorruptDatabaseError("Database integrity check failed.")
            conn.execute(SCHEMA)
            conn.execute("SELECT roll_no, name, email, gpa, course FROM students LIMIT 1")

    def reset_corrupt_database(self):
        """Move the bad file aside (never deletes it) and start a fresh database."""
        backup = self.db_path.with_name(f"{self.db_path.name}.corrupt-{int(time.time())}")
        self.db_path.replace(backup)
        self._init_db()
        return backup

    @staticmethod
    def _row(row):
        return Student(row["roll_no"], row["name"], row["email"], row["gpa"], row["course"])

    def add(self, s):
        with self._session() as conn:
            try:
                conn.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                             (s.roll_no, s.name, s.email, s.gpa, s.course))
            except sqlite3.IntegrityError:
                raise DuplicateStudentError(f"Roll number {s.roll_no} already exists.") from None

    def get(self, roll_no):
        with self._session() as conn:
            row = conn.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,)).fetchone()
        if row is None:
            raise StudentNotFoundError(f"No student with roll number {roll_no}.")
        return self._row(row)

    def list_all(self):
        with self._session() as conn:
            rows = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
        return [self._row(r) for r in rows]

    def search(self, query):
        """Case-insensitive partial match on roll number or name."""
        q = query.strip().casefold()
        if not q:
            return []
        return [s for s in self.list_all() if q in s.roll_no.casefold() or q in s.name.casefold()]

    def update(self, roll_no, **changes):
        self.get(roll_no)
        sets = ", ".join(f"{k} = ?" for k in changes)
        with self._session() as conn:
            conn.execute(f"UPDATE students SET {sets} WHERE roll_no = ?", (*changes.values(), roll_no))

    def delete(self, roll_no):
        with self._session() as conn:
            cur = conn.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
            if cur.rowcount == 0:
                raise StudentNotFoundError(f"No student with roll number {roll_no}.")


MENU = """
==== Student Record Management ====
 1. Add student
 2. View all students
 3. Search (roll no. or name)
 4. Update student
 5. Delete student
 0. Exit
"""


def ask(prompt, validator, keep=None):
    """Keep asking until input is valid. If keep is given, empty Enter keeps old value."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and keep is not None:
            return keep
        try:
            return validator(raw)
        except ValidationError as exc:
            print(f"  x {exc}")


def print_table(students):
    if not students:
        print("  (no records)")
        return
    header = f"{'Roll No':<12}{'Name':<24}{'Email':<30}{'GPA':<6}Course"
    print(header)
    print("-" * (len(header) + 12))
    for s in students:
        print(f"{s.roll_no:<12}{s.name[:22]:<24}{s.email[:28]:<30}{s.gpa:<6.2f}{s.course}")
    print(f"\n  {len(students)} record(s)")


def add_student(repo):
    print("\n-- Add student (Ctrl+C to cancel) --")
    roll = ask("Roll no : ", validate_roll_no)
    try:
        repo.get(roll)
        print(f"  x Roll number {roll} already exists.")
        return
    except StudentNotFoundError:
        pass
    name = ask("Name    : ", validate_name)
    email = ask("Email   : ", validate_email)
    gpa = ask("GPA     : ", validate_gpa)
    course = ask("Course  : ", validate_course)
    student = Student(roll, name, email, gpa, course)
    repo.add(student)
    print("  OK Student added.")
    print_table([student])


def view_all(repo):
    print()
    print_table(repo.list_all())


def search_students(repo):
    q = input("\nSearch (partial roll no. or name): ").strip()
    if not q:
        print("  x Enter something to search for.")
        return
    print()
    print_table(repo.search(q))


def update_student(repo):
    roll = ask("\nRoll no to update: ", validate_roll_no)
    cur = repo.get(roll)
    print("  Press Enter to keep the current value.")
    changes = {
        "name": ask(f"Name   [{cur.name}]: ", validate_name, keep=cur.name),
        "email": ask(f"Email  [{cur.email}]: ", validate_email, keep=cur.email),
        "gpa": ask(f"GPA    [{cur.gpa}]: ", validate_gpa, keep=cur.gpa),
        "course": ask(f"Course [{cur.course}]: ", validate_course, keep=cur.course),
    }
    repo.update(roll, **changes)
    print("  OK Student updated.")


def delete_student(repo):
    roll = ask("\nRoll no to delete: ", validate_roll_no)
    s = repo.get(roll)
    if input(f"  Delete {s.name} ({s.roll_no})? [y/N]: ").strip().lower() == "y":
        repo.delete(roll)
        print("  OK Deleted.")
    else:
        print("  Cancelled.")


ACTIONS = {"1": add_student, "2": view_all, "3": search_students,
           "4": update_student, "5": delete_student}


def open_repository():
    try:
        return StudentRepository(DB_FILE)
    except CorruptDatabaseError as exc:
        print(f"! {exc}")
        if input("Move the damaged file aside and start fresh? [y/N]: ").strip().lower() != "y":
            return None
        repo = StudentRepository.__new__(StudentRepository)
        repo.db_path = DB_FILE
        print(f"  Old file kept as {repo.reset_corrupt_database().name}")
        return repo
    except StorageError as exc:
        print(f"! Could not open database: {exc}")
        return None


def main():
    repo = open_repository()
    if repo is None:
        return
    while True:
        try:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                return
            action = ACTIONS.get(choice)
            if action is None:
                print("  x Invalid option. Enter a number from 0 to 5.")
                continue
            action(repo)
        except StorageError as exc:
            print(f"  x {exc}")
        except KeyboardInterrupt:
            print("\n  Cancelled.")
        except EOFError:
            print("\nGoodbye!")
            return


if __name__ == "__main__":
    main()
