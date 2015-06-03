import socket
import sys
import json

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

while True:
    connection, client_address = sock.accept()    

    try:
        while True:
            data = connection.recv(BUFSIZE)
            if data: 
                data = json.loads(data.decode())
                
                FILE = data['filename']
                message = data['data']   

                print("File: %s\nMessage:" % (FILE) )
                print(message)

                f = open( FILE, "w+")
                print ( f.read() )
                f.write(message)
                f.seek(0)
                new_data = f.read().encode()
                f.close()           
     
                connection.send(new_data)
    finally:
        connection.close()
