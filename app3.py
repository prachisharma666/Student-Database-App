from flask import Flask, request, render_template_string
import psycopg2
import os
 
app = Flask(__name__)
 
# Connect to PostgreSQL using Render's DATABASE_URL
def get_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))
 
# Create table if not exists
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id SERIAL PRIMARY KEY,
            name TEXT,
            sap_id TEXT,
            roll_no TEXT,
            marks INTEGER,
            gender TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
 
init_db()
 
 
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Student Database</title>
<style>
body{font-family:Arial;background:#f2f2f2;padding:40px;}
.container{background:white;padding:30px;border-radius:10px;width:500px;margin:auto;}
input,select,button{width:100%;padding:10px;margin-top:10px;}
.result{margin-top:20px;background:#eef;padding:15px;border-radius:5px;}
</style>
</head>
<body>
 
<div class="container">
<h2>Add Student</h2>
 
<form method="POST" action="/add">
<input type="text" name="name" placeholder="Student Name" required>
<input type="text" name="sap_id" placeholder="SAP ID" required>
<input type="text" name="roll_no" placeholder="Roll Number" required>
<input type="number" name="marks" placeholder="Marks" required>
<input type="text" name="gender" placeholder="Gender" required>
<button type="submit">Save Student</button>
</form>
 
<hr>
 
<h2>Search Student</h2>
 
<form method="POST" action="/search">
<select name="search_name" required>
<option value="">Select Student</option>
{% for name in names %}
<option value="{{name}}">{{name}}</option>
{% endfor %}
</select>
 
<button type="submit">Show Details</button>
</form>
 
{% if student %}
<div class="result">
<h3>Student Information</h3>
<p><b>Name:</b> {{student[0]}}</p>
<p><b>SAP ID:</b> {{student[1]}}</p>
<p><b>Roll Number:</b> {{student[2]}}</p>
<p><b>Marks:</b> {{student[3]}}</p>
<p><b>Gender:</b> {{student[4]}}</p>
</div>
{% endif %}
 
</div>
</body>
</html>
"""
 
 
def get_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [x[0] for x in data]
 
 
@app.route("/")
def home():
    names = get_names()
    return render_template_string(HTML_PAGE, names=names)
 
 
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    sap_id = request.form["sap_id"]
    roll_no = request.form["roll_no"]
    marks = request.form["marks"]
    gender = request.form["gender"]
 
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute(
        "INSERT INTO students(name,sap_id,roll_no,marks,gender) VALUES (%s,%s,%s,%s,%s)",
        (name, sap_id, roll_no, marks, gender)
    )
 
    conn.commit()
    cursor.close()
    conn.close()
 
    names = get_names()
    return render_template_string(HTML_PAGE, names=names)
 
 
@app.route("/search", methods=["POST"])
def search():
    name = request.form["search_name"]
 
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute(
        "SELECT name,sap_id,roll_no,marks,gender FROM students WHERE name=%s",
        (name,)
    )
 
    student = cursor.fetchone()
    cursor.close()
    conn.close()
 
    names = get_names()
 
    return render_template_string(HTML_PAGE, student=student, names=names)
 
 
if __name__ == "__main__":
    app.run()
 
 
