import math
from rc4 import get_entropy, decode_rc4
import rot_vige as rv
from Crypto.Cipher import ARC4,DES,AES
from Crypto.Random import get_random_bytes
import hashlib


def get_simplified_entropy(text, alphabet_length):
    return len(text) * math.log(alphabet_length, 2)
    
def get_alphabet_length(text):
    freq = {}
    rv.update_freq(text,freq)
    return len(freq.keys())

def compare_entropy(text, atext):
    print(['Entropy of text 1:', get_entropy(text)])
    print(['Simplified entropy of text 1:', get_simplified_entropy(text, get_alphabet_length(text))])
    print(['Entropy of text 2', get_entropy(atext)])
    print(['Simplified entropy of text 2:', get_simplified_entropy(atext, get_alphabet_length(atext))])

def aes_cbc(path, key):
    key = key.encode(encoding='UTF-8')
    byte_key = hashlib.sha256(key).digest()
    iv = get_random_bytes(16)
    aes = AES.new(byte_key, AES.MODE_CBC, iv)
    chunk_size = 16
    result = []
    with open(path,'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                 chunk += bytes(' ' * (16 - len(chunk) % 16), encoding='UTF-8')
            result = aes.encrypt(chunk)
    with open(path+'enc','wb') as file:
        file.write(result)

def generate_key(password, key_size):
    m = hashlib.sha256()
    while True:
        if key_size > m.digest_size:
            m.update(password)
        else:
            break
    return m.digest()[:key_size]



text = ""
cipher = ""
with open("/home/welters/Downloads/crypto.rc4", 'rb') as file:
    cipher = file.read()
    #text = ARC4.new("def").decrypt(cipher)
    text = bytearray.fromhex(decode_rc4(cipher, "def"))
    compare_entropy(text, cipher.decode("Latin-1"))

print("****************")

with open("/home/welters/Downloads/text", 'rb') as file:
    key = "sTronKey"
    text = file.read()
    iv = get_random_bytes(8)
    ecb = DES.new(key, DES.MODE_ECB)
    ecb = ecb.encrypt(text)
    cbc = DES.new(key, DES.MODE_CBC,iv)
    cbc = cbc.encrypt(text)
    compare_entropy(ecb, cbc)

path = "/home/welters/Downloads/text"
aes_cbc(path,"testowytextabcdef")
print(generate_key('lekarzegonienawidza',32))
