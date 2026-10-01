# Computer Systems Labs

Three labs from Computer Science II at IE School of Science and Technology (Master in Computer Science and Business Technology, 2025 to 2026). Course starter code and test harnesses are not included.

## `mips-assembly/`

MIPS assembly exercises for a MARS/SPIM-style simulator.

- `lab3.asm`: reads up to five integers, prints them as a list, and sums the even ones
- `main.py`: the Python reference the assembly mirrors
- `mips1.asm`, `mips2.asm`: shorter exercises

## `ticket-store-threads/`

A ticket store simulated with threads. Each customer runs as a thread, a semaphore limits how many are in the store at once, and VIP customers get priority.

- `ticket_store.py`: the simulation
- `tests/customers.json`: sample customers

## `tcp-chat-server/`

A multi-client chat over TCP sockets. The server gives each client its own thread, guards the client list and message history with locks, accepts up to 10 connections, and backs up the conversation to a file.

```
python server.py
python client.py
```

## Stack

MIPS assembly; Python standard library (`threading`, `socket`, `signal`).
