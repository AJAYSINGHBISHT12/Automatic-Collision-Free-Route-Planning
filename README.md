# 🤖 Autonomous Robot Navigation – A* Path Planning Extension

This project is an enhanced version of the original robot simulator:  
🔗 https://github.com/terafac/sim-1

We’ve extended it to support **autonomous navigation**, **obstacle memory**, and a **visual goal marker** using A* pathfinding and real-time collision detection.

---

## 🔁 Changes Made

### 🔧 Modified Files

- **`server.py`**
  - Enhanced the WebSocket handler (`ws_handler`) to detect collision messages from the simulator.
  - Added logic to log the collision data into `collision_log.json`:
    ```python
    if data.get("type") == "collision":
        with open("collision_log.json", "w") as f:
            json.dump(data, f)
    ```
  - This allows the robot to dynamically replan its route when it collides with new obstacles.

- **`index.html`**
  - Added a **goal flag** at `(24, 24)` consisting of a **yellow stick and red flag**.
  - Added new **walls and a small house** for better pathfinding realism.
  - 📥 You can download the modified `index.html` here: **[Download Modified Simulator](#)**  
    *(Replace the link with the actual download location if you're sharing this)*

---

### 🆕 New Files Added

1. **`vision.py`**  
   - Handles obstacle memory by saving and loading from `learned_obstacles.json`.
   - Rounds coordinates to a consistent grid using `GRID_STEP`.

2. **`path_planner.py`**  
   - Main autonomous control script.
   - Implements the A* algorithm.
   - Sends movement commands to the robot and replans if a collision occurs.

3. **`learned_obstacles.json`** *(auto-generated)*  
   - Stores positions of obstacles learned from collisions for future runs.

---

## 🧠 How It Works

- The robot starts at `(0, 0)` and automatically finds a path to `(24, 24)` using A*.
- If it collides with an obstacle, the simulator sends a collision message.
- The server logs the collision, and the robot replans a new path dynamically.
- The robot learns and remembers obstacles to improve in subsequent runs.

---

## 🧪 How to Run

### 1️⃣ Install Requirements
```bash
pip install flask websockets


2️⃣ Start the Server:
python server.py

3️⃣ Launch the Simulator:
python -m http.server

4️⃣ Start the Autonomous Robot:
python path_planner.py
