import multiprocessing
import time
import ctypes

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encryptCBC(text, key):
    vector = bytearray(text, 'utf-8')
    aes = AES.new(key, AES.MODE_ECB)
    for i in range(blocksNumber):
        offset = i * AES.block_size
        block = text[offset:offset + AES.block_size]       
        encrypted = aes.encrypt(block)
        vector[offset:offset + AES.block_size] = bytearray(encrypted)
    return bytes(vector)

def decryptCBC(encrypted, key):
    vector = bytearray(encrypted)
    aes = AES.new(key, AES.MODE_ECB)
    for i in range(blocksNumber):
        offset = i * AES.block_size
        block = encrypted[offset:offset + AES.block_size]
        decrypted = aes.decrypt(block)
        vector[offset:offset + AES.block_size] = bytearray(decrypted)
    return bytes(vector)

def mapper(i):
    offset = i * AES.block_size
    block = inputData[offset:offset + AES.block_size]
    encrypted = aes.encrypt(bytes(block))
    outputData[offset:offset + AES.block_size] = bytearray(encrypted)
    return i

with open('text','r') as file:
    plain_text = file.read()
key = "sTrOnkkEy@13&$2)"
iv = get_random_bytes(16)
blocksNumber = int(len(plain_text) / AES.block_size)

start = time.time()
encrypted = encryptCBC(plain_text, key)
end = time.time()

decrypted = decryptCBC(encrypted, key)
print(decrypted)

aes = AES.new(key, AES.MODE_ECB)
inputData = multiprocessing.RawArray(ctypes.c_byte, bytearray(plain_text,'utf-8'))
outputData = multiprocessing.RawArray(ctypes.c_byte, bytearray(plain_text,'utf-8'))
pool = multiprocessing.Pool(4)

starttime = time.time()
pool.map(mapper, range(blocksNumber))
endtime = time.time()

#decrypted = decryptCBC(outputData, key)

#decrypted = decrypted.replace('"\"n','\n')
#print(decrypted)

print(f'cbc : {end - start}')
print(f'cbc parallel: {endtime - starttime}')
