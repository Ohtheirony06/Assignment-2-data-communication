import socket
import ssl
HOST = '192.168.88.131' # Server IP
PORT = 3008 # Server port
try:
    context = ssl.create_default_context() #Will use the root CA certificates stored on this machine. I'm not specifying-
    #-A specific directory in my code for increased security and reduced custom configurations in the future.
    with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),server_hostname = "kali-server") as s:
        #^ Above I'm adding to the the TLS context by creating a socket and expecting the hostname "kali-server"
        s.connect((HOST, PORT))
        while True: #Added a loop so you can constantly type new inputs.
            Data = input("Insert number: ")
            if Data == "Stop": #If you want to stop sending inputs.
                break
            Data = Data.encode("utf-8") #This and below is the same
            s.sendall(Data)
            data = s.recv(1024)
            print('Received:', str(data))
        s.shutdown(socket.SHUT_RDWR) 
except OSError: #Only added this error as when trying out different things it was the only one I kept getting.
    pass
s.close()
