CREATE DATABASE IF NOT EXISTS focusflow;
USE focusflow;

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
