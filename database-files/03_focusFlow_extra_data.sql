USE focusflow;
INSERT INTO users (user_id, institution_id, department_id, first_name, last_name, email, password, role, major, year)
VALUES (9001, 1, 8, 'Test', 'Professor', 'test.professor@northeastern.edu', 'hashed_pw', 'professor', NULL, NULL);

INSERT INTO users (user_id, institution_id, department_id, first_name, last_name, email, password, role, major, year)
VALUES
(9002, 1, 8, 'Alice', 'Chen', 'chen.a@northeastern.edu', 'hashed_pw', 'student', 'Computer Science', 2),
(9003, 1, 8, 'Ben', 'Torres', 'torres.b@northeastern.edu', 'hashed_pw', 'student', 'Computer Science', 3),
(9004, 1, 8, 'Cara', 'Nguyen', 'nguyen.c@northeastern.edu', 'hashed_pw', 'student', 'Data Science', 2),
(9005, 1, 8, 'Dan', 'Kim', 'kim.d@northeastern.edu', 'hashed_pw', 'student', 'Computer Science', 1);

INSERT INTO courses (course_id, professor_id, department_id, title, course_code)
VALUES (9001, 9001, 8, 'Introduction to Databases', 'CS 3200');

INSERT INTO enrollments (user_id, course_id) VALUES
(9002, 9001),
(9003, 9001),
(9004, 9001),
(9005, 9001);

INSERT INTO tasks (task_id, user_id, assignment_id, title, category, priority, time_allocated, status) VALUES
(9001, 9002, NULL, 'Study for midterm', 'school', 'high', 120, 'completed'),
(9002, 9003, NULL, 'Study for midterm', 'school', 'high', 120, 'in_progress'),
(9003, 9004, NULL, 'Study for midterm', 'school', 'medium', 90, 'completed'),
(9004, 9005, NULL, 'Study for midterm', 'school', 'low', 60, 'not_started');

INSERT INTO timer_sessions (task_id, user_id, start_time, end_time, duration, session_type) VALUES
(9001, 9002, '2026-04-01 10:00:00', '2026-04-01 11:30:00', 5400, 'custom'),
(9001, 9002, '2026-04-02 14:00:00', '2026-04-02 14:50:00', 3000, 'pomodoro'),
(9002, 9003, '2026-04-01 09:00:00', '2026-04-01 09:25:00', 1500, 'pomodoro'),
(9003, 9004, '2026-04-03 13:00:00', '2026-04-03 15:00:00', 7200, 'custom'),
(9003, 9004, '2026-04-04 10:00:00', '2026-04-04 10:25:00', 1500, 'pomodoro');