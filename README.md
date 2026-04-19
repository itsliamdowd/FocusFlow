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

## Demo Video

[Link](#)
