CREATE DATABASE IF NOT EXISTS focusflow;
USE focusflow;

DROP TABLE IF EXISTS activity_logs;
DROP TABLE IF EXISTS timer_sessions;
DROP TABLE IF EXISTS productivity_scores;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS institutions;

CREATE TABLE institutions (
    institution_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    type ENUM('university', 'company', 'other') NOT NULL
);

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    institution_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    CONSTRAINT fk_dept_institution FOREIGN KEY (institution_id)
        REFERENCES institutions(institution_id) ON DELETE RESTRICT
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    institution_id INT NOT NULL,
    department_id INT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'professor', 'analyst', 'admin') NOT NULL,
    major VARCHAR(100),
    year INT,
    CONSTRAINT fk_users_institution FOREIGN KEY (institution_id)
        REFERENCES institutions(institution_id) ON DELETE RESTRICT,
    CONSTRAINT fk_users_department FOREIGN KEY (department_id)
        REFERENCES departments(department_id) ON DELETE SET NULL
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    professor_id INT NOT NULL,
    department_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    CONSTRAINT fk_courses_professor FOREIGN KEY (professor_id)
        REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_courses_department FOREIGN KEY (department_id)
        REFERENCES departments(department_id) ON DELETE RESTRICT
);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_enrollments_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_enrollments_course FOREIGN KEY (course_id)
        REFERENCES courses(course_id) ON DELETE CASCADE
);

CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    due_date DATE,
    time_benchmark INT,
    CONSTRAINT fk_assignments_course FOREIGN KEY (course_id)
        REFERENCES courses(course_id) ON DELETE CASCADE
);

CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    assignment_id INT,
    title VARCHAR(200) NOT NULL,
    category ENUM('school', 'work', 'extracurricular', 'personal') NOT NULL,
    priority ENUM('low', 'medium', 'high'),
    time_allocated INT,
    status ENUM('not_started', 'in_progress', 'completed') NOT NULL DEFAULT 'not_started',
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_tasks_assignment FOREIGN KEY (assignment_id)
        REFERENCES assignments(assignment_id) ON DELETE SET NULL
);

CREATE TABLE timer_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration INT,
    session_type ENUM('pomodoro', 'custom') NOT NULL,
    CONSTRAINT fk_tsess_task FOREIGN KEY (task_id)
        REFERENCES tasks(task_id) ON DELETE CASCADE,
    CONSTRAINT fk_tsess_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE productivity_scores (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    week_start_date DATE NOT NULL,
    CONSTRAINT fk_pscore_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    assignment_id INT NOT NULL,
    message TEXT NOT NULL,
    sent_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_notif_assignment FOREIGN KEY (assignment_id)
        REFERENCES assignments(assignment_id) ON DELETE CASCADE
);

CREATE TABLE activity_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    category ENUM('school', 'work', 'extracurricular', 'personal') NOT NULL,
    duration INT NOT NULL,
    logged_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_alog_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_alog_task FOREIGN KEY (task_id)
        REFERENCES tasks(task_id) ON DELETE RESTRICT
);

INSERT INTO institutions (name, type) VALUES
('Northeastern University', 'university'),
('Boston University', 'university'),
('FocusFlow Inc.', 'company');

INSERT INTO departments (institution_id, name) VALUES
(1, 'Khoury College of Computer Sciences'),
(1, 'College of Engineering'),
(2, 'Department of Computer Science');

INSERT INTO users (institution_id, department_id, first_name, last_name, email, password, role, major, year) VALUES
(1, 1, 'Maya', 'Johnson', 'johnson.m@northeastern.edu', 'hashed_pw_1', 'student', 'Computer Science', 2),
(1, 1, 'Alex', 'Rivera', 'rivera.a@northeastern.edu', 'hashed_pw_2', 'student', 'Data Science', 3),
(1, 1, 'Richard', 'Smith', 'smith.r@northeastern.edu', 'hashed_pw_3', 'professor', NULL, NULL),
(3, NULL, 'James', 'Carter', 'carter.j@focusflow.com', 'hashed_pw_4', 'analyst', NULL, NULL),
(3, NULL, 'Jimmy', 'Park', 'park.j@focusflow.com', 'hashed_pw_5', 'admin', NULL, NULL);

INSERT INTO courses (professor_id, department_id, title, course_code) VALUES
(3, 1, 'Database Design', 'CS 3200'),
(3, 1, 'Algorithms and Data', 'CS 3000');

INSERT INTO enrollments (user_id, course_id) VALUES
(1, 1),
(1, 2),
(2, 1);

INSERT INTO assignments (course_id, title, description, due_date, time_benchmark) VALUES
(1, 'HW 04 - SQL Queries', 'Write queries for the provided schema', '2026-03-15', 3),
(1, 'Phase 2 - Data Model', 'Design the ER and relational diagrams', '2026-04-06', 10),
(2, 'Sorting Algorithm Analysis', 'Analyze and implement three sorting algorithms', '2026-03-20', 6);

INSERT INTO tasks (user_id, assignment_id, title, category, priority, time_allocated, status) VALUES
(1, 1, 'Complete SQL practice problems', 'school', 'high', 3, 'completed'),
(1, 2, 'Draw ER diagram', 'school', 'high', 5, 'in_progress'),
(1, NULL, 'Club meeting prep', 'extracurricular', 'low', 1, 'not_started');

INSERT INTO timer_sessions (task_id, user_id, start_time, end_time, duration, session_type) VALUES
(1, 1, '2026-03-10 14:00:00', '2026-03-10 14:25:00', 25, 'pomodoro'),
(1, 1, '2026-03-10 14:30:00', '2026-03-10 14:55:00', 25, 'pomodoro'),
(2, 1, '2026-04-01 10:00:00', '2026-04-01 11:30:00', 90, 'custom');

INSERT INTO productivity_scores (user_id, score, week_start_date) VALUES
(1, 82.50, '2026-03-09'),
(1, 74.00, '2026-03-16'),
(2, 90.25, '2026-03-09');

INSERT INTO notifications (user_id, assignment_id, message, sent_at) VALUES
(1, 2, 'Phase 2 - Data Model has been posted. Due April 6th.', '2026-03-20 09:00:00'),
(2, 2, 'Phase 2 - Data Model has been posted. Due April 6th.', '2026-03-20 09:00:00'),
(1, 3, 'Sorting Algorithm Analysis has been posted. Due March 20th.', '2026-03-01 08:00:00');

INSERT INTO activity_logs (user_id, task_id, category, duration, logged_at, archived) VALUES
(1, 1, 'school', 50, '2026-03-10 15:00:00', FALSE),
(1, 2, 'school', 90, '2026-04-01 11:30:00', FALSE),
(2, 1, 'school', 120, '2026-03-11 16:00:00', FALSE);