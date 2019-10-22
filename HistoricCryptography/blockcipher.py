import math
from rc4 import get_entropy, decode_rc4
import rot_vige as rv
from Crypto.Cipher import ARC4,DES,AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import hashlib
import itertools
import string
from PIL import Image


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

def convert_to_RGB(data):
    pixels = []
    counter = 2

    for i in range(len(data)-1):
        if counter == 2:
            r = int(data[i])
            g = int(data[i+1])
            b = int(data[i+2])

            pixels.append((r,g,b))
            counter = 0
        else:
            counter += 1
    return pixels



text = ""
cipher = ""
with open("/home/welters/Downloads/crypto.rc4", 'rb') as file:
    cipher = file.read()
    #text = ARC4.new("def").decrypt(cipher)
    text = bytearray.fromhex(decode_rc4(cipher, "def"))
    compare_entropy(text, cipher.decode("Latin-1"))

print("****************")

#with open("/home/welters/Downloads/demo24.bmp", 'rb') as file:
#    key = "sTronKey"
#    text = file.read()
#    iv = get_random_bytes(8)
#    for i in range(8 - (len(text) % 8)):
#        text += bytes([0])
#    ecb = DES.new(key, DES.MODE_ECB)
#    ecb = ecb.encrypt(text)
#    cbc = DES.new(key, DES.MODE_CBC,iv)
#    cbc = cbc.encrypt(text)
#    compare_entropy(ecb, cbc)

class AttackResult:
    def __init__(self, text, key, entropy):
        self.text = text
        self.key = key
        self.entropy = entropy

def force_decode(text, keylength):
    result = AttackResult("","",None)
    i = 0
    for key in itertools.product(string.ascii_lowercase,repeat=keylength):
        key = 'fe'+ ''.join(key)
        print(key)
        key = PBKDF2(bytes(key,'ascii'), b'abc')
        aes = AES.new(key, DES.MODE_CBC, b'aaaaaaaaaaaaaaaa')
        decoded = aes.decrypt(text)
        entropy = get_entropy(decoded)
        if result.entropy is None or entropy < result.entropy:
            print(entropy)
            result = AttackResult(decoded,key,entropy)

    return result

cbc = ""
ecb = ""

#with open("/home/welters/Downloads/demo24_CBC_encrypted.bmp", 'rb') as file:
#    cbc = file.read()

#with open("/home/welters/Downloads/demo24_ECB_encrypted.bmp", 'rb') as file:
#    ecb = file.read()

#compare_entropy(cbc, ecb)

img = Image.open("/home/welters/Downloads/we800_CBC_encrypted.bmp")
data = img.convert("RGB").tobytes()
result = force_decode(data,1)
data = convert_to_RGB(result.text)
img = Image.new(img.mode, img.size)
img.putdata(data)
img.save("/home/welters/Downloads/we800_CBC_decrypted.bmp")