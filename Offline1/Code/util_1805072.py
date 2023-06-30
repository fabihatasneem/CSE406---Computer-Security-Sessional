from BitVector import *
from bitvectordemo_1805072 import *

k = 16                  #128 bits = 16 bytes

def left_shift(my_list):
    return [my_list[1], my_list[2], my_list[3], my_list[0]]

#get the hexadecimal ascii value of each character from a string
def get_hex_from_ascii(string):
    hex_ascii = []
    for char in string:
        hex_ascii.append(hex(ord(char))[2:])
    return hex_ascii

#convert the hexadecimal ascii value of each entry from a list into ascii
def get_ascii_from_hex(hex_list):
    ascii_list = []
    for h in hex_list:
        ascii_list.append(chr(int(h, 16)))
    return ''.join(ascii_list)

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

#break the long hexadecimal padded string into 16 byte chunks
def chunk_hex_string(hex_str):
    #pad the hexadecimal number with 0s to make it 16 bytes long
    if(len(hex_str) % 32 != 0):
        hex_str = hex_str.zfill(len(hex_str) + (32 - len(hex_str) % 32))
    chunks = []
    while len(hex_str) > 0:
        if len(hex_str) >= 32:
            chunk = hex_str[:32]
        chunks.append(chunk)
        hex_str = hex_str[32:]
    return chunks

def break_hex_string(hex_string):
    hex_list = [hex_string[i:i+2] for i in range(0, len(hex_string)-1, 2)]
    return hex_list

def list_to_matrix(word_list):
    matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            matrix[j][i] = word_list[i * 4 + j]
    return matrix

# write a function for byte substitution for all entries of a list from the Sbox in bitvectordemo.py
def byte_substitution(word, inv):
    new_word = []
    # Perform byte substitution using the S-box
    for i in range(len(word)):
        if(len(word[i]) < 2):
            row = 0
            col = int(str(word[i][0]), 16)
        else:
            row = int(str(word[i][0]), 16)  # Convert the first character of byte to decimal
            col = int(str(word[i][1]), 16)  # Convert the second character of byte to decimal
        if(inv == False):
           new_word.append(hex(Sbox[row*16 + col])[2:])
        else:
            new_word.append(hex(InvSbox[row*16 + col])[2:])
    return new_word

# write a function for byte substitution for all entries of a matrix from the Sbox in bitvectordemo.py
def byte_substitution_matrix(matrix, inv):
    new_matrix = []
    for i in range(4):
        new_matrix.append(byte_substitution(matrix[i], inv))
    return new_matrix

def add_round_constant(round, word):
    constant = Rcon[round]
    result = []
    for i in range(len(word)):
        num = int(str(word[i]), 16)
        result.append(hex(num ^ constant[i]))
    return result

def XOR_hexa(num1, num2):
    num1 = int(num1, 16)
    num2 = int(num2, 16)
    return hex(num1 ^ num2)[2:]

def XOR_word(word1, word2):
    result = []
    for i in range(len(word2)):
        result.append(XOR_hexa(str(word1[i]), str(word2[i])))
    return result

def modify_last_word(round, word):
    word = left_shift(word)
    word = byte_substitution(word, False)
    word = add_round_constant(round, word)
    return word

def turn_into_column_matrix(word_list):
    matrix = []
    for i in range(4):
        column = []
        for j in range(4):
            column.append(word_list[j][i])
        matrix.append(column)
    return matrix

def XOR_matrix(matrix1, matrix2):
    result = [ [0]*4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = XOR_hexa(matrix1[i][j], matrix2[i][j])
    return result

#four rows are shifted cyclically to the left by offsets of 0,1,2, and 3
def shift_rows(matrix):
    result = [ [0]*4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = matrix[i][(j+i)%4]
    return result

#four rows are shifted cyclically to the right by offsets of 0,1,2, and 3
def inverse_shift_rows(matrix):
    result = [ [0]*4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = matrix[i][(j-i)%4]
    return result

#multiply two hexadecimal numbers
def multiply_hexa(num1, num2):
    num1 = int(str(num1), 16)
    num2 = int(str(num2), 16)
    return hex(num1 * num2)[2:]

#Mix Column multiplies fixed matrix Mixer from bitvectordemo.py against current State Matrix
def mix_columns(matrix, inv):
    result = [ [0]*4 for i in range(4)]
    if(inv == False):
        for i in range(4):
            for j in range(4):
                result[i][j] = XOR_hexa((BitVector(bitstring=Mixer[i][0]).gf_multiply_modular(BitVector(hexstring=matrix[0][j]), AES_modulus, 8)).get_bitvector_in_hex(),
                    XOR_hexa((BitVector(bitstring=Mixer[i][1]).gf_multiply_modular(BitVector(hexstring=matrix[1][j]),  AES_modulus, 8)).get_bitvector_in_hex(), 
                    XOR_hexa((BitVector(bitstring=Mixer[i][2]).gf_multiply_modular(BitVector(hexstring=matrix[2][j]),  AES_modulus, 8)).get_bitvector_in_hex(),
                    (BitVector(bitstring=Mixer[i][3]).gf_multiply_modular(BitVector(hexstring=matrix[3][j]),  AES_modulus, 8)).get_bitvector_in_hex())))
    else:
        for i in range(4):
            for j in range(4):
                result[i][j] = XOR_hexa((BitVector(bitstring=InvMixer[i][0]).gf_multiply_modular(BitVector(hexstring=matrix[0][j]), AES_modulus, 8)).get_bitvector_in_hex(),
                    XOR_hexa((BitVector(bitstring=InvMixer[i][1]).gf_multiply_modular(BitVector(hexstring=matrix[1][j]),  AES_modulus, 8)).get_bitvector_in_hex(), 
                    XOR_hexa((BitVector(bitstring=InvMixer[i][2]).gf_multiply_modular(BitVector(hexstring=matrix[2][j]),  AES_modulus, 8)).get_bitvector_in_hex(),
                    (BitVector(bitstring=InvMixer[i][3]).gf_multiply_modular(BitVector(hexstring=matrix[3][j]),  AES_modulus, 8)).get_bitvector_in_hex())))
    return result

# convert the column matrix into a list of words
def convert_matrix_to_words(matrix):
    word_list = []
    for i in range(4):
        for j in range(4):
            if(len(matrix[j][i]) < 2):
                word_list.append('0' + matrix[j][i])
            else:
                word_list.append(matrix[j][i])
    return word_list

#if key is less than 128 bits or 16 bytes, expand it to 16 bytes using padding
def key_expand(key):
    if(len(key) < 32):
        key = key.zfill(32)
    # else if key is greater than 128 bits or 16 bytes, truncate it to 16 bytes
    elif(len(key) > 32):
        key = key[:32]
    return key

# print a list of multiple 4x4 matrices
def print_matrix(matrix_list):
    for i in range(len(matrix_list)):
        print("Round Key Matrix ", i, ":")
        # print the matrix in a nice 4x4 format
        for j in range(4):
            print("| ", end=' ')
            for k in range(4):
                print(matrix_list[i][j][k], end=' ')
            print("|")
        print()