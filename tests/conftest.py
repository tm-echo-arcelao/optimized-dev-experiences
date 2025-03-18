import pytest
import os
import sys
import tempfile

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app as app_module
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    # Create the database schema
    with flask_app.app_context():
        conn = app_module.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()
    
    yield flask_app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner() 