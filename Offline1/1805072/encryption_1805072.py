from util_1805072 import *

k = 128
if(k == 128):
    num_of_rounds = 10
elif(k == 192):
    num_of_rounds = 12
elif(k == 256):
    num_of_rounds = 14

def encryption(plain_text_chunks, round_key_matrices):
    ciphertext_hex = ""
    ciphertext_ascii = ""
    for i in range(len(plain_text_chunks)):
        # Make the first State Matrix from the text
        state_matrix = []
        for j in range(0, len(plain_text_chunks[i])-3, 4):
            state_matrix.append(get_hex_from_ascii(plain_text_chunks[i][j:j + 4]))
        state_matrix = turn_into_column_matrix(state_matrix)
        state_matrix = XOR_matrix(state_matrix, round_key_matrices[0])

        for j in range(num_of_rounds):
            #substitute bytes of each entry of the state matrix
            state_matrix = byte_substitution_matrix(state_matrix, False)
            #shift rows of the state matrix
            state_matrix = shift_rows(state_matrix)
            #mix columns of the state matrix if round is not last round
            if j != 9:
                state_matrix = mix_columns(state_matrix, False)
            #XOR with this round's key from the round_key_list
            state_matrix = XOR_matrix(state_matrix, round_key_matrices[j+1])
        
        cipher_hex_chunk = convert_matrix_to_words(state_matrix)
        cipher_hex_chunk = ''.join(cipher_hex_chunk)
        ciphertext_hex += cipher_hex_chunk   # add the new chunk to the ciphertext
        
        cipher_asii_chunk = get_ascii_from_hex(cipher_hex_chunk)
        ciphertext_ascii += cipher_asii_chunk
    print("Ciphertext in HEX: ", ciphertext_hex)
    print("Ciphertext in ASCII: ", ciphertext_ascii)
    return ciphertext_hex

def round_key_generate(hex_key):
    # each 4 elements in the hex_key list is a word
    round_key_matrices = []
    round_key = []
    for i in range(0, len(hex_key)-3, 4):
        round_key.append(hex_key[i:i + 4])
    round0_key = turn_into_column_matrix(round_key)
    round_key_matrices.append(round0_key)

    # XOR with the previous round key and store the result
    for i in range(num_of_rounds):
        curr = []
        g_w_3 = modify_last_word(i+1, round_key[3])
        curr.append(XOR_word(g_w_3, round_key[0]))
        curr.append(XOR_word(curr[0], round_key[1]))
        curr.append(XOR_word(curr[1], round_key[2]))
        curr.append(XOR_word(curr[2], round_key[3]))
        round_key = curr
        key_matrix = turn_into_column_matrix(curr)
        round_key_matrices.append(key_matrix)
    return round_key_matrices