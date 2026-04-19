# FocusFlow

FocusFlow is a productivity tracking app for students, professors, data analysts, and system administrators. Students can manage tasks and run focus timers, professors can track how students are spending their time, and analysts and admins have tools to monitor and maintain platform data.

**Team:** Liam Dowd, Ben Assa, Chloe Scanlan, Ryan McCarthy, Nicholas Boden

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

## Setup

Clone the repo and create the `.env` file from the template:

```bash
git clone <repo-url>
cd FocusFlow
cp api/.env.template api/.env
```

Open `api/.env` and fill in your values:

```
SECRET_KEY=<any random string>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=focusflow
MYSQL_ROOT_PASSWORD=<your chosen password>
```

Then start the containers:

```bash
docker compose up -d
```

The app will be available at [http://localhost:8501](http://localhost:8501) and the API at [http://localhost:4000](http://localhost:4000). On first run the database is created and populated automatically from the SQL files in `database-files/`.

If API calls fail on first launch, the API may have started before MySQL finished initializing. Run `docker compose restart api` to fix this.

## Rebuilding the Database

If you change any SQL files, recreate the database container to re-run them:

```bash
docker compose down db -v
docker compose up db -d
```

## Regenerating Mock Data

```bash
pip install faker
python database-files/generate_mock_data.py
python database-files/convert_to_insert.py
```

This rewrites `02_focusFlow_data.sql`. Rebuild the database container afterwards.

## Functionality

FocusFlow supports four personas, each accessible from the home page. Select a role to log in as a user from that group.

### Student

The student experience is centered around task management and focus tracking. From the home page, students can view all their tasks filtered by category (school, work, extracurricular, personal) and jump directly into a focus session for any task. The **Task Studio** page allows students to add new tasks and delete existing ones. The **Focus Timer** page runs a 30-minute Pomodoro-style countdown, automatically recording the session to the database when stopped. The **Analytics** page shows a weekly productivity score trend, a breakdown of time spent by category, and a leaderboard ranking against other students at the same institution.

### Professor

Professors log in by selecting their profile from a list pulled from the database. From there they can manage their courses — creating new ones or deleting existing ones. The **Student Roster** page shows all students enrolled in a selected course, their total logged focus time, and a bar chart showing the distribution of time across the class. Professors can also add or remove students from a course directly from this page. The **Assignments** page lets professors create assignments with a title, description, due date, and suggested time benchmark, and delete existing ones.

### Data Analyst

Analysts have access to six views of aggregate platform data. They can explore correlations between study time and productivity scores, flag concerning trends in user activity, filter student data by major and year, view time breakdowns by category, check how much data is being shared per institution, and export filtered activity records.

### System Administrator

Admins have five tools for maintaining data quality and monitoring platform health. They can identify and remove duplicate activity log entries, update incorrect records, manage activity categories, monitor system-wide usage across all institutions, and archive old activity data.

## Demo Video

[Link](#)
