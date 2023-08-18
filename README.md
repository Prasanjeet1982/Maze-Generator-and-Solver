# Maze-Generator-and-Solver
Maze Generator and Solver: Generate a random maze and allow the player to navigate through it. You can also implement an automatic solver.

# FastAPI Maze Generator and Solver

This is a web-based maze generator and solver built using FastAPI.

## Features

- Generate mazes with custom dimensions.
- Solve generated mazes using the A* algorithm.

## Prerequisites

- Python 3.8 or later
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-maze-generator.git
   ```

2. Navigate to the project directory:
   ```bash
   cd fastapi-maze-generator
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. Open your web browser and navigate to `http://localhost:8000/` to access the maze generator and solver.

3. Generate a maze by providing width and height, then solve it using the A* algorithm.

## Docker Support

You can also run the application in a Docker container. See the provided `Dockerfile` for more details on building and running the container.
---

Feel free to customize this README template with more details about your application, usage instructions, deployment options, screenshots, and any other relevant information. Make sure to replace placeholders like `[Your Name]` with your actual information.

Including clear and concise instructions in your README will help users understand how to use your application and contribute to its success.
