from BitVector import *
from bitvectordemo import *

#implement a key scheduling algorithm to make keys 128 bits long
#source: https://en.wikipedia.org/wiki/AES_key_schedule
#if the key is short expand it to 128 bits
#if the key is long, truncate it to 128 bits
Rcon = [0x01, 0x00, 0x00, 0x00]
def key_schedule(key):
    # Create a BitVector from the input key
    key_bv = BitVector(hexstring=key)

    # Initialize the round keys list with the original key
    round_keys = [key_bv.deep_copy()]

    # Number of rounds in AES-128
    num_rounds = 10

    # Generate additional round keys
    for i in range(num_rounds):
        # Get the previous round key
        prev_key = round_keys[-1]

        # Perform the key schedule operations
        if i % 4 == 0:
            prev_key = g(prev_key, i // 4)

        # XOR with the previous round key and store the result
        round_key = prev_key ^ round_keys[-4]

        # Append the round key to the list
        round_keys.append(round_key)

    return round_keys

def g(word, round_constant):
    # Perform byte substitution
    word = sub_bytes(word)

    # Perform left circular shift
    word = word << 8

    # XOR with the round constant
    word = word ^ BitVector(intVal=Rcon[round_constant], size=8)

    return word

def sub_bytes(word):
    # Perform byte substitution using the S-box
    new_word = BitVector(size=0)
    for i in range(4):
        byte = word[i * 8:i * 8 + 8]
        row = byte[0:4].intValue()
        col = byte[4:].intValue()
        new_word += BitVector(intVal=Sbox[row * 16 + col], size=8)
    return new_word