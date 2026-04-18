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

# Helper function to write CSV files with mock data 
def write_csv(filename, headers, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"  ✓ {filename}: {len(rows)} rows")

