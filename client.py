import socket


TCP_IP= '192.168.0.106'  # The server's hostname or IP address
TCP_PORT = 5005
BUFFER_SIZE = 1024
st= 'hello'  #message to be sent
st=st.encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(st)
#data = s.recv(BUFFER_SIZE)
s.close()
st=st.decode()

print ("data sent:",st)