import requests
import time
import json
import os
from queue import PriorityQueue

GRID_STEP = 2
COLLISION_FILE = "collision_log.json"
MEMORY_FILE = "learned_obstacles.json"
MOVE_API = "http://localhost:5000/move"

START = (0, 0)
GOAL = (24, 24)

# for Loading past obstacle memory
def load_learned_obstacles(path=MEMORY_FILE):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        try:
            data = json.load(f)
            return {tuple(item) for item in data}
        except json.JSONDecodeError:
            return set()

# for Saving obstacle memory
def save_learned_obstacles(obs_set, path=MEMORY_FILE):
    with open(path, "w") as f:
        json.dump(list(obs_set), f)

# Rounding real position to grid cell
def round_grid(x, z):
    return (round(x / GRID_STEP) * GRID_STEP, round(z / GRID_STEP) * GRID_STEP)

# To Get neighbors in grid
def neighbors(pos, obstacles):
    x, z = pos
    candidates = [
        (x + GRID_STEP, z),
        (x - GRID_STEP, z),
        (x, z + GRID_STEP),
        (x, z - GRID_STEP),
    ]
    return [n for n in candidates if n not in obstacles]

# Heuristic: Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Pathfinding
def a_star(start, goal, obstacles):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        _, current = frontier.get()
        if current == goal:
            break
        for next_node in neighbors(current, obstacles):
            new_cost = cost_so_far[current] + GRID_STEP
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                frontier.put((priority, next_node))
                came_from[next_node] = current

    if goal not in came_from:
        return []

    # Reconstruct path
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# for Sending move command
def move_to(x, z):
    print(f"Moving to ({x}, {z})")
    res = requests.post(MOVE_API, json={"x": x, "z": z})
    if not res.ok:
        print("❌ Move failed:", res.text)
    time.sleep(0.1)

# for Detecting collision and updating memory
def check_collision(obstacles):
    if not os.path.exists(COLLISION_FILE):
        return None

    try:
        with open(COLLISION_FILE) as f:
            content = f.read().strip()
            if not content:
                return None
            data = json.loads(content)
            if data.get("type") == "collision":
                pos = data["position"]
                obstacle_pos = round_grid(pos["x"], pos["z"])
                print(f"Collision at {obstacle_pos}")
                obstacles.add(obstacle_pos)
                save_learned_obstacles(obstacles)
                return obstacle_pos
    except (json.JSONDecodeError, IOError) as e:
        print("Error reading collision log:", e)
        return None

    return None

def remove_collision_log():
    if os.path.exists(COLLISION_FILE):
        os.remove(COLLISION_FILE)

# Full navigation loop
def autonomous_navigate(start, goal):
    obstacles = load_learned_obstacles()
    print(f"Loaded {len(obstacles)} learned obstacle(s)")

    current = start
    path = a_star(start, goal, obstacles)

    if not path:
        print("No path found!")
        return

    print("Initial Path:", path)

    i = 1  # Skip start
    while i < len(path):
        next_pos = path[i]
        move_to(*next_pos)
        time.sleep(0.5)
        col_pos = check_collision(obstacles)
        if col_pos:
            remove_collision_log()
            print("Replanning...")
            path = a_star(current, goal, obstacles)
            if not path:
                print("❌ No path after replanning.")
                return
            print("New Path:", path)
            i = 1
            continue
        current = next_pos
        i += 1

    print("Finally you Reached Goal! 🕺")

if __name__ == "__main__":
    autonomous_navigate(START, GOAL)
