#TLS client

#Client's stored data

username = "pakeclient"
password = b'client_opaque_pass'


#Open connection to server
import socket
port = 24601
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', port))


    #Request certificate and perform exchange



    #Exchange data (an actual protocol would be secured; this just uses a localhost connection in a prearranged order of moves)
    #TODO
    msg = s.recv(1024)
    while msg:
        print('Received:' + msg.decode())
        msg = s.recv(1024)
