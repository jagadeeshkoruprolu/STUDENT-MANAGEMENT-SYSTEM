from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hall_ticket TEXT UNIQUE,
            name TEXT,
            age INTEGER,
            gender TEXT,
            mobile TEXT,
            location TEXT,
            email TEXT,
            dob TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home - list all students
@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = (
            request.form['hall_ticket'],
            request.form['name'],
            request.form['age'],
            request.form['gender'],
            request.form['mobile'],
            request.form['location'],
            request.form['email'],
            request.form['dob']
        )
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (hall_ticket, name, age, gender, mobile, location, email, dob) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    if request.method == 'POST':
        data = (
            request.form['hall_ticket'],
            request.form['name'],
            request.form['age'],
            request.form['gender'],
            request.form['mobile'],
            request.form['location'],
            request.form['email'],
            request.form['dob'],
            id
        )
        c.execute('''
            UPDATE students SET hall_ticket=?, name=?, age=?, gender=?, mobile=?, location=?, email=?, dob=? WHERE id=?
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM students WHERE id=?", (id,))
        student = c.fetchone()
        conn.close()
        return render_template('edit_student.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
