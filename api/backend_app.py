from backend.rest_entry import create_app
import os

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').strip().lower() in {'1', 'true', 'yes'}
    app.run(debug=debug_mode, host='0.0.0.0', port=4000)
