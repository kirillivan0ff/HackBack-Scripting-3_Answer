import socket
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

HOST = '10.10.144.222'  # The server's hostname or IP address
PORT = 4000        # The port used by the server
KEY = ''
IV = ''
FLAG1 = ''
FLAG2 = ''
CHECKSUM = ''

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST, PORT))
    print(f'Connecting to the server on {HOST}:{PORT}')
    s.send(b'hello')
    data = s.recv(1024).decode()
    print(data)

    s.send(b"ready to receive more information")
    data2 = s.recv(1024)

    KEY = data2.split()[0][4:]
    IV = data2.split()[1][3:]
    CHECKSUM = data2.split()[14]
    print(data2)
    print(f'Key received: {KEY}')
    print(f'IV recieved: {IV}')
    print(f'CHECKSUM received: {CHECKSUM}')

    while True:
        s.send(b"final")
        data3 = s.recv(1024)
        #print(f'Chipper text received: {data3}')

        s.send(b"final")
        data4 = s.recv(1024)
        #print(f'Chipper tag received: {data4}')

        cipher = AES.new(KEY, AES.MODE_GCM, nonce=IV)
        decrypted_data = cipher.decrypt(data3)
        if CHECKSUM == (hashlib.sha256(decrypted_data).digest()):
            print(f'The answer is: {decrypted_data}')
            break

        try:
            cipher.verify(data4)
        except ValueError as e:
            raise e
