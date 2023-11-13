import sqlite3

def create_database():
    try:
        conn = sqlite3.connect('main_database.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                student_id INTEGER UNIQUE,
                name TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY,
                status INTEGER,
                path TEXT,
                student_id INTEGER,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS professors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                classes_id INTEGER,
                FOREIGN KEY(classes_id) REFERENCES classes(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                students_id INTEGER,
                tests_id INTEGER,
                FOREIGN KEY(students_id) REFERENCES students(id),
                FOREIGN KEY(tests_id) REFERENCES tests(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY,
                name TEXT,
                questions_id INTEGER,
                FOREIGN KEY(questions_id) REFERENCES questions(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                name TEXT,
                answer TEXT,
                pages_id INTEGER,
                FOREIGN KEY(pages_id) REFERENCES pages(id)
            )
        ''')

        conn.commit()
        print("Database and tables created successfully!")

    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

    finally:
        conn.close()

#function to print the contents of a table
def print_table(table_name):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM {table_name}')
        table_data = cursor.fetchall()

        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = [col[1] for col in cursor.fetchall()]

        print(" | ".join(columns))
        print("-" * (len(columns) * 10))

        for row in table_data:
            print(" | ".join(str(col) for col in row))

    except sqlite3.Error as e:
        print(f"Error printing table: {e}")
    finally:
        conn.close()

#function to get pages for a student based on student_id
def get_pages_via_student_id(student_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT pages.id, pages.status, pages.path
            FROM students
            JOIN pages ON students.student_id = pages.student_id
            WHERE students.student_id = ?
        ''', (student_id,))

        pages_data = cursor.fetchall()
        print(f"Pages for student {student_id}:")
        for row in pages_data:
            print(f"Page ID: {row[0]}, Status: {row[1]}, Path: {row[2]}")

    except sqlite3.Error as e:
        print(f"Error retrieving pages for student: {e}")
    finally:
        conn.close()

#function to get classes for a professor based on professor_id
def get_classes(professor_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT classes.id, classes.name
            FROM professors
            JOIN classes ON professors.classes_id = classes.id
            WHERE professors.id = ?
        ''', (professor_id,))

        classes_data = cursor.fetchall()
        print(f"Classes for professor {professor_id}:")
        for row in classes_data:
            print(f"Class ID: {row[0]}, Name: {row[1]}")

    except sqlite3.Error as e:
        print(f"Error retrieving classes for professor: {e}")
    finally:
        conn.close()

#function to get students for a class based on class_id
def get_students_via_classes(class_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT students.id, students.name
            FROM classes
            JOIN students ON classes.students_id = students.id
            WHERE classes.id = ?
        ''', (class_id,))

        students_data = cursor.fetchall()
        print(f"Students for class {class_id}:")
        for row in students_data:
            print(f"Student ID: {row[0]}, Name: {row[1]}")

    except sqlite3.Error as e:
        print(f"Error retrieving students for class: {e}")
    finally:
        conn.close()

def get_answer_via_question_id(question_id):
    try:
        conn = sqlite3.connect('main_database.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT answer
            FROM questions
            WHERE id = ?
        ''', (question_id,))

        answer_data = cursor.fetchone()

        if answer_data:
            answer = answer_data[0]
            print(f"Answer for question {question_id}: {answer}")
        else:
            print(f"Error: Invalid question id - {question_id}")

    except sqlite3.Error as e:
        print(f"Error fetching answer: {e}")

    finally:
        conn.close()

#function to add pages to the database with duplicate check
def add_page_to_database(student_id, status, path):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM pages WHERE student_id = ?", (student_id,))
        existing_page = cursor.fetchone()

        if existing_page:
            print("Pages for the provided student_id already exist. Not adding.")
        else:
            cursor.execute("INSERT INTO pages (student_id, status, path) VALUES (?, ?, ?)", (student_id, status, path))

            conn.commit()
            print("Pages added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding pages: {e}")
    finally:
        conn.close()

#function to add a student to the database with duplicate check
def add_student_to_database(student_id, student_name):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM students WHERE student_id = ?", (student_id,))
        existing_student = cursor.fetchone()

        if existing_student:
            print("Student with the provided student_id already exists. Not adding.")
        else:
            cursor.execute("INSERT INTO students (student_id, name) VALUES (?, ?)", (student_id, student_name))

            conn.commit()
            print("Student added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding student: {e}")
    finally:
        conn.close()

#function to add a professor to the database with duplicate check
def add_professor_to_database(professor_name, classes_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM professors WHERE name = ?", (professor_name,))
        existing_professor = cursor.fetchone()

        if existing_professor:
            print("Professor with the provided name already exists. Not adding.")
        else:
            cursor.execute("INSERT INTO professors (name, classes_id) VALUES (?, ?)", (professor_name, classes_id))

            conn.commit()
            print("Professor added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding professor: {e}")
    finally:
        conn.close()

#function to add a class to the database with duplicate check
def add_class_to_database(class_name, students_id, tests_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM classes WHERE name = ?", (class_name,))
        existing_class = cursor.fetchone()

        if existing_class:
            print("Class with the provided name already exists. Not adding.")
        else:
            cursor.execute("INSERT INTO classes (name, students_id, tests_id) VALUES (?, ?, ?)", (class_name, students_id, tests_id))

            conn.commit()
            print("Class added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding class: {e}")
    finally:
        conn.close()

#function to add a test to the database with duplicate check
def add_test_to_database(test_name, questions_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM tests WHERE name = ?", (test_name,))
        existing_test = cursor.fetchone()

        if existing_test:
            print("Test with the provided name already exists. Not adding.")
        else:
            cursor.execute("INSERT INTO tests (name, questions_id) VALUES (?, ?)", (test_name, questions_id))

            conn.commit()
            print("Test added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding test: {e}")
    finally:
        conn.close()

#function to add a question to the database with duplicate check
def add_question_to_database(question_name, answer, pages_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM questions WHERE name = ?", (question_name,))
        existing_question = cursor.fetchone()

        if existing_question:
            print("Question with the provided name already exists. Not adding.")
        else:
            cursor.execute("INSERT INTO questions (name, answer, pages_id) VALUES (?, ?, ?)", (question_name, answer, pages_id))

            conn.commit()
            print("Question added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding question: {e}")
    finally:
        conn.close()

#function to clear table
def clear_table(table_name):
    try:
        conn = sqlite3.connect('main_database.db')
        cursor = conn.cursor()

        cursor.execute(f'DELETE FROM {table_name}')

        conn.commit()
        print(f"All records cleared from the {table_name} table.")

    except sqlite3.Error as e:
        print(f"Error clearing table: {e}")

    finally:
        conn.close()

def processes_pages_via_question_id(question_id):
    conn = sqlite3.connect('main_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT pages.id, pages.path
            FROM questions
            JOIN pages ON questions.pages_id = pages.id
            WHERE questions.id = ?
        ''', (question_id,))

        pages_data = cursor.fetchall()

        for row in pages_data:
            page_id, page_path = row
            #not yet implemented yet
            #read_answer_box(page_path, question_id)

    except sqlite3.Error as e:
        print(f"Error fetching pages data: {e}")

    finally:
        conn.close()


# UNCOMMENT THE BELOW LINE TO RUN THE SQL COMMANDS THE INTIALIZES THE TABLES
#create_database()

tables = ["professors", "classes", "tests", "questions", "pages", "students"]
for table in tables:
    clear_table(table)

# Sample data insertion
add_professor_to_database("Professor Smith", 1)
add_class_to_database("Math 101", 1, 1)
add_student_to_database(123456789, "John Doe")
add_page_to_database(123456789, 1, "/path/to/page1")
add_test_to_database("Final Exam", 1)
add_question_to_database("Question 1", "Answer 1", 1)

get_pages_via_student_id(123456789)

get_classes(1)

get_students_via_classes(1)

get_answer_via_question_id(1)


for table in tables:
    print_table(table)