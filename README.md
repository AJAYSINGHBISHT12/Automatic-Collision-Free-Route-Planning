# 🤖 Autonomous Robot Navigation System

This project is an **expansion of the original repository**:  
🔗 https://github.com/terafac/sim-1

It adds **fully autonomous collision-free route planning** using A* pathfinding and dynamic obstacle memory.

---

## 📁 Files Overview

| File                  | Description |
|-----------------------|-------------|
| `vision.py`           | Module for processing captured environment data and managing learned obstacle memory. |
| `path_planner.py`     | Autonomous navigation logic. Plans a route using A*, moves robot, replans on collision. |
| `server.py`           | WebSocket and Flask API server for communication with the simulator. |
| `index.html`          | Three.js-based robot simulator UI. Includes goal flag at position (24, 24). |
| `learned_obstacles.json` | Stores obstacles learned from previous collisions. Auto-updated. |
| `collision_log.json`  | Stores the most recent collision data from simulator. Auto-generated. |
| `README.md`           | Instructions for setup and usage (this file). |

---

## ⚙️ Setup Instructions

### 1️⃣ Install Python Dependencies
Make sure Python 3.7+ is installed.

Then install required packages:
```bash
pip install flask websockets
