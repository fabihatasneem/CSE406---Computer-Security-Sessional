from encryption import *
from decryption import *

#take input string
input_string = input("Enter a plain text: ")
# chunk the string into 16 byte chunks
plain_text_chunks = chunk_string(input_string)

#take input key
input_key = input("Enter a key: ")
hex_key = get_hex_ascii(input_key)
# key = key_schedule(key)

print("Desired Ciphertext: ", encryption(plain_text_chunks, hex_key))

