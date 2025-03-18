# Flask Todo App

A simple to-do application built with Flask.

## Setup

### Option 1: Local Setup

1. Install dependencies using uv (recommended):
   ```
   uv pip install -r requirements.txt
   ```
   
   Or using pip:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and navigate to http://127.0.0.1:5000

### Option 2: Using Dev Containers

This project includes configuration for Development Containers, which provides a consistent development environment.

1. Install [Docker](https://www.docker.com/products/docker-desktop) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code.

2. Open the project in VS Code and click on the "Reopen in Container" button when prompted, or use the Command Palette (`F1`) and select "Dev Containers: Reopen in Container".

3. The container will automatically set up the development environment, including installing all dependencies.

## Development Workflow

### Using mise-en-place

This project uses [mise-en-place](https://mise.jdx.dev/) to manage development tools and tasks.

- Run the development server:
  ```
  mise run dev
  ```

- Run tests:
  ```
  mise run test
  ```

### Using uv

[uv](https://github.com/astral-sh/uv) is used as a fast Python package installer and resolver:

- Install dependencies:
  ```
  uv pip install -r requirements.txt
  ```

- Activate a virtual environment and run Python:
  ```
  uv run python app.py
  ```
