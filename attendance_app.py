
import sqlite3
from datetime import date

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    attendance_date TEXT,
    status TEXT
)
""")

conn.commit()

# Main Menu
while True:
    print("\n===== STUDENT ATTENDANCE MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Mark Attendance")
    print("4. View Attendance History")
    print("5. Calculate Attendance Percentage")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n--- Add Student ---")

        name = input("Enter student name: ")
        roll_no = input("Enter roll number: ")
        department = input("Enter department: ")

        try:
            cursor.execute(
                "INSERT INTO students VALUES (?, ?, ?)",
                (roll_no, name, department)
            )
            conn.commit()
            print("Student added successfully!")

        except sqlite3.IntegrityError:
            print("Roll number already exists!")

    
    elif choice == "2":
        print("\n--- Student Details ---")

        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        if records:
            for student in records:
                print("Name:", student[1])
                print("Roll Number:", student[0])
                print("Department:", student[2])
                print("--------------------")
        else:
            print("No students found!")



    elif choice == "3":
        print("\n--- Mark Attendance ---")

        roll = input("Enter student roll number: ")

        cursor.execute(
            "SELECT * FROM students WHERE roll_no = ?",
            (roll,)
        )
        student = cursor.fetchone()

        if student:
            status = input("Enter attendance (Present/Absent): ").capitalize()

            if status in ["Present", "Absent"]:
                cursor.execute("""
                    INSERT INTO attendance
                    (roll_no, attendance_date, status)
                    VALUES (?, ?, ?)
                """, (roll, str(date.today()), status))

                conn.commit()
                print("Attendance marked successfully!")
            else:
                print("Invalid attendance status!")
        else:
            print("Student not found!")

    elif choice == "4":
        print("\n--- Attendance History ---")

        roll = input("Enter student roll number: ")

        cursor.execute("""
            SELECT attendance_date, status
            FROM attendance
            WHERE roll_no = ?
        """, (roll,))

        records = cursor.fetchall()

        if records:
            for record in records:
                print("Date:", record[0])
                print("Status:", record[1])
                print("--------------------")
        else:
            print("No attendance records found!")

    elif choice == "5":
        print("\n--- Attendance Percentage ---")

        roll = input("Enter student roll number: ")

        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END)
            FROM attendance
            WHERE roll_no = ?
        """, (roll,))

        total, present = cursor.fetchone()

        if total > 0:
            percentage = (present / total) * 100
            print("Total Classes:", total)
            print("Present Classes:", present)
            print("Attendance Percentage:", round(percentage, 2), "%")
        else:
            print("No attendance records found!")

    elif choice == "6":
        print("Thank you for using our system!")
        break

    else:
        print("Invalid choice! Try again.")

conn.close()