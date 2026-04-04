# Week 8 – Opportunistic Routing (Basic)

## Overview

This lab simulates opportunistic routing in a delay-tolerant network.

Nodes:

- Maintain delivery probabilities for neighbors
- Forward messages only when probability is high
- Store messages when delivery fails

---

## Features

- Delivery probability table
- Opportunistic forwarding
- Message queue (store-and-forward)
- Dynamic probability updates
- Duplicate message prevention

---

## How to Run

### Step 1: Open multiple terminals

### Step 2: Modify config.py for each node

Example:

Node 1:
BASE_PORT = 9000
PEER_PORTS = [9001, 9002]

Node 2:
BASE_PORT = 9001
PEER_PORTS = [9000, 9002]

Node 3:
BASE_PORT = 9002
PEER_PORTS = [9000, 9001]

---

### Step 3: Run nodes

```bash
python node.py
```
