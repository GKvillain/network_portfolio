# Run Instructions

## Step 1: Open 3 terminals

## Step 2: Modify config.py for each node

### Node A

BASE_PORT = 11000
PEER_PORTS = [11001, 11002]

### Node B

BASE_PORT = 11001
PEER_PORTS = [11000, 11002]

### Node C

BASE_PORT = 11002
PEER_PORTS = [11000, 11001]

---

## Step 3: Run each node

python node.py

---

## Expected Behavior

- Tokens move between nodes
- Tokens are read once (state collapse)
- Expired tokens disappear
- Some tokens randomly never get forwarded

---

## Experiments

- Reduce TOKEN_EXPIRY to 3 → observe loss
- Increase UPDATE_INTERVAL → slower network
- Change probability → more/less delivery

---

## Key Insight

Reading a message destroys it.
