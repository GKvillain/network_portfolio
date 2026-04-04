# WEEK 9 – Bio-Inspired Routing

## Overview

This project simulates pheromone-based routing inspired by ant colony behavior.

Nodes:

- Reinforce successful paths
- Decay old paths
- Forward messages probabilistically

---

## How to Run

### Step 1: Open 3 terminals

### Terminal 1

Edit config.py:
BASE_PORT = 10000
PEER_PORTS = [10001, 10002]

Run:
python node.py

---

### Terminal 2

BASE_PORT = 10001
PEER_PORTS = [10000, 10002]

Run:
python node.py

---

### Terminal 3

BASE_PORT = 10002
PEER_PORTS = [10000, 10001]

Run:
python node.py

---

## Expected Behavior

- Nodes send messages to peers
- Successful routes get reinforced
- Weak routes decay over time
- Messages prefer "strong" paths

---

## Key Concept

This mimics ant colony optimization:

- Ants leave pheromones on good paths
- Short/better paths accumulate more pheromone
- Weak paths fade away

---

## Debug Tips

- If nothing forwards → threshold too high
- If one path dominates → decay too low
- If spam → reinforcement too high
