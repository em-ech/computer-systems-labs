import socket
import sys
import signal
import threading


PORT = 4321
ADDRESS = '127.0.0.1'

#for the thread to know when to exit
is_it_on = True
c_socket = None


def spy_on_server():
    #spy_on_server listens to the server to get and print messages, essentially a spy
    global is_it_on
    while is_it_on:
        try:
            #checks, and if yes then moves through the loop
            msg = c_socket.recv(1024)
            if not msg:
                print("\nDisconnected from server.")
                break

            #translates bytes to string
            print(msg.decode('ascii').strip())
        except OSError:
            break
    is_it_on = False
    sys.exit(0)


def bye_client(signum, frame):
    #by_client is used for when the user preses ctrl+c
    global is_it_on
    is_it_on = False
    #
    print("\n^C Disconnected from server.")

    #closes connection and leaves
    if c_socket:
        try:
            c_socket.close()
        except OSError:
            pass
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('You must pass the client name as a command line argument.')
    else:
        client_name = sys.argv[1]

    signal.signal(signal.SIGINT, bye_client)

    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c_socket.connect((ADDRESS, PORT))
    except OSError:
        sys.exit("Could not connect to the server.")

    print('Connected to server', ADDRESS, 'on port', PORT)

    try:
        c_socket.sendall(client_name.encode('ascii'))
    except OSError:
        sys.exit("Error sending name to server.")

    threading.Thread(target=spy_on_server, daemon=True).start()

    while is_it_on:
        try:
            msg = input()
            if msg.strip():
                c_socket.sendall(msg.encode('ascii'))
        except (EOFError, OSError):
            break

    if c_socket:
        c_socket.close()