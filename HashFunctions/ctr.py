import multiprocessing
import time
import ctypes
import os

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

random = get_random_bytes(8)
counter = lambda: random

def encryptCTR(text, key):
    des = DES.new(key, DES.MODE_CTR, counter=counter)
    vector = bytearray(text, 'utf-8')
    for i in range(blocksNumber):
        offset = i * DES.block_size
        block = text[offset:offset + DES.block_size]        
        encrypted = des.encrypt(block)    
        vector[offset:offset + DES.block_size] = bytearray(encrypted)
    return bytes(vector)


def decryptCTR(encrypted, key):
    vector = bytearray(encrypted)
    des = DES.new(key, DES.MODE_CTR, counter=counter)
    for i in range(blocksNumber):
        offset = i * DES.block_size
        block = encrypted[offset:offset + DES.block_size]        
        decrypted = des.decrypt(block)        
        vector[offset:offset + DES.block_size] = bytearray(decrypted)
    return bytes(vector)

def mapper(i):
    offset = i * DES.block_size
    block = bytes(inputData[offset:offset + DES.block_size])
    decrypted = des.decrypt(block)
    outputData[offset:offset + DES.block_size] = bytearray(decrypted)
    return i

with open('text','r') as file:
    text = file.read()
key = "sTrOnkEy"

iv = get_random_bytes(16)
blocksNumber = int(len(text) / DES.block_size)

starttime = time.time()
encrypted = encryptCTR(text,key)
print(f'ctr: {time.time() - starttime}')

starttime = time.time()
decrypted = decryptCTR(encrypted, key)
print("".join(map(chr, decrypted)))
print(f'decrypt ctr : {time.time() - starttime}')


des = DES.new(key, DES.MODE_CTR, counter=counter)
inputData = multiprocessing.RawArray(ctypes.c_ubyte, encrypted)
outputData = multiprocessing.RawArray(ctypes.c_ubyte, encrypted)
pool = multiprocessing.Pool(4)
starttime = time.time()
pool.map(mapper, range(blocksNumber))
endtime = time.time()

decrypted = "".join(map(chr, bytes(outputData)))
decrypted = decrypted.replace('"\"n','\n')
print(decrypted)

print(f'ctr: {endtime - starttime}')
