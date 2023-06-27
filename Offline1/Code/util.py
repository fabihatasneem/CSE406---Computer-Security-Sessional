from BitVector import *
from bitvectordemo import *

def left_shift(my_list):
    return [my_list[1], my_list[2], my_list[3], my_list[0]]

#get the hexadecimal ascii value of each character from a string
def get_hex_ascii(string):
    hex_ascii = []
    for char in string:
        hex_ascii.append(hex(ord(char))[2:])
    return hex_ascii

#break the string into 16 byte chunks
def chunk_string(string):
    chunks = []
    while len(string) > 0:
        if len(string) >= 16:
            chunk = string[:16]
        else:
            chunk = string.ljust(16, ' ')  # Padding with spaces if the last chunk is less than 16 characters
        chunks.append(chunk)
        string = string[16:]
    return chunks

# write a function for byte substitution for all entries of a list from the Sbox in bitvectordemo.py
def byte_substitution(word):
    new_word = []
    # Perform byte substitution using the S-box
    for i in range(len(word)):
        print("word[i]: ",word[i])
        row = int(str(word[i][0]), 16)  # Convert the first character of byte to decimal
        if(word[i][1] == None):
            col = 0
        else:
            col = int(str(word[i][1]), 16)  # Convert the second character of byte to decimal
        new_word.append(hex(Sbox[row*16 + col])[2:])
    return new_word

def add_round_constant(word):
    constant = [1, 00, 00, 00]
    return XOR(word, constant)

def XOR(word1, word2):
    print("word1: ",word1," , word2: ", word2)
    result = []
    for i in range(len(word2)):
        num1 = int(str(word1[i]), 16)
        num2 = int(str(word2[i]), 16)
        result.append(hex(num1 ^ num2)[2:])
    return result

def modify_last_word(word):
    word = left_shift(word)
    print(word)
    word = byte_substitution(word)
    print(word)
    word = add_round_constant(word)
    print(word)
    return word