from flask import Flask, request, jsonify, session, render_template
import mysql.connector
from functools import wraps  

app = Flask(__name__)
app.secret_key = "123"  # Secret key for session management

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="SCI"
    )

# Serve HTML file
@app.route('/')
def index():
    return render_template("index.html")

# Admin Authentication
@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    password = data.get("password")

    if password == "123":  # Hardcoded admin password
        session["admin"] = True
        return jsonify({"message": "Admin logged in successfully"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Admin Logout
@app.route('/admin_logout', methods=['POST'])
def admin_logout():
    session.pop("admin", None)
    return jsonify({"message": "Logged out successfully"}), 200

# Middleware for Admin Authorization
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return wrapper

# Add Student (Admin Only)
@app.route('/add_student', methods=['POST'])
@admin_required
def add_student():
    data = request.json
    student_name = data.get("student_name")
    email = data.get("email")
    course_id = data.get("course_id")

    if not student_name or not email or not course_id:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Course WHERE course_id = %s", (course_id,))
    course = cursor.fetchone()
    if not course:
        return jsonify({"error": "Invalid course_id"}), 400

    try:
        cursor.execute("INSERT INTO Student (student_name, email, course_id) VALUES (%s, %s, %s)",
                       (student_name, email, course_id))
        conn.commit()
        return jsonify({"message": "Student added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Retrieve Student Details (Accessible to All)
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT Student.student_id, Student.student_name, Student.email, 
           Course.course_name, Course.course_code, Course.course_duration
    FROM Student
    LEFT JOIN Course ON Student.course_id = Course.course_id
    """
    cursor.execute(query)
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students), 200

# Update Student Details, including changing course (Admin Only)
@app.route('/update_student/<int:student_id>', methods=['PUT'])
@admin_required
def update_student(student_id):
    data = request.json
    student_name = data.get("student_name")
    email = data.get("email")
    course_id = data.get("course_id")

    if not student_name or not email or not course_id:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the student exists
    cursor.execute("SELECT * FROM Student WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Check if the new course exists
    cursor.execute("SELECT * FROM Course WHERE course_id = %s", (course_id,))
    course = cursor.fetchone()
    if not course:
        return jsonify({"error": "Invalid course_id"}), 400

    # Update student details and course
    try:
        cursor.execute("""
            UPDATE Student 
            SET student_name = %s, email = %s, course_id = %s 
            WHERE student_id = %s
        """, (student_name, email, course_id, student_id))
        conn.commit()
        return jsonify({"message": "Student details updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Delete Student (Admin Only)
@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
@admin_required
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT course_id FROM Student WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    if student[0]:  
        return jsonify({"error": "Cannot delete student enrolled in a course"}), 403

    cursor.execute("DELETE FROM Student WHERE student_id = %s", (student_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Student deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
