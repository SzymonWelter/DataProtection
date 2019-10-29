import multiprocessing
import time
import ctypes

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encryptCBC(text, key):
    vector = bytearray(text, 'utf-8')
    aes = AES.new(key, AES.MODE_CBC,iv)
    for i in range(blocksNumber):
        offset = i * AES.block_size
        block = text[offset:offset + AES.block_size]       
        encrypted = aes.encrypt(block)
        vector[offset:offset + AES.block_size] = bytearray(encrypted)
    return bytes(vector)

def decryptCBC(encrypted, key):
    vector = bytearray(encrypted)
    aes = AES.new(key, AES.MODE_CBC, iv)
    for i in range(blocksNumber):
        offset = i * AES.block_size
        block = encrypted[offset:offset + AES.block_size]
        decrypted = aes.decrypt(block)
        vector[offset:offset + AES.block_size] = bytearray(decrypted)
    return bytes(vector)

def mapper(i):
    offset = i * AES.block_size
    block = bytes(shared_data[offset:offset + AES.block_size])
    decrypted = aes.decrypt(block)
    output_data[offset:offset + AES.block_size] = bytearray(decrypted)
    return i

with open('text','r') as file:
    plain_text = file.read()
key = "sTrOnkkEy@13&$2)"
iv = get_random_bytes(16)
blocksNumber = int(len(plain_text) / AES.block_size)


encrypted = encryptCBC(plain_text, key)
start = time.time()
decrypted = decryptCBC(encrypted, key)
end = time.time()


aes = AES.new(key, AES.MODE_CBC,iv)
shared_data = multiprocessing.RawArray(ctypes.c_ubyte, encrypted)
output_data = multiprocessing.RawArray(ctypes.c_ubyte, encrypted)
pool = multiprocessing.Pool(4)
starttime = time.time()
pool.map(mapper, range(blocksNumber))
endtime = time.time()

decrypted = "".join(map(chr, bytes(output_data)))
decrypted = decrypted.replace('"\"n','\n')
print(decrypted)

print(f'cbc : {end - start}')
print(f'cbc parallel: {endtime - starttime}')
