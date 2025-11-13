# COSC 439 – very first client draft
# Connects to the chat server, sends user input,
# and prints anything it receives.

import socket
import threading
import sys

SERVER_HOST = "127.0.0.1"  # change to server machine IP when testing over network
SERVER_PORT = 5000


def listen_for_messages(sock: socket.socket) -> None:
    """Background thread: receives data from server and prints it."""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("\n[Disconnected from server]")
                break
            print(data.decode("utf-8"), end="")
    except ConnectionError:
        print("\n[Connection error]")
    finally:
        sock.close()
        # exit whole program when server closes
        sys.exit(0)


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        print(f"[CLIENT] Connected to {SERVER_HOST}:{SERVER_PORT}")

        # start listener thread
        t = threading.Thread(target=listen_for_messages, args=(sock,), daemon=True)
        t.start()

        try:
            # main loop: read from keyboard and send to server
            while True:
                user_input = input()
                # add newline so server prints nicely
                message = user_input + "\n"
                sock.sendall(message.encode("utf-8"))
        except (KeyboardInterrupt, EOFError):
            print("\n[CLIENT] Closing connection, bye.")
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


if __name__ == "__main__":
    main()

