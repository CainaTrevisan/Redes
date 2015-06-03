import socket
import sys
import json
import threading
import thread

# Modo de Uso
if len(sys.argv) != 3:
    print ("Modo de Uso:")
    print ("<servidor> <porta>")
    sys.exit(1)

IP = sys.argv[1]
PORT = int( sys.argv[2] )
BUFSIZE = 8192
BACKLOG = 5 # Maximum, probably

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
sock.bind( (IP, PORT) )

# Listen incoming connection
sock.listen(BACKLOG)

lock = threading.Lock()
    
def listen_socket(connection, lock):
    try:
        while True:
            data = connection.recv(BUFSIZE)
            if data: 
                data = json.loads(data.decode())
                
                FILE = data['filename']
                message = data['data']   

                print("File: %s\nMessage:" % (FILE) )
                print(message)

                lock.acquire()
                f = open( FILE, "w+")
                print ( f.read() )
                f.write(message)
                f.seek(0)
                new_data = f.read().encode()
                f.close()     
                lock.release()    
     
                connection.send(new_data)
    finally:
        connection.close()

while True:
    connection, client_address = sock.accept()    
    thread.start_new_thread(listen_socket, (connection, lock) ) 
