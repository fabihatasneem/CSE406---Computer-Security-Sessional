from encryption import *
from decryption import *
import time

#take input string
input_string = input("Enter a plain text: ")
#take input key
input_key = input("Enter a key: ")

# chunk the string into 16 byte chunks
plain_text_chunks = chunk_string(input_string)
hex_key = get_hex_from_ascii(input_key)
# key = key_schedule(key)

#ENCRYPTION
start_time = time.perf_counter()
round_key_matrices = round_key_generate(hex_key)
ciphertext = encryption(plain_text_chunks, round_key_matrices)
encryption_time = time.perf_counter() - start_time
print("Encryption time: ", encryption_time, " seconds")
print("-------------------------------------------------------------------------------------------------------------------")

#DECRYPTION
start_time = time.perf_counter()
decrypted_output = decryption(ciphertext, round_key_matrices)
decryption_time = time.perf_counter() - start_time
print("Deciphered Text in ASCII:", decrypted_output)
print("Decryption time: ", decryption_time, " seconds")