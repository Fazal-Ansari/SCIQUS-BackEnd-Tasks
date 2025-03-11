# SCIQUS-BackEnd-Tasks
# Student-Course Management System

## Setup and Run Instructions

### Prerequisites
- Python 3.x
- MySQL Server
- Required Python Packages: `Flask`, `mysql-connector-python`

### Installation
1. Clone the repository or download the source files.
2. Install dependencies:
   ```sh
   pip install flask mysql-connector-python
   ```
3. Setup MySQL database:
   - Open MySQL and run:
     ```sql
     CREATE DATABASE SCI;
     USE SCI;
     ```
   - Execute the provided SQL scripts to create tables.
4. Run the application:
   ```sh
   python app.py
   ```
5. The server will start on `http://127.0.0.1:5000/`.

## Database Schema

### Tables
#### `Course` Table
```sql
CREATE TABLE IF NOT EXISTS Course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    course_duration INT NOT NULL CHECK (course_duration > 0)
);
```
#### `Student` Table
```sql
CREATE TABLE IF NOT EXISTS Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE SET NULL
);
```

### Sample Data
```sql
INSERT INTO Course (course_name, course_code, course_duration) VALUES ('Python Programming', '1', '3');
INSERT INTO Course (course_name, course_code, course_duration) VALUES ('Java Programming', '2', '4');
INSERT INTO Course (course_name, course_code, course_duration) VALUES ('C++ Programming', '3', '4');
```

## API Endpoints

### Admin Authentication
- **Login:** `POST /admin_login` (Payload: `{ "password": "123" }`)
- **Logout:** `POST /admin_logout`

### Student Management (Admin Only)
- **Add Student:** `POST /add_student`
- **Update Student:** `PUT /update_student/<student_id>`
- **Delete Student:** `DELETE /delete_student/<student_id>`

### Public Access
- **Get Students:** `GET /students`

## Notes
- Admin access is required for modifying student records.
- Students must be linked to an existing course.
- Deleting a student enrolled in a course is restricted.

