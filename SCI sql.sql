create database SCI;
use SCI;

show tables;

desc course;
desc student;


SELECT * FROM Course;
INSERT INTO Course (course_name, course_code, course_duration) VALUES ('Python Programming', '1', '3');
INSERT INTO Course (course_name, course_code, course_duration) VALUES ('Java Programming', '2', '4');
INSERT INTO Course (course_name, course_code, course_duration) VALUES ('C++ Programming', '3', '4');


select * from student;

ALTER TABLE student DROP COLUMN role;
ALTER TABLE student DROP COLUMN password;


