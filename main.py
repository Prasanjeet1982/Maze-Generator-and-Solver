from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from typing import List, Tuple
import random
from queue import PriorityQueue

app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

class MazeGenerator:
    @staticmethod
    def generate(width, height):
        """
        Generate a maze using the recursive backtracking algorithm.

        Args:
            width (int): The width of the maze.
            height (int): The height of the maze.

        Returns:
            List[List[str]]: A 2D list representing the generated maze.
        """
        if width <= 1 or height <= 1:
            raise ValueError("Width and height must be greater than 1.")

        maze = [["#" for _ in range(width)] for _ in range(height)]

        def backtrack(x, y):
            maze[y][x] = " "
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == "#":
                    maze[(y + ny) // 2][(x + nx) // 2] = " "
                    backtrack(nx, ny)

        start_x, start_y = random.randint(0, (width - 1) // 2) * 2, random.randint(0, (height - 1) // 2) * 2
        backtrack(start_x, start_y)

        maze[0][1] = " "
        maze[height - 1][width - 2] = " "

        return maze

class MazeSolver:
    @staticmethod
    def solve(maze):
        """
        Solve a maze using the A* algorithm.

        Args:
            maze (List[List[str]]): A 2D list representing the maze.

        Returns:
            List[Tuple[int, int]] or None: A list of coordinates representing the path,
            or None if no path is found.
        """
        width = len(maze[0])
        height = len(maze)

        def heuristic(node):
            return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

        open_set = PriorityQueue()
        open_set.put((0, start))

        came_from = {}
        g_score = {node: float("inf") for row in maze for node in row}
        g_score[start] = 0

        while not open_set.empty():
            _, current = open_set.get()

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == " ":
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score[(nx, ny)]:
                        came_from[(nx, ny)] = current
                        g_score[(nx, ny)] = tentative_g_score
                        f_score = tentative_g_score + heuristic((nx, ny))
                        open_set.put((f_score, (nx, ny)))

        return None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the index page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(request: Request, width: int = Form(...), height: int = Form(...)):
    """
    Generate a maze based on user input.

    Args:
        request (Request): The incoming request.
        width (int): The width of the maze.
        height (int): The height of the maze.

    Returns:
        TemplateResponse: The maze page template with the generated maze.
    """
    try:
        maze = MazeGenerator.generate(width, height)
        return templates.TemplateResponse("maze.html", {"request": request, "maze": maze})
    except ValueError as ve:
        return templates.TemplateResponse("index.html", {"request": request, "error_message": str(ve)})

@app.post("/solve")
async def solve(request: Request, maze: List[List[str]] = Form(...)):
    """
    Solve a maze based on user input.

    Args:
        request (Request): The incoming request.
        maze (List[List[str]]): A 2D list representing the maze.

    Returns:
        TemplateResponse: The maze page template with the solved path or an error message.
    """
    start = (1, 0)
    goal = (len(maze[0]) - 2, len(maze) - 1)
    path = MazeSolver.solve(maze)

    if path:
        for node in path:
            maze[node[1]][node[0]] = "."
    else:
        return templates.TemplateResponse("maze.html", {"request": request, "maze": maze, "error_message": "No path found."})

    return templates.TemplateResponse("maze.html", {"request": request, "maze": maze})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
