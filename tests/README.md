# Todo App Tests

This directory contains tests for the Flask Todo application.

## Running Tests

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_todo_app.py
```

To run a specific test:

```bash
pytest tests/test_todo_app.py::test_add_todo
```

To run tests with verbose output:

```bash
pytest -v
```

## Test Structure

- `conftest.py` - Contains pytest fixtures for setting up the test environment
- `test_todo_app.py` - Tests for the app routes and functionality
- `test_db.py` - Tests for the database functionality
- `test_templates.py` - Tests for the template rendering

## Notes

- Tests use an in-memory SQLite database to ensure they don't affect the production database
- Each test runs in isolation with a fresh database 