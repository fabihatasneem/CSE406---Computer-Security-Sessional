from util_1805072 import *
from encryption_1805072 import *

k = 128
if(k == 128):
    num_of_rounds = 10
elif(k == 192):
    num_of_rounds = 12
elif(k == 256):
    num_of_rounds = 14

def decryption(ciphertext, round_key_matrices):
    #if ciphertext is longer than 128 bits, break it into chunks of 128 bits
    ciphertext = chunk_hex_string(ciphertext)
    output = []
    for i in range(len(ciphertext)):
        ciphertext[i] = break_hex_string(ciphertext[i])
        #add round key from the last round with the ciphertext matrix
        state_matrix = list_to_matrix(ciphertext[i])
        state_matrix = XOR_matrix(state_matrix, round_key_matrices[num_of_rounds])
        for i in reversed(range(num_of_rounds)):
            #inverse shift rows
            state_matrix = inverse_shift_rows(state_matrix)
            #inverse byte substitution
            state_matrix = byte_substitution_matrix(state_matrix, True)
            #add round key of this round with the state matrix
            state_matrix = XOR_matrix(state_matrix, round_key_matrices[i])
            #inverse mix columns if round is not 0
            if i != 0:
                state_matrix = mix_columns(state_matrix, True)
        output = output + convert_matrix_to_words(state_matrix)
    deciphered_text = get_ascii_from_hex(output)
    return deciphered_text