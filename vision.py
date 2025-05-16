# vision.py

import os
import json

GRID_STEP = 2
MEMORY_FILE = "learned_obstacles.json"

def round_grid(x, z):
    return (round(x / GRID_STEP) * GRID_STEP, round(z / GRID_STEP) * GRID_STEP)

# for Loading learned obstacles from file
def load_learned_obstacles(path=MEMORY_FILE):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        try:
            data = json.load(f)
            return {tuple(item) for item in data}
        except json.JSONDecodeError:
            return set()

# for Saving updated obstacle memory
def save_learned_obstacles(obs_set, path=MEMORY_FILE):
    with open(path, "w") as f:
        json.dump(list(obs_set), f)
