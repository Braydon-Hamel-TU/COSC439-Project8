# COSC 439 – very first server draft
# Super simple chat server using TCP sockets.
# Right now it just:
#   - accepts clients
#   - asks for a username
#   - broadcasts each message to everyone else

import socket
import threading

HOST = "0.0.0.0"   # listen on all network interfaces
PORT = 5000        # you can change this if needed

clients = {}  # socket -> username


def broadcast(message: str, sender_sock=None) -> None:
    """Send message to all connected clients except the sender."""
    for sock in list(clients.keys()):
        if sock is sender_sock:
            continue
        try:
            sock.sendall(message.encode("utf-8"))
        except OSError:
            # if something goes wrong just drop that client
            clients.pop(sock, None)


def handle_client(sock: socket.socket, addr) -> None:
    """Handle a single client connection."""
    print(f"[+] New connection from {addr}")

    try:
        # ask for a username once at the start
        sock.sendall(b"Enter username: ")
        name_data = sock.recv(1024)
        if not name_data:
            sock.close()
            return

        name = name_data.decode("utf-8").strip()
        if not name:
            name = f"user{len(clients) + 1}"

        clients[sock] = name
        print(f"[+] {name} joined")
        broadcast(f"*** {name} joined the chat ***\n", sender_sock=None)

        # main receive loop
        while True:
            data = sock.recv(1024)
            if not data:
                break  # client disconnected

            text = data.decode("utf-8").strip()
            if text == "":
                continue

            msg = f"{name}: {text}\n"
            print(msg, end="")
            broadcast(msg, sender_sock=sock)

    except ConnectionError:
        pass
    finally:
        # clean up when client disconnects
        username = clients.get(sock, "unknown")
        print(f"[-] {username} disconnected")
        clients.pop(sock, None)
        broadcast(f"*** {username} left the chat ***\n", sender_sock=None)
        sock.close()


def main() -> None:
    """Start the server and accept clients forever."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()

        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            client_sock, addr = server_sock.accept()
            t = threading.Thread(
                target=handle_client, args=(client_sock, addr), daemon=True
            )
            t.start()


if __name__ == "__main__":
    main()

