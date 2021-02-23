import socket
import tqdm
import os
import pyAesCrypt
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
# create the server socket

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

my_port = 1234          # this is the port for socket
my_host = socket.gethostname() # this is host name

     # Create a socket object

s.bind((my_host, my_port))
s.listen(5) #Waiting for connection by client
#########################################################

# accept connection if there is any
client_socket, address = s.accept()
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()

filename='a.txt'

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(1), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

print("The Encrypted File has been received")

# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
password = input("Enter the password for Decryption: ")

# decrypt
pyAesCrypt.decryptFile("File.txt", "Fileout.txt", password, bufferSize)
print("The file has been succesfully Decrypted!")

client_socket.close()
# close the socket
# s.close()