import math
import string
import itertools

import rot_vige as rv

def ksa(key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(text):
    i = 0
    j = 0
    while True:
        i = ( i + 1 ) % 256
        j = ( j + text[i] ) % 256 
        text[i], text[j] = text[j], text[i]

        key = text[(text[i] + text[j]) % 256]
        yield key

def rc4(text, key):
    S = ksa(key)
    key = prga(S)
    result = ""
    for char in text:
        result += "%02X" % (ord(char) ^ next(key))
    return result

   
def entropy(text):
    freqdict = {}
    rv.update_freq(text, freqdict)
    probdict = rv.compute_prob(freqdict)
    result = 0

    for char in probdict.keys():
        result += probdict[char] * math.log(probdict[char],2)
    
    return -result

def force_decode_rc4(text, keylength):
    res_key = ""
    res_text = ""
    res_entropy = None

    for key in itertools.combinations_with_replacement(string.ascii_lowercase,keylength):
        key = ''.join(key)

print(rc4("dupa","huj"))
 
                
        
