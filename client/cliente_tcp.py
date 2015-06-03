import socket
import sys
import json

BUFSIZE = 8192

def str_to_tuple(string, *converters):
    return tuple( c(v) for c,v in zip(converters, string.split()) )

# Modo de Uso
if len(sys.argv) != 1:
    print ("Modo de Uso:")
    print ("python cliente_tcp.py")

print ("Entre com quantas tuplas de servidor/porta quanto quiser (SERVIDOR PORTA):")
print ("Para continuar digite 0")

servers = []

tmp = str_to_tuple(raw_input(), str, int)
i = 0

while tmp[0] != '0':
    servers.append(tmp)
    tmp = str_to_tuple(raw_input(), str, int)
    i += 1


# Create List of TCP/IP sockets
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM) for s in servers ]

print( "Connecting to servers:")
# Connect to servers
for sck, srv  in zip(socks, servers):
    print (srv)
    sck.connect( srv )

try:

    while True:

        sys.stdout.write ("Name of the file to be synced:")
        filename = raw_input()    

        try:
            data = open(filename, "r").read()
            tmp = raw_input ("Do you want to edit the file? (y/n):")
            if tmp == 'y':
           
                f = open(filename,"w")
                data = raw_input("Enter the new content:")
                f.write(data)
                f.close()

        except IOError as e:

            print ("File does not Exist!")
            tmp = raw_input ("Do you want to create a file with this name (y/n):")

            if tmp == 'y':
                f = open(filename,"w")
                data = raw_input("Enter the file content:")
                f.write(data)
                f.close()    

        # Creating message with field 'file' and 'data'
        message = json.dumps( { 'filename':filename, 'data':data } )

        print("Sending\n %s" % (data) )

        message = message.encode()

        for s in socks:
            s.send(message);

        # TODO: If the received  message is bigger than BUFSIZE the socket send 
        # function will automatically split it into multiple messages. But we 
        # are not getting every message received. The code on the first email I 
        # sent does this but for some reason it stopped working. It might be 
        # because now messages are using JSON         

        for s in socks:
            data = s.recv(BUFSIZE)

            print ("received from:", s.getsockname() )
            print (data.decode())

        print("")
finally:
    for s in socks:
        s.close()
