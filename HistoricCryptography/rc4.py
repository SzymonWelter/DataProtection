import math
import string
import itertools
import binascii
import os

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
        result += "%02X" % (char ^ next(key))
    return result

def get_entropy(text):
    freqdict = {}
    rv.update_freq(text, freqdict)
    probdict = rv.compute_prob(freqdict)
    result = 0

    for char in probdict.keys():
        result += probdict[char] * math.log(probdict[char],2)
    
    return -result

class AttackResult:
    def __init__(self, text, key, entropy):
        self.text = text
        self.key = key
        self.entropy = entropy

def force_decode_rc4(text, keylength):

    result = AttackResult("","",None)
    i = 0
    for key in itertools.product(string.ascii_lowercase,repeat=keylength):
        key = ''.join(key)
        decoded = rc4(text, key)
        entropy = get_entropy(decoded)
        i += 1
        print("{0:.2f}%".format(100*i/(26**3)), end="\r")
        if result.entropy is None or entropy < result.entropy:
            result = AttackResult(decoded,key,entropy)
    print("\n"+result.key)

    return result

with open("C:/Users/Z6SZW/Private/DataProtection/HistoricCryptography/crypto.rc4", 'rb') as file:
    result = ""
    text = file.read(1024)
    result = force_decode_rc4(text,3).text
    print(bytearray.fromhex(result).decode())

 
                
        
