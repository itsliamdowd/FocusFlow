import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker
 
fake = Faker()
Faker.seed(42)
random.seed(42)
 
OUTPUT_DIR = "mock_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Constants for data generation
NUM_INSTITUTIONS = 5
DEPARTMENTS_PER_INSTITUTION = 8 
NUM_STUDENTS = 100
NUM_PROFESSORS = 30
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
    "Georgetown University"
]

# Ensuring each department has a unique course prefix and a set of course names
COURSE_PREFIXES = {
    "Engineering": ("ENG", ["Statics", "Dynamics", "Thermodynamics", "Circuit Analysis",
                            "Fluid Mechanics", "Materials Science", "Control Systems"]),
    "Health Sciences": ("HSC", ["Anatomy", "Physiology", "Epidemiology", "Biostatistics",
                                "Public Health", "Nutrition", "Pharmacology"]),
    "Computer Science": ("CS", ["Data Structures", "Algorithms", "Operating Systems",
                                "Databases", "Machine Learning", "Networks", "Software Engineering"]),
    "Business": ("BUS", ["Accounting", "Marketing", "Finance", "Management",
                         "Business Ethics", "Entrepreneurship", "Operations"]),
    "Art and Media": ("ART", ["Drawing", "Digital Media", "Photography", "Film Studies",
                              "Graphic Design", "Art History", "Animation"]),
    "Literature": ("LIT", ["American Literature", "British Literature", "Creative Writing",
                           "Poetry", "World Literature", "Literary Theory", "Drama"]),
    "Social Science": ("SOC", ["Sociology", "Anthropology", "Political Science",
                               "Geography", "Criminology", "Urban Studies", "Demography"]),
    "Science": ("SCI", ["Biology", "Chemistry", "Physics", "Geology",
                        "Astronomy", "Environmental Science", "Biochemistry"]),
    "Law": ("LAW", ["Constitutional Law", "Criminal Law", "Contract Law",
                    "Tort Law", "International Law", "Legal Writing", "Property Law"]),
    "Humanities": ("HUM", ["Ethics", "History", "Cultural Studies", "Linguistics",
                           "Religious Studies", "Classics", "Gender Studies"]),
    "Mathematics": ("MTH", ["Calculus", "Linear Algebra", "Probability", "Statistics",
                            "Discrete Math", "Real Analysis", "Number Theory"]),
    "Education": ("EDU", ["Curriculum Design", "Child Development", "Educational Psychology",
                          "Pedagogy", "Classroom Management", "Special Education", "Assessment"]),
    "Psychology": ("PSY", ["Cognitive Psychology", "Developmental Psychology", "Abnormal Psychology",
                           "Research Methods", "Social Psychology", "Neuroscience", "Clinical Psychology"]),
    "Philosophy": ("PHL", ["Logic", "Metaphysics", "Epistemology", "Ethics",
                           "Philosophy of Mind", "Aesthetics", "Political Philosophy"]),
    "Economics": ("ECN", ["Microeconomics", "Macroeconomics", "Econometrics", "Game Theory",
                          "International Trade", "Labor Economics", "Development Economics"]),
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
inst_departments = {}  )
 
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

