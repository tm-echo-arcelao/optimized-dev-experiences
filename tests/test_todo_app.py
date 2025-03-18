import pytest
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, get_db_connection

def test_index_route(client):
    """Test that the index route renders correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h2>Tasks</h2>' in response.data

def test_add_todo(client):
    """Test adding a new todo."""
    # Add a new todo
    response = client.post('/add', data={'task': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_complete_todo(client):
    """Test marking a todo as complete."""
    # First add a todo
    client.post('/add', data={'task': 'Task to Complete'})
    
    # Get the database to find the id of the added task
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE task = 'Task to Complete'")
        todo = cursor.fetchone()
        assert todo is not None, "Todo was not added to the database"
        todo_id = todo['id']
        print(f"\nFound todo with ID: {todo_id}")
        conn.close()
    
    # Mark it as complete
    response = client.get(f'/complete/{todo_id}', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify it's marked as complete in the database
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Debug: List all todos
        cursor.execute("SELECT id, task, completed FROM todos")
        all_todos = cursor.fetchall()
        print("\nAll todos in database after complete request:")
        for t in all_todos:
            print(f"ID: {t['id']}, Task: {t['task']}, Completed: {t['completed']}")
        
        # Check the specific todo
        cursor.execute(f"SELECT completed FROM todos WHERE id = {todo_id}")
        todo = cursor.fetchone()
        assert todo is not None, "Todo was not found in the database"
        completed = todo['completed']
        print(f"\nTodo {todo_id} completed value: {completed}")
        conn.close()
    
    assert completed == 1, f"Todo with ID {todo_id} was not marked as completed"

def test_delete_todo(client):
    """Test deleting a todo."""
    # First add a todo
    client.post('/add', data={'task': 'Task to Delete'})
    
    # Get the database to find the id of the added task
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE task = 'Task to Delete'")
        todo = cursor.fetchone()
        assert todo is not None, "Todo was not added to the database"
        todo_id = todo['id']
        print(f"\nFound todo to delete with ID: {todo_id}")
        conn.close()
    
    # Delete it
    response = client.get(f'/delete/{todo_id}', follow_redirects=True)
    assert response.status_code == 200
    
    # Debug: List all todos after delete
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Debug: List all todos
        cursor.execute("SELECT id, task, completed FROM todos")
        all_todos = cursor.fetchall()
        print("\nAll todos in database after delete request:")
        for t in all_todos:
            print(f"ID: {t['id']}, Task: {t['task']}, Completed: {t['completed']}")
        
        # Check the specific todo
        cursor.execute(f"SELECT * FROM todos WHERE id = {todo_id}")
        todo = cursor.fetchone()
        if todo:
            print(f"\nTodo with ID {todo_id} still exists after delete.")
        else:
            print(f"\nTodo with ID {todo_id} was successfully deleted.")
        conn.close()
    
    assert todo is None, f"Todo with ID {todo_id} was not deleted from the database"

def test_add_empty_todo(client):
    """Test that empty todos are not added."""
    # Get current todos count
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM todos")
        initial_count = cursor.fetchone()['count']
        conn.close()
    
    # Try to add an empty todo
    response = client.post('/add', data={'task': ''}, follow_redirects=True)
    assert response.status_code == 200
    
    # Verify the count didn't change
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM todos")
        new_count = cursor.fetchone()['count']
        conn.close()
    
    assert new_count == initial_count 