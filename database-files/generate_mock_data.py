import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker
 
fake = Faker()
Faker.seed(42)
random.seed(42)
 
OUTPUT_DIR = "database-files/mock_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Constants for data generation
NUM_INSTITUTIONS = 30
DEPARTMENTS_PER_INSTITUTION = 8 
NUM_STUDENTS = 100
NUM_PROFESSORS = 60
NUM_ANALYSTS = 10
NUM_ADMINS = 5
COURSES_PER_DEPARTMENT = 3       
ENROLLMENTS_PER_STUDENT = 3     
ASSIGNMENTS_PER_COURSE = 4
TASKS_PER_USER = 8              
TIMER_SESSIONS_PER_TASK = 3      
WEEKS_OF_SCORES = 8              
NOTIFICATIONS_PER_USER = 5
ACTIVITY_LOGS_PER_USER = 10

# Referrential data 
ALL_DEPARTMENT_NAMES = [
    "Engineering", "Health Sciences", "Computer Science", "Business",
    "Art and Media", "Literature", "Social Science", "Science",
    "Law", "Humanities", "Mathematics", "Education",
    "Psychology", "Philosophy", "Economics"
]
UNIVERSITY_NAMES = [
    "Northeastern University", "Boston University", "MIT",
    "Harvard University", "Tufts University", "Stanford University",
    "Yale University", "Columbia University", "Duke University",
    "Georgetown University", "Princeton University", "Brown University",
    "Cornell University", "University of Pennsylvania", "NYU",
    "UCLA", "UC Berkeley", "University of Michigan",
    "University of Chicago", "Northwestern University",
    "Carnegie Mellon University", "Johns Hopkins University",
    "Vanderbilt University", "Rice University", "Emory University",
    "University of Virginia", "University of Notre Dame",
    "Washington University in St. Louis", "Georgia Tech",
    "University of Southern California"
]

# Ensuring each department has a unique course prefix and a set of course names
COURSE_PREFIXES = {
    "Engineering": ("ENG", ["Statics", "Dynamics", "Thermodynamics"]),
    "Health Sciences": ("HSC", ["Anatomy", "Physiology", "Biostatistics"]),
    "Computer Science": ("CS", ["Algorithms","Databases", "Machine Learning"]),
    "Business": ("BUS", ["Accounting", "Marketing", "Finance"]),
    "Art and Media": ("ART", ["Drawing", "Digital Media", "Photography"]),
    "Literature": ("LIT", ["American Literature", "British Literature", "Creative Writing"]),
    "Social Science": ("SOC", ["Sociology", "Anthropology", "Political Science"]),
    "Science": ("SCI", ["Biology", "Chemistry", "Physics"]),
    "Law": ("LAW", ["Constitutional Law", "Criminal Law", "Contract Law"]),
    "Humanities": ("HUM", ["Ethics", "History", "Cultural Studies"]),
    "Mathematics": ("MTH", ["Calculus", "Linear Algebra", "Probability"]),
    "Education": ("EDU", ["Curriculum Design", "Child Development", "Educational Psychology"]),
    "Psychology": ("PSY", ["Cognitive Psychology", "Developmental Psychology", "Abnormal Psychology"]),
    "Philosophy": ("PHL", ["Logic", "Metaphysics", "Epistemology"]),
    "Economics": ("ECN", ["Microeconomics", "Macroeconomics", "Econometrics"]),
}

# A list of common majors to assign to students
MAJORS = [
    "Computer Science", "Engineering", "Business", "Biology", "Psychology",
    "English", "Mathematics", "Economics", "Political Science", "Art",
    "Health Sciences", "Sociology", "Philosophy", "Chemistry", "Physics"
]

# A list of assignment types to randomly generate assignment names
ASSIGNMENT_TYPES = [
    "Homework {n}", "Problem Set {n}", "Lab Report {n}", "Essay {n}",
    "Quiz {n}", "Midterm Exam", "Final Exam", "Group Project",
    "Research Paper", "Presentation", "Case Study {n}", "Reading Response {n}"
]

### Helper Functions ###

# Write CSV files with mock data 
def write_csv(filename, headers, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"{filename}: {len(rows)} rows")

# Generate unique emails
def unique_email():
    while True:
        email = fake.email()
        if email not in used_emails:
            used_emails.add(email)
            return email

### Generate mock data for institutions ###

institutions = []
for i in range(1, NUM_INSTITUTIONS + 1):
    # creating university data from list of universities
    name = UNIVERSITY_NAMES[i - 1]
    institutions.append((i, name, "university"))

# Adding FocusFlow Inc. as a company institution
COMPANY_ID = NUM_INSTITUTIONS + 1
institutions.append((COMPANY_ID, "FocusFlow Inc.", "company"))
NUM_INSTITUTIONS_TOTAL = len(institutions)

write_csv("01_institutions.csv",
          ["institution_id", "name", "type"],
          institutions)


### Generate mock data for departments ###

departments = []
dept_id = 1
inst_departments = {}
 
for inst_id, _, _ in institutions:
    # Each institution gets a random subset of departments
    dept_names = random.sample(ALL_DEPARTMENT_NAMES, min(DEPARTMENTS_PER_INSTITUTION, len(ALL_DEPARTMENT_NAMES)))
    inst_departments[inst_id] = []
    # Create department entries for the institution
    for name in dept_names:
        departments.append((dept_id, inst_id, name))
        inst_departments[inst_id].append((dept_id, name))
        dept_id += 1
 
write_csv("02_departments.csv",
          ["department_id", "institution_id", "name"],
          departments)


### Generate mock data for users (students, professors, analysts, admins) ###

users = []
user_id = 1
# (user_id, institution_id, department_id)
professors = []  
# (user_id, institution_id, department_id) 
students = []     
 
used_emails = set()
 
 ## Professors (at least 1 per department)
# Guarantee every department has at least one professor
for dept_id, inst_id, dept_name in departments:
    pw = fake.sha256()[:60]
    u = (user_id, inst_id, dept_id, fake.first_name(), fake.last_name(),
         unique_email(), pw, "professor", None, None)
    users.append(u)
    professors.append((user_id, inst_id, dept_id))
    user_id += 1
 
# Additional random professors
extra_profs = max(0, NUM_PROFESSORS - len(professors))
for _ in range(extra_profs):
    inst = random.choice(institutions)
    dept = random.choice(inst_departments[inst[0]])
    pw = fake.sha256()[:60]
    # Ensuring profs are only associated with academic institutions
    u = (user_id, inst[0], dept[0], fake.first_name(), fake.last_name(),
         unique_email(), pw, "professor", None, None)
    users.append(u)
    professors.append((user_id, inst[0], dept[0]))
    user_id += 1
 
## Students 
for _ in range(NUM_STUDENTS):
    inst = random.choice(institutions)
    dept = random.choice(inst_departments[inst[0]])
    pw = fake.sha256()[:60]
    major = random.choice(MAJORS)
    year = random.choice([1, 2, 3, 4])
    # Ensuring students are only associated with academic institutions
    u = (user_id, inst[0], dept[0], fake.first_name(), fake.last_name(),
         unique_email(), pw, "student", major, year)
    users.append(u)
    students.append((user_id, inst[0], dept[0]))
    user_id += 1
 
## Analysts
for _ in range(NUM_ANALYSTS):
    pw = fake.sha256()[:60]
    # Ensuring analysts are only associated with Focus Flow Inc.
    u = (user_id, COMPANY_ID, None, fake.first_name(), fake.last_name(),
         unique_email(), pw, "analyst", None, None)
    users.append(u)
    user_id += 1

## Admins 
for _ in range(NUM_ADMINS):
    pw = fake.sha256()[:60]
    # Ensuring Admins are only associated with Focus Flow Inc.
    u = (user_id, COMPANY_ID, None, fake.first_name(), fake.last_name(),
         unique_email(), pw, "admin", None, None)
    users.append(u)
    user_id += 1
 
write_csv("03_users.csv",
          ["user_id", "institution_id", "department_id", "first_name",
           "last_name", "email", "password", "role", "major", "year"],
          users)

### Generate mock data for courses ###

courses = []
course_id = 1
# department_id: list of course_ids
dept_courses = {}  
 # department_id: list of professor user_ids
dept_professors = {}

for prof_uid, prof_inst, prof_dept in professors:
    dept_professors.setdefault(prof_dept, []).append(prof_uid)
 
for dept_id, inst_id, dept_name in departments:
    # Get professors in this department
    profs_in_dept = dept_professors.get(dept_id, [])
    if not profs_in_dept:
        # pick any professor from same institution
        profs_in_dept = [p[0] for p in professors if p[1] == inst_id]
 
    # Get course titles for this department
    if dept_name in COURSE_PREFIXES:
        prefix, titles = COURSE_PREFIXES[dept_name]
    else:
        prefix = dept_name[:3].upper()
        titles = [f"{dept_name} Topics {i}" for i in range(1, 8)]
 
    num_courses = random.randint(max(1, COURSES_PER_DEPARTMENT - 1), COURSES_PER_DEPARTMENT + 2)
    selected_titles = random.sample(titles, min(num_courses, len(titles)))
 
    dept_courses[dept_id] = []
    for idx, title in enumerate(selected_titles):
        code = f"{prefix} {random.randint(100, 499)}"
        prof = random.choice(profs_in_dept)
        courses.append((course_id, prof, dept_id, title, code))
        dept_courses[dept_id].append(course_id)
        course_id += 1
 
write_csv("04_courses.csv",
          ["course_id", "professor_id", "department_id", "title", "course_code"],
          courses)


### Generate mock data for enrollments ###

enrollments = []
enrollment_id = 1
# user_id: list of course_ids 
student_courses = {}  
 
# institution_id : list of course_ids
inst_courses = {}
for c_id, _, d_id, _, _ in courses:
    for dept_did, dept_inst, _ in departments:
        if dept_did == d_id:
            inst_courses.setdefault(dept_inst, []).append(c_id)
            break
 
for stu_uid, stu_inst, stu_dept in students:
    available = inst_courses.get(stu_inst, [])
    if not available:
        continue
    num_enroll = min(random.randint(ENROLLMENTS_PER_STUDENT - 1, ENROLLMENTS_PER_STUDENT + 2), len(available))
    chosen = random.sample(available, num_enroll)
    student_courses[stu_uid] = chosen
 
    for crs_id in chosen:
        enrolled_at = fake.date_time_between(start_date="-6m", end_date="-1m")
        enrollments.append((enrollment_id, stu_uid, crs_id, enrolled_at.strftime("%Y-%m-%d %H:%M:%S")))
        enrollment_id += 1
 
write_csv("05_enrollments.csv",
          ["enrollment_id", "user_id", "course_id", "enrolled_at"],
          enrollments)

### Generate mock data for assignments ###
assignments = []
assignment_id = 1
# course_id : list of assignment_ids
course_assignments = {}  
 
for c_id, _, _, _, _ in courses:
    num_assign = random.randint(ASSIGNMENTS_PER_COURSE - 2, ASSIGNMENTS_PER_COURSE + 2)
    course_assignments[c_id] = []
 
    for n in range(1, num_assign + 1):
        template = random.choice(ASSIGNMENT_TYPES)
        title = template.format(n=n)
        description = fake.paragraph(nb_sentences=3)
        due_date = fake.date_between(start_date="-2m", end_date="+2m")
        time_benchmark = random.choice([30, 45, 60, 90, 120, 180, 240])
 
        assignments.append((assignment_id, c_id, title, description,
                            due_date.strftime("%Y-%m-%d"), time_benchmark))
        course_assignments[c_id].append(assignment_id)
        assignment_id += 1
 
write_csv("06_assignments.csv",
          ["assignment_id", "course_id", "title", "description", "due_date", "time_benchmark"],
          assignments)


### Generate mock data for tasks ###
tasks = []
task_id = 1
# user_id :list of (task_id, category)
user_tasks = {}  
 
for stu_uid, _, _ in students:
    user_tasks[stu_uid] = []
    enrolled_courses = student_courses.get(stu_uid, [])
 
    # School tasks (linked to assignments)
    for crs_id in enrolled_courses:
        for a_id in course_assignments.get(crs_id, []):
            title = f"Complete assignment #{a_id}"
            priority = random.choice(["low", "medium", "high"])
            time_alloc = random.choice([30, 45, 60, 90, 120])
            status = random.choices(
                ["not_started", "in_progress", "completed"],
                weights=[0.3, 0.3, 0.4]
            )[0]
            tasks.append((task_id, stu_uid, a_id, title, "school",
                          priority, time_alloc, status))
            user_tasks[stu_uid].append((task_id, "school"))
            task_id += 1
 
    # Non-school tasks
    other_categories = ["work", "extracurricular", "personal"]
    num_other = random.randint(2, 5)
    for _ in range(num_other):
        cat = random.choice(other_categories)
        title_map = {
            "work": ["Shift at cafe", "Freelance project", "Update resume",
                     "Team meeting prep", "Submit timesheet"],
            "extracurricular": ["Club meeting", "Volunteer event", "Practice session",
                                "Organize fundraiser", "Rehearsal"],
            "personal": ["Grocery shopping", "Workout", "Call family",
                         "Clean apartment", "Meal prep", "Laundry"]
        }
        title = random.choice(title_map[cat])
        priority = random.choice(["low", "medium", "high"])
        time_alloc = random.choice([15, 30, 45, 60, 90])
        status = random.choices(
            ["not_started", "in_progress", "completed"],
            weights=[0.25, 0.25, 0.5]
        )[0]
        tasks.append((task_id, stu_uid, None, title, cat,
                      priority, time_alloc, status))
        user_tasks[stu_uid].append((task_id, cat))
        task_id += 1
 
write_csv("07_tasks.csv",
          ["task_id", "user_id", "assignment_id", "title", "category",
           "priority", "time_allocated", "status"],
          tasks)


### Generate mock data for timer sessions ###
timer_sessions = []
session_id = 1
 
for stu_uid, _, _ in students:
    for t_id, _ in user_tasks.get(stu_uid, []):
        num_sessions = random.randint(0, TIMER_SESSIONS_PER_TASK)
        for _ in range(num_sessions):
            session_type = random.choices(["pomodoro", "custom"], weights=[0.7, 0.3])[0]
            start = fake.date_time_between(start_date="-3m", end_date="now")
 
            if session_type == "pomodoro":
                duration = 25  # standard pomodoro
            else:
                duration = random.choice([15, 30, 45, 60, 90])
 
            end = start + timedelta(minutes=duration)
            timer_sessions.append((session_id, t_id, stu_uid,
                                   start.strftime("%Y-%m-%d %H:%M:%S"),
                                   end.strftime("%Y-%m-%d %H:%M:%S"),
                                   duration, session_type))
            session_id += 1
 
write_csv("08_timer_sessions.csv",
          ["session_id", "task_id", "user_id", "start_time", "end_time",
           "duration", "session_type"],
          timer_sessions)

### Generate mock data for scores ###
prod_scores = []
score_id = 1
base_date = datetime.now() - timedelta(weeks=WEEKS_OF_SCORES)
 
for stu_uid, _, _ in students:
    for w in range(WEEKS_OF_SCORES):
        week_start = (base_date + timedelta(weeks=w)).date()
        # Monday of that week
        week_start = week_start - timedelta(days=week_start.weekday())
        score = round(random.uniform(20.0, 100.0), 2)
        prod_scores.append((score_id, stu_uid, score, week_start.strftime("%Y-%m-%d")))
        score_id += 1
 
write_csv("09_productivity_scores.csv",
          ["score_id", "user_id", "score", "week_start_date"],
          prod_scores)

### Generate mock data for notifications ###
notifications = []
notif_id = 1
 
for stu_uid, _, _ in students:
    enrolled = student_courses.get(stu_uid, [])
    all_assignment_ids = []
    for crs in enrolled:
        all_assignment_ids.extend(course_assignments.get(crs, []))
 
    if not all_assignment_ids:
        continue
 
    num_notifs = random.randint(1, NOTIFICATIONS_PER_USER)
    for _ in range(num_notifs):
        a_id = random.choice(all_assignment_ids)
        message = random.choice([
            f"Assignment #{a_id} just assigned!"
            f"Reminder: Assignment #{a_id} is due soon!",
            f"Don't forget to submit assignment #{a_id}.",
            f"Assignment #{a_id} deadline approaching.",
            f"You have an upcoming deadline for assignment #{a_id}.",
        ])
        sent_at = fake.date_time_between(start_date="-2m", end_date="now")
        notifications.append((notif_id, stu_uid, a_id, message,
                              sent_at.strftime("%Y-%m-%d %H:%M:%S")))
        notif_id += 1
 
write_csv("10_notifications.csv",
          ["notification_id", "user_id", "assignment_id", "message", "sent_at"],
          notifications)


### Generate mock data for activity logs ###
activity_logs = []
log_id = 1
 
for stu_uid, _, _ in students:
    for t_id, cat in user_tasks.get(stu_uid, []):
        num_logs = random.randint(0, 3)
        for _ in range(num_logs):
            duration = random.choice([15, 25, 30, 45, 60, 90, 120])
            logged_at = fake.date_time_between(start_date="-3m", end_date="now")
            archived = random.choices([True, False], weights=[0.2, 0.8])[0]
            activity_logs.append((log_id, stu_uid, t_id, cat, duration,
                                  logged_at.strftime("%Y-%m-%d %H:%M:%S"), archived))
            log_id += 1
 
write_csv("11_activity_logs.csv",
          ["log_id", "user_id", "task_id", "category", "duration", "logged_at", "archived"],
          activity_logs)


# Sanity checks
print(f"\n{'='*50}")
print(f"All CSV files written to '{OUTPUT_DIR}/' directory")
print(f"{'='*50}")
print(f"  Institutions:        {len(institutions)}")
print(f"  Departments:         {len(departments)}")
print(f"  Users:               {len(users)}")
print(f"    - Professors:      {len(professors)}")
print(f"    - Students:        {NUM_STUDENTS}")
print(f"    - Analysts:        {NUM_ANALYSTS}")
print(f"    - Admins:          {NUM_ADMINS}")
print(f"  Courses:             {len(courses)}")
print(f"  Enrollments:         {len(enrollments)}")
print(f"  Assignments:         {len(assignments)}")
print(f"  Tasks:               {len(tasks)}")
print(f"  Timer Sessions:      {len(timer_sessions)}")
print(f"  Productivity Scores: {len(prod_scores)}")
print(f"  Notifications:       {len(notifications)}")
print(f"  Activity Logs:       {len(activity_logs)}")
print(f"{'='*50}\n")
