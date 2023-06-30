import socket
import time
from decryption_1805072 import *
from diffie_hellman_1805072 import *

host = socket.gethostname()
port = 1234
chunk_size = 1024
k = 128
p = 0
g = 0
b = 0
A = 0
B = 0
C2 = 0
message = ""

s = socket.socket()
s.bind((host, port))
s.listen(2)
print('Waiting for connections...')

conn, addr = s.accept()
print(f'Connected to Alice by {addr}')

while True:
    # Receive file from Alice first
    message = conn.recv(chunk_size).decode()
    print('Data received from Alice')

    # Split the message into a list of substrings
    lines = message.split(' ')

    if(lines[0] == "KEY"):
        print('KEY File received from Alice')
        message = lines[0]
        p = int(lines[1])
        g = int(lines[2])
        A = int(lines[3])
        b = generate_prime_number(int(k/2))
        B = binary_exponentiation(g, b, p)
        C2 = binary_exponentiation(A, b, p)
        
        # Send key to Alice
        data = ("KEY " + str(B) + " " + str(C2)).encode()
        conn.send(data)
        print('KEY File sent to Alice')
    elif(lines[0] == "READY"):
        print('READY File received from Alice')
        print("Private Key Shared :", C2)

        # Inform Alice that Bob is ready
        data = ("READY").encode()
        conn.send(data)
        print('READY File sent to Alice')
    elif(lines[0] == "NOTREADY"):
        b = generate_prime_number(int(k/2))
        B = binary_exponentiation(g, b, p)
        C2 = binary_exponentiation(A, b, p)
        
        # Send key to Alice
        data = ("KEY " + str(B) + " " + str(C2)).encode()
        conn.send(data)
        print('KEY File again sent to Alice')
    elif(lines[0] == "CIPHERTEXT"):
        print('CIPHERTEXT File received from Alice')
        ciphertext = lines[1]
        hex_key = get_hex_from_ascii(str(C2))
        hex_key = key_expand(hex_key)
        round_key_matrices = round_key_generate(hex_key)
        # print_matrix(round_key_matrices)

        #DECRYPTION
        start_time = time.perf_counter()
        decrypted_output = decryption(ciphertext, round_key_matrices)
        decryption_time = time.perf_counter() - start_time
        print("Deciphered Text in ASCII:", decrypted_output)
        print("Decryption time: ", decryption_time, " seconds")
        break