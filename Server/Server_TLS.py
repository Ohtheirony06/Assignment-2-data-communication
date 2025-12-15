import socket
import threading
import time
import ssl

HOST = ''
PORT = 3008
Client_Sockets = []
Flags = {"stop": False, "Binded": False}

def Check_Even(data_Input):
    try:
        Data = int(data_Input)
        if (Data % 2) == 0:
            #print("Even")
            return "Even"
        else:
            #print("Odd")
            return "Odd"
    except Exception as e:
        return "Invalid input"

def Listener(sock):
    attempts = 0
    while attempts < 3:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            print("Bind successful!")
            Flags["Binded"] = True
            break
        except OSError:
            attempts += 1
            print("OS may be holding so waiting for 5 seconds.")
            time.sleep(5)
    
    sock.listen(5)
    sock.settimeout(1.0)  # periodic unblock
    while not Flags["stop"]:
        try: #Dealing with the listener socket.
            conn, addr = sock.accept()
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="/home/user1server/Desktop/Part_2_TLS/CRT/server.crt", keyfile="/home/user1server/Desktop/Part_2_TLS/CRT/server.key")
            connstream = context.wrap_socket(conn, server_side=True)
            connstream.settimeout(1.0)
            print('Connected by', addr)
            Client_Sockets.append(connstream)
            while not Flags["stop"]:
                try: #Dealing with the connection socket.
                    data_bytes = connstream.recv(1024)
                    if not data_bytes:  # client disconnected
                        break
                    else:
                        connstream.send(Check_Even(data_bytes).encode("utf-8"))
                except socket.timeout:
                    continue
                except ValueError:
                    Error_Message = "Invalid integer received"
                    Error_Message = Error_Message.encode("utf-8")
                    connstream.sendto(Error_Message, addr)
                    print("Invalid integer received")
                except OSError:
                    break  # socket closed from main thread
        except socket.timeout:
            continue
        except OSError:
            break  # listener socket closed

def Resource_Cleaner(sock):
    Flags["stop"] = True  # signal threads to exit
    # Close all client sockets
    for conn in Client_Sockets:
        if conn.fileno() != -1:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conn.close()
    # Close listener socket
    if sock.fileno() != -1:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()

# Main program
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Listener_A = threading.Thread(target=Listener, args=(sock,))
Listener_A.start()

while True:
    if Flags["Binded"]:
        print(sock.getsockname()[1])
        Answer = input("Would you like to close the socket? 1=Yes 2=No\n")
        if int(Answer) == 1:
            print("Shutting down!")
            Resource_Cleaner(sock)
            Listener_A.join()
            print("Server closed cleanly")
            break
