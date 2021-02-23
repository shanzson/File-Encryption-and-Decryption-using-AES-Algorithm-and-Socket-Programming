import socket
import tqdm
import os
import pyAesCrypt

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "192.168.1.101"
# the port, let's use 5002
port = 5002
# the name of file we want to send, make sure it exists


# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
password = input("Enter the password for Encryption: ")
# encrypt
pyAesCrypt.encryptFile("File.txt", "File.txt.aes", password, bufferSize)
# decrypt
#pyAesCrypt.decryptFile("a.txt.aes", "aout.txt", password, bufferSize)
filename = "a.txt.aes"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
print("[+] Connected.")

# send the filename and filesize
s.send(f"{filename}".encode())

# start sending the file
progress = tqdm.tqdm(range(1), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in# busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
print('The file has been encrypted and sent')
# close the socket
# s.close()