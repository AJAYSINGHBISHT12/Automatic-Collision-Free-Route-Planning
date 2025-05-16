# 🤖 Autonomous Robot Navigation – A* Path Planning Extension

This project is an enhanced version of the original robot simulator:  
🔗 https://github.com/terafac/sim-1

It integrates a Three.js-based robot simulator with a Flask and WebSocket backend, and adds **autonomous navigation**, **collision memory**, and a **goal marker**, enabling the robot to reach a target without manual input.

---

## 🚀 Features Overview

### ✅ Autonomous Path Planning
- Implements the **A\*** algorithm to find a collision-free path from `(0, 0)` to `(24, 24)`.

### ✅ Collision Detection and Learning
- Robot detects obstacles during movement and logs them in `learned_obstacles.json`.
- Learns to avoid previously collided locations on future runs.

### ✅ Dynamic Replanning
- When a collision occurs, the robot **replans automatically** from its current position.

### ✅ Visual Goal Marker
- A red flag on a yellow stick at `(24, 24)` visually marks the destination in the simulator.

---

## 🔧 Setup Instructions

### 1️⃣ Install Requirements
Ensure you have Python 3.7+ installed. Then run:
```bash
pip install flask websockets
