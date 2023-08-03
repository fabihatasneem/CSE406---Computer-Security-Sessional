import socket
import time
from diffie_hellman_1805072 import *
from encryption_1805072 import *

host = socket.gethostname()
port = 1234
chunk_size = 1024
k = 128
message = ""
C1 = 0
filename = "message_sent.txt"

s = socket.socket()
s.connect((host, port))
print('Connected to Bob')

p = generate_prime_number(k)
g = generate_primitive_root(p, 2, p-2)

# generate random prime number a of given bit length k/2
a = generate_prime_number(int(k/2))

# Compute A = g^a (mod p)
A = binary_exponentiation(g, a, p)
# Send p,g,A to Bob
data = ("KEY " + str(p) + " " + str(g) + " " + str(A)).encode()
s.send(data)

while True:
    # Receive from Bob
    message = s.recv(chunk_size).decode()
    print('Data received from Bob')

    # Split the message into a list of substrings
    lines = message.split(' ')

    if(lines[0] == "KEY"):
        print('KEY received from Bob')
        # Compute C = B^a (mod p) = A^b (mod p)
        B = int(lines[1])
        C2 = int(lines[2])
        C1 = binary_exponentiation(B, a, p)
        if C1 == C2:
            print("Private Key Shared :", C1)
            #Inform Bob that Alice is ready
            data = ("READY").encode()
            s.send(data)
            print('READY sent to Bob')
        else:
            print("Private Key not Shared")
            data = ("NOTREADY").encode()
            s.send(data)
    elif(lines[0] == "READY"):
        print('READY received from Bob')
        with open(filename, 'r') as f:
            input_string = f.read()

        # chunk the string into 16 byte chunks
        plain_text_chunks = chunk_string(input_string)
        hex_key = get_hex_from_ascii(str(C1))
        hex_key = key_expand(hex_key)

        #ENCRYPTION
        start_time = time.perf_counter()
        round_key_matrices = round_key_generate(hex_key)
        # print_matrix(round_key_matrices)
        ciphertext = encryption(plain_text_chunks, round_key_matrices)
        encryption_time = time.perf_counter() - start_time
        print("Encryption time: ", encryption_time, " seconds")
        print("-------------------------------------------------------------------------------------------------------------------")

        # Send ciphertext
        data = ("CIPHERTEXT " + ciphertext).encode()
        s.send(data)
        print('CIPHERTEXT sent to Bob')
        break
