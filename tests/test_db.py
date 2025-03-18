import pytest
import sqlite3
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import init_db, get_db_connection

def test_init_db(app):
    """Test that the database initialization creates the right schema."""
    # The app fixture already initialized the DB, so let's check the schema
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if the todos table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='todos'
        """)
        table_exists = cursor.fetchone() is not None
        assert table_exists
        
        # Check the table schema
        cursor.execute("PRAGMA table_info(todos)")
        columns = {column['name']: column for column in cursor.fetchall()}
        
        # Check expected columns
        assert 'id' in columns
        assert 'task' in columns
        assert 'completed' in columns
        assert 'created_at' in columns
        
        # Check column types
        assert columns['id']['type'] == 'INTEGER'
        assert columns['task']['type'] == 'TEXT'
        assert columns['completed']['type'] == 'BOOLEAN'
        assert columns['created_at']['type'] == 'TIMESTAMP'
        
        # Check primary key
        assert columns['id']['pk'] == 1
        
        # Check NOT NULL constraints
        assert columns['task']['notnull'] == 1
        
        conn.close()

def test_db_connection(app):
    """Test that the database connection works."""
    with app.app_context():
        conn = get_db_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        assert conn.row_factory == sqlite3.Row
        conn.close() 