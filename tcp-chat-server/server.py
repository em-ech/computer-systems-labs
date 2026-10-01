import socket
import signal
import sys
import threading

PORT = 4321
ADDRESS = ''
MAX_CONNECTIONS = 10
HISTORY_FILENAME = 'conversation_backup.txt'

client_list = []
users_lock = threading.Lock()
convo = []
history_lock = threading.Lock()
s_socket = None
listening = True


def handle_client(c_socket, address):
    #handle_client creates a thread per client
    try:
        msg = c_socket.recv(1024)
        if not msg:
            c_socket.close()
            return

        #converting bytes to string
        client_name = msg.decode('ascii').strip()
        
        user_info = {"sock": c_socket, "name": client_name, "addr": address}

        #adding to the client list
        users_lock.acquire()
        names = [u["name"] for u in client_list]
        client_list.append(user_info)
        users_lock.release()

        #print's client connected and it's address
        print(f'Client with address {address} connected')

        #checks if the length of the client list is 1, ie if it's the first client
        if not names:
            line = f'You joined the chat as "{client_name}". You are the first to join.'
            c_socket.sendall((line + '\n').encode('ascii'))
        else:
            #if not, make a list of their names
            others = ", ".join(names)
            line = f'You joined the chat as "{client_name}". People in the chat room: {others}.'
            c_socket.sendall((line + '\n').encode('ascii'))
            
        #message to the other clients that the newbie joined (and log to history)
        #MOVED OUTSIDE ELSE: Now runs for the first user too so history is complete
        send_message(f'{client_name} joined the chat!', c_socket)

        #while the server is on, keep getting messages
        while listening:
            try:
                data = c_socket.recv(1024)
                if not data:
                    break
                
                #translate bytes to string
                decoded_message = data.decode('ascii').strip()
                
                if decoded_message:
                    #the pretty version of the message
                    msg_final = f"{client_name}: {decoded_message}"
                    print(msg_final)
                    
                    #send it to the other clients
                    send_message(msg_final, c_socket)
            except OSError:
                break

    finally:
        #after the while loop, so the client's leaving, and adjust the list accordingly
        users_lock.acquire()
        if user_info in client_list:
            client_list.remove(user_info)
        users_lock.release()

        #bye message
        print(f'Client "{client_name}" with address {address} disconnected.')
        bye_bye = client_name + " left the chat!"
        send_message(bye_bye, c_socket)
        
        try:
            c_socket.close()
        except OSError:
            pass


def send_message(msg_final, sender_sock):
    #send_message sends a message to everyone besides the one sending it
    
    #creates a chat history to save messages
    history_lock.acquire()
    convo.append(msg_final)
    history_lock.release()

    users_lock.acquire()
    for user in client_list:
        sock = user["sock"]
        if sock != sender_sock:
            #checks if it's not the sender, then send to everyone else
            try:
                sock.sendall((msg_final + '\n').encode('ascii'))
            except OSError:
                pass
    users_lock.release()


def save_me(signum, frame):
    #save_me moves the conversations into a backup file
    try:
        history_lock.acquire()
        #join with newlines to ensure clean formatting in file
        content = '\n'.join(convo)
        history_lock.release()
        
        with open(HISTORY_FILENAME, "w", encoding="utf-8") as backup:
            backup.write(content + "\n")
        
        print(f'[SERVER] Backup saved to {HISTORY_FILENAME}')
    except OSError:
        pass
    
    #Only reset alarm if this is a real signal (not a manual call on exit)
    if signum is not None:
        signal.alarm(30)


def bye_server(signum, frame):
    #bye_server is used when the user uses ctr+c, shuts the server down and closes sockets
    global listening
    #flip to false so the client threads end their loops to stop listening
    listening = False

    print("\n^C Server disconnected.")
    
    #Last minute save to ensure no data is lost on exit
    save_me(None, None)
    
    users_lock.acquire()
    for user in client_list:
        try:
            user["sock"].close()
        except OSError:
            pass
    client_list.clear()
    users_lock.release()

    if s_socket:
        s_socket.close()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, bye_server)
    signal.signal(signal.SIGALRM, save_me)
    signal.alarm(30)

    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #critical for Mac to avoid 'Address already in use' errors
    s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_socket.bind((ADDRESS, PORT))
    s_socket.listen(MAX_CONNECTIONS)

    print('Server', socket.gethostname(), 'started on port', PORT)

    #keeps accepting clients foreverr
    while True:
        try:
            c_socket, address = s_socket.accept()
            threading.Thread(target=handle_client, args=(c_socket, address), daemon=True).start()
        except OSError:
            break