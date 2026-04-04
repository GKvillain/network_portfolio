# WEEK 2 – UDP Communication (Connectionless Unicast)

**Teaching Intent**
Week 2 removes comfort. There is no handshake, no memory, no apology.
Students must experience what it means when the network does not care.

---

## Overview

This lab introduces **UDP socket programming**, contrasting sharply with Week 1’s TCP discipline.

Messages may:

- Arrive late
- Arrive out of order
- Never arrive at all

And that is **not a bug**. It is a feature.

---

## Learning Outcomes

By completing this lab, you will:

- Understand the **connectionless communication model**
- Implement **UDP sender and receiver**
- Analyze **trade-offs between performance and reliability**
- Develop:
  - Risk awareness
  - Defensive programming mindset
  - System-level reasoning

---

## Key Concepts

| Concept     | TCP                        | UDP                    |
| ----------- | -------------------------- | ---------------------- |
| Connection  | Required (3-way handshake) | Not required           |
| Reliability | Guaranteed delivery        | Best-effort only       |
| Ordering    | Guaranteed                 | Not guaranteed         |
| Speed       | Slower                     | Faster                 |
| Overhead    | High                       | Low                    |
| Use Case    | Web, file transfer         | Streaming, gaming, IoT |

---

## Repository Structure

```
week02-udp-unicast-basic/
├── README.md
├── sender.py
├── receiver.py
├── config.py
└── docs/
    └── run_instructions.md
```

---

## Quick Start

### 1. Configure

Edit `config.py`:

```python
HOST = "127.0.0.1"
PORT = 6000
BUFFER_SIZE = 1024
```

---

### 2. Run Receiver (Terminal 1)

```bash
python receiver.py
```

Expected:

```
[RECEIVER] Listening on 127.0.0.1:6000
```

---

### 3. Run Sender (Terminal 2)

```bash
python sender.py
```

Expected:

```
[SENDER] Message sent
```

---

## Implementation Deep Dive

### config.py

```python
HOST = "127.0.0.1"
PORT = 6000
BUFFER_SIZE = 1024
```

---

### receiver.py

```python
import socket
from config import HOST, PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"[RECEIVER] Listening on {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"[RECEIVER] From {addr}: {data.decode()}")
```

**Key Points**

- `SOCK_DGRAM` = UDP
- No `listen()` or `accept()`
- `recvfrom()` returns (data, sender address)
- Stateless design

---

### sender.py

```python
import socket
from config import HOST, PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello via UDP"
sock.sendto(message.encode(), (HOST, PORT))

print("[SENDER] Message sent")
sock.close()
```

**Key Points**

- No connection setup
- `sendto()` specifies destination
- No ACK or confirmation
- Fire-and-forget behavior

---

## TCP vs UDP

### TCP (Reliable)

```
Client              Server
  |                   |
  |--- SYN ---------->|
  |<-- SYN-ACK -------|
  |--- ACK ---------->|
  |--- DATA --------->|
  |<-- ACK -----------|
```

---

### UDP (Unreliable)

```
Sender              Receiver
  |                   |
  |--- DATAGRAM ----->|
  |                   |
```

---

## UDP Failure Scenario

```
Sender              Network              Receiver
  |                    |                    |
  |--- Packet 1 ------>|------------------->|
  |--- Packet 2 ------>|   (DROPPED)        |
  |--- Packet 3 ------>|------------------->|
```

Receiver sees:

```
1, 3
```

Missing:

```
2
```

---

## Testing Scenarios

### Test 1: Normal Communication

- Start receiver
- Run sender
  ✅ Message received

---

### Test 2: Multiple Sends

Run sender multiple times:

```bash
python sender.py
python sender.py
```

✅ Messages may all arrive
❌ Or some may be lost

---

### Test 3: No Receiver (Critical Test)

Do NOT start receiver.

Run:

```bash
python sender.py
```

Result:

- Sender shows success
- No message received

**This proves UDP is unreliable.**

---

## Common Mistakes

| Mistake               | Reason            | Fix                           |
| --------------------- | ----------------- | ----------------------------- |
| Message lost          | UDP is unreliable | Accept or handle at app layer |
| Expecting connection  | UDP is stateless  | No session exists             |
| Waiting for reply     | No ACK            | Add timeout logic             |
| Out-of-order messages | Network routing   | Use sequence numbers          |
| Data truncated        | Buffer too small  | Increase BUFFER_SIZE          |

---

## Extension A: Sequence Numbers

Detect packet loss:

```python
# sender
for i in range(5):
    msg = f"{i}|Hello"
    sock.sendto(msg.encode(), (HOST, PORT))
```

```python
# receiver
received = set()
msg_id, text = data.decode().split("|")
```

---

## Extension B: Manual ACK (Build Reliability)

```python
# receiver
sock.sendto(b"ACK", addr)
```

```python
# sender
sock.settimeout(2)
```

You just recreated **TCP behavior on UDP**.

---

## Extension C: Rate Control

Send fast:

```python
for i in range(1000):
    sock.sendto(str(i).encode(), (HOST, PORT))
```

Observe:

- Packet drops
- Receiver overload

---

## Real-World Applications

| System      | Why UDP                      |
| ----------- | ---------------------------- |
| DNS         | Fast request-response        |
| VoIP        | Real-time audio              |
| Gaming      | Low latency updates          |
| Streaming   | Drop frames instead of delay |
| IoT Sensors | Continuous lightweight data  |

---

## When NOT to Use UDP

Do NOT use UDP when:

- Data must be 100% correct
- Order is critical
- Loss is unacceptable

Use TCP instead.

---

## Performance Insight

UDP is faster because:

- No handshake (0-RTT)
- No acknowledgments
- No retransmissions

Trade-off:

- No reliability
- No congestion control

---

## Debugging Checklist

- Receiver started first?
- HOST and PORT match?
- Using `SOCK_DGRAM`?
- Firewall blocking UDP?
- BUFFER_SIZE large enough?
- Multiple processes using same port?

---

## Design Philosophy

UDP does not guarantee:

- Delivery
- Order
- Duplication protection

This is intentional.

Applications must:

- Detect loss
- Handle reordering
- Decide retransmission strategy

**Reliability is an application responsibility.**

---

## Reflection

This lab reveals a fundamental truth:

> The network does not guarantee anything.

Reliability is not built-in.
It must be designed.

UDP forces developers to think beyond APIs
and understand systems under uncertainty.

---

## Key Takeaway

> TCP is safety. UDP is freedom.

Choose based on what your system needs.

---

**Status**: Complete
**Next**: Week 3 – UDP Broadcast
