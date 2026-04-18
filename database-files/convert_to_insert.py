import csv
import os
 
INPUT_DIR = "database-files/mock_data"
OUTPUT_FILE = "database-files/02_focusFlow_data.sql"
 
# Map CSV filenames to table names
FILE_TO_TABLE = {
    "01_institutions.csv": "institutions",
    "02_departments.csv": "departments",
    "03_users.csv": "users",
    "04_courses.csv": "courses",
    "05_enrollments.csv": "enrollments",
    "06_assignments.csv": "assignments",
    "07_tasks.csv": "tasks",
    "08_timer_sessions.csv": "timer_sessions",
    "09_productivity_scores.csv": "productivity_scores",
    "10_notifications.csv": "notifications",
    "11_activity_logs.csv": "activity_logs",
}
 
 
def format_value(value):
    """
    Formatting a single value for SQL.
    """
    if value == "" or value is None:
        return "NULL"
    # Booleans
    if value in ("True", "False"):
        return "1" if value == "True" else "0"
    # Numbers (int or float)
    try:
        if "." in value:
            float(value)
            return value
        else:
            int(value)
            return value
    except ValueError:
        pass
    # Strings — escape single quotes
    escaped = value.replace("'", "''")
    return f"'{escaped}'"
 
 
def csv_to_inserts(csv_path, table_name):
    """
    Convert a CSV file to a list of INSERT statements
    """
    statements = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        columns = ", ".join(headers)
 
        for row in reader:
            values = ", ".join(format_value(v) for v in row)
            statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
    return statements
 
 
def main():
    all_statements = []
    all_statements.append("USE focusflow;\n")
    all_statements.append("SET FOREIGN_KEY_CHECKS = 0;\n")
 
    files = sorted(FILE_TO_TABLE.keys())
 
    for filename in files:
        table_name = FILE_TO_TABLE[filename]
        csv_path = os.path.join(INPUT_DIR, filename)
 
        if not os.path.exists(csv_path):
            print(f"{filename} not found, skipping")
            continue
 
        inserts = csv_to_inserts(csv_path, table_name)
        all_statements.append(f"\n-- {table_name} ({len(inserts)} rows)")
        all_statements.append(f"-- {'='*50}")
        all_statements.extend(inserts)
        print(f"{table_name}: {len(inserts)} INSERT statements")
 
    all_statements.append("\nSET FOREIGN_KEY_CHECKS = 1;")
 
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_statements))
 
    print(f"\nDone! Written to {OUTPUT_FILE}")
 
 
if __name__ == "__main__":
    main()