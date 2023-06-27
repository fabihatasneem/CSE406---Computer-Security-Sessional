from BitVector import *
from bitvectordemo import *
from keySchedulingAlgo import *
from util import *

#take input string
input_string = input("Enter a plain text: ")
input_key = input("Enter a key: ")
hex_key = get_hex_ascii(input_key)
# key = key_schedule(key)

# each 4 elements in the hex_key list is a word
word_list = []
for i in range(0, len(hex_key)-3, 4):
    word_list.append(hex_key[i:i + 4])

# XOR with the previous round key and store the result
for i in range(10):
    print("Round ", i+1)
    curr = []
    g_word_3 = modify_last_word(word_list[3])
    print("g_word_3 : ",g_word_3)
    curr.append(XOR(g_word_3, word_list[0]))
    curr.append(XOR(curr[0], word_list[1]))
    curr.append(XOR(curr[1], word_list[2]))
    curr.append(XOR(curr[2], word_list[3]))
    word_list = curr
    print(word_list)
    print("----------------------------------------------------------------------------------")