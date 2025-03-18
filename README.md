# Flask Todo App

A simple to-do application built with Flask.

## Setup

### Using Poetry and Pyenv

1. Install Pyenv and Poetry (if not already installed):
   - [Pyenv Installation](https://github.com/pyenv/pyenv)
   - [Poetry Installation](https://python-poetry.org/docs/)

2. Install Python version using Pyenv:
   ```
   pyenv install
   ```

3. Install dependencies using Poetry:
   ```
   poetry sync
   ```

4. Run the application:
   ```
   poetry run python app.py
   ```

### Alternative Setup (without Poetry)

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and navigate to http://127.0.0.1:5000
