from flask import Flask
from dotenv import load_dotenv
import os
import logging

from backend.db_connection import init_app as init_db
from backend.simple.simple_routes import simple_routes
from backend.ngos.ngo_routes import ngos
from backend.students import student_bp
from backend.professors import professor_bp
from backend.analysts import analyst_bp
from backend.admins import admin_bp


def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    # Load environment variables from the .env file so they are
    # accessible via os.getenv() below.
    load_dotenv()

    # Secret key used by Flask for securely signing session cookies.
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    def required_env(name, cast=str):
        value = os.getenv(name)
        if value is None:
            raise RuntimeError(f"Missing required environment variable: {name}")
        value = value.strip() if isinstance(value, str) else value
        if value == "":
            raise RuntimeError(f"Environment variable {name} cannot be empty")
        try:
            return cast(value)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f"Invalid value for {name}: {value}") from exc

    # Database connection settings — values come from the .env file.
    app.config["MYSQL_DATABASE_USER"] = required_env("DB_USER")
    app.config["MYSQL_DATABASE_PASSWORD"] = required_env("MYSQL_ROOT_PASSWORD")
    app.config["MYSQL_DATABASE_HOST"] = required_env("DB_HOST")
    app.config["MYSQL_DATABASE_PORT"] = required_env("DB_PORT", cast=int)
    app.config["MYSQL_DATABASE_DB"] = required_env("DB_NAME")

    # Register the cleanup hook for the database connection.
    app.logger.info("create_app(): initializing database connection")
    init_db(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each.
    app.logger.info("create_app(): registering blueprints")
    app.register_blueprint(simple_routes)
    app.register_blueprint(ngos, url_prefix="/ngo")
    app.register_blueprint(student_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(analyst_bp)
    app.register_blueprint(admin_bp)

    @app.before_request
    def protect_api_routes():
        # Local-only project: do not enforce API route auth/role checks.
        return None

    return app
