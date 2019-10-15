import math
from rc4 import get_entropy, decode_rc4
import rot_vige as rv
import Crypto.Cipher

def get_simplified_entropy(text, alphabet_length):
    return len(text) * math.log(alphabet_length, 2)
    
def get_alphabet_length(text):
    freq = {}
    rv.update_freq(text,freq)
    return len(freq.keys())

def compare_entropy(text, cipher):
    print(['Entropy of text:', get_entropy(text)])
    print(['Simplified entropy of text:', get_simplified_entropy(text, get_alphabet_length(text))])
    print(['Entropy of cipher', get_entropy(cipher)])
    print(['Simplified entropy of cipher:', get_simplified_entropy(cipher, get_alphabet_length(cipher))])

text = ""
cipher = ""
with open("C:/Users/user/Downloads/crypto.rc4", 'rb') as file:
    cipher = file.read()
    text = bytearray.fromhex(decode_rc4(cipher, "def"))
    compare_entropy(text, cipher.decode("Latin-1"))
