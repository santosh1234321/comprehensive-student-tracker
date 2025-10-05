import sqlite3
from flask import Flask, render_template, request, redirect, url_for
# --- Database Setup and Student Class (Keep from your original code) ---
# Database Connection (The database connection needs to be managed within the request context in a web app,
# but for a simple example, we'll keep the basic connection for now, focusing on the web structure)
# In a production app, you'd use a pattern like `g` or a framework extension for better resource management.
DB_NAME = "student_performance.db"
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn
# Create Student Table (Executed once when the app starts or a utility runs)
def setup_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            math INTEGER,
            science INTEGER,
            english INTEGER,
            total INTEGER,
            average REAL,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()
class Student:
    """A simplified class to handle grade/total/average calculation."""
    def __init__(self, name, math, science, english):
        self.name = name
        self.math = math
        self.science = science
        self.english = english
        self.total = math + science + english
        self.average = self.total / 3
        self.grade = self.calculate_grade()
    def calculate_grade(self):
        if self.average >= 90: return 'A'
        elif self.average >= 80: return 'B'
        elif self.average >= 70: return 'C'
        elif self.average >= 60: return 'D'
        else: return 'F'
# --- Flask App Initialization and Routes ---
app = Flask(__name__)
setup_db() # Ensure the table is created before running the app
# 1. Home / View Students Route
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('index.html', students=students)
# 2. Add Student Route (GET for form, POST for submission)
@app.route('/add', methods=('GET', 'POST'))
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        math = int(request.form['math'])
        science = int(request.form['science'])
        english = int(request.form['english'])
        student = Student(name, math, science, english)
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO students (name, math, science, english, total, average, grade) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student.name, student.math, student.science, student.english, student.total, student.average, student.grade)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')
# 3. Edit Student Route
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

    if student is None:
        conn.close()
        return "Student not found", 404

    if request.method == 'POST':
        name = request.form['name'] # Keep name just for display/consistency, though it's not updated
        math = int(request.form['math'])
        science = int(request.form['science'])
        english = int(request.form['english'])

        # Recalculate total, average, and grade
        temp_student = Student(name, math, science, english)

        conn.execute(
            "UPDATE students SET math=?, science=?, english=?, total=?, average=?, grade=? WHERE id=?",
            (math, science, english, temp_student.total, temp_student.average, temp_student.grade, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', student=student)

# 4. Delete Student Route
@app.route('/delete/<int:id>', methods=('POST',))
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Remove the conn.close() from the original script's end, as Flask manages this now.
    app.run(debug=True)
