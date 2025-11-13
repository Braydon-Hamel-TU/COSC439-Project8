# COSC 439 – Multicomputer Chat Project

This repo is for our COSC 439 project where we build a simple multi-computer chat system using sockets.

The basic idea:
- There’s one **server** running on some machine and listening on a port.
- Multiple **clients** connect to that server from different machines (or terminals).
- Clients should be able to:
  - send messages to **everyone**,
  - send **direct messages** to a specific user,
  - and (later) send **files** to another user.

## Project Layout

- `server/`  
  Code for the chat server (handles connections, keeps track of users, broadcasts messages, DMs, file stuff).

- `client/`  
  Code for the chat client (user input, printing messages, and commands like `/dm` and `/sendfile`).

- `docs/`  
  Project write-ups:
  - progress report drafts
  - protocol notes (how messages are formatted)
  - final technical report

## How to Run (will be updated)

This is just the rough plan for now. We’ll update it once the code is actually working.

1. Start the server  
   - Run the server script from the `server/` folder.

2. Start one or more clients  
   - Run the client script from the `client/` folder on different machines or different terminals.

3. Test features  
   - Send a normal message (should go to everyone).
   - Try a direct message to one user.
   - Try sending a small file once that’s implemented.
   
We’ll replace this with real commands and examples after everything is implemented and tested.
