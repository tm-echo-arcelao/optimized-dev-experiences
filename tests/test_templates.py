import pytest
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, get_db_connection

def test_index_template(client):
    """Test that the index template renders correctly with todos."""
    # First add a test todo
    client.post('/add', data={'task': 'Template Test Task'})
    
    # Get the index page
    response = client.get('/')
    
    # Check basic HTML structure
    assert b'<!DOCTYPE html>' in response.data
    assert b'<html' in response.data
    assert b'</html>' in response.data
    
    # Check for todo list elements
    assert b'<h2>Tasks</h2>' in response.data
    assert b'<ul' in response.data
    assert b'<form' in response.data
    assert b'<input' in response.data
    
    # Check that our test task is displayed
    assert b'Template Test Task' in response.data

def test_index_with_completed_todo(client):
    """Test that completed todos are displayed correctly."""
    # Add a todo and mark it as complete
    client.post('/add', data={'task': 'Completed Test Task'})
    
    # Get the id of the added task
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE task = 'Completed Test Task'")
        todo = cursor.fetchone()
        assert todo is not None, "Todo was not added to the database"
        todo_id = todo['id']
        conn.close()
    
    # Mark it as complete
    client.get(f'/complete/{todo_id}')
    
    # Get the index page again
    response = client.get('/')
    
    # Check that the completed task is displayed
    assert b'Completed Test Task' in response.data
    
    # Check that the task has some indication of being completed
    # This depends on how completion is displayed in the template,
    # might need adjusting based on the HTML structure
    content = response.data.decode()
    assert 'Completed Test Task' in content
    
    # Verify that the Complete button doesn't appear for this task
    task_html = content.split('Completed Test Task')[1].split('</li>')[0]
    assert 'Complete</a>' not in task_html 