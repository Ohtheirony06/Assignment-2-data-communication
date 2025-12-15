import socket
try:
    import ssl
except ImportError:
    print("Error importing ssl")
    exit()
else:
    print("Working")
HOST = '192.168.88.131' # Server IP
PORT = 3008 # Server port
context = ssl.create_default_context() #Use the default context.
conn = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),server_hostname = "kali-server") 
#^Create the TCP socket and expect the hostname "kali-server" in the TLS context.
conn.connect((HOST, PORT)) # Connect to server.
cert = conn.getpeercert() # Get authenticated certificate
print(f"CERT: {cert}") # Print certificate.
Data_To_Send = b"2" #Data I want to send.
conn.sendall(Data_To_Send) #Attempt to send the data which in this case is 2.
data_bytes = conn.recv(1024) #Wait to recieve data.
print(data_bytes) #Print received data.
