from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app=Flask(__name__)
Database= 'database.db'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory= sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO students (name, email, phone, course) VALUES (?, ?, ?, ?)',
                         (name, email, phone, course))
            conn.commit()
            conn.close()
            return redirect(url_for('index', success='1'))
        except sqlite3.IntegrityError:
            conn.close()
            return redirect(url_for('index', error='1'))
    return render_template('register.html')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']

        conn.execute('UPDATE students SET name = ?, email = ?, phone = ?, course = ? WHERE id = ?',
                     (name, email, phone, course, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index', updated='1'))

    conn.close()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index', deleted='1'))

if __name__ == '__main__':
    app.run(debug=True)