import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jai@2003',
            database='student_management'
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as e:
        print(f"Error: '{e}'")
        return None

def validate_input(prompt, min_value, max_value):
    while True:
        try:
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Value must be between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_result(total_marks):
    return 'Selected' if total_marks >= 200 else 'Rejected'

def add_student(conn):
    cursor = conn.cursor()

    student_name = input("Enter student name (max 30 chars): ")
    if len(student_name) > 30:
        print("Student name too long.")
        return

    college_name = input("Enter college name (max 50 chars): ")
    if len(college_name) > 50:
        print("College name too long.")
        return

    round1_marks = validate_input("Enter marks for Round 1 (0-10): ", 0, 10)
    round2_marks = validate_input("Enter marks for Round 2 (0-10): ", 0, 10)
    round3_marks = validate_input("Enter marks for Round 3 (0-10): ", 0, 10)
    technical_round_marks = validate_input("Enter marks for Technical Round (0-20): ", 0, 20)

    total_marks = round1_marks + round2_marks + round3_marks + technical_round_marks
    result = get_result(total_marks)

    cursor.execute('''INSERT INTO Students (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, Result)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                   (student_name, college_name, round1_marks, round2_marks, round3_marks, technical_round_marks, result))

    conn.commit()
    print("Student added successfully.")

def display_students(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def main():
    conn = create_connection()

    if conn is None:
        return

    while True:
        print("1. Add student")
        print("2. Display all students")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_student(conn)
        elif choice == '2':
            display_students(conn)
        elif choice == '3':
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
