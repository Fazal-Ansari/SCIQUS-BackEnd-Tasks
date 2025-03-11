import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="SCI"
)
cursor = conn.cursor()

# Create Course Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    course_duration INT NOT NULL CHECK (course_duration > 0)
)
""")

# Create Student Table with Foreign Key
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE SET NULL
)
""")

print("Tables created successfully.")


# Close connection
cursor.close()
conn.close()
