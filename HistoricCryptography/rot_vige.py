import re
import math
import itertools
import string

def rot(source, offset, decode = False):
    
    destination = ''
    action = lambda x,y : x + y

    if decode:
        action = lambda x,y : x - y

    for char in source:
        destnum = action(ord(char), offset) % 256
        destchar = chr(destnum)
        destination += destchar
    return destination

def vigenere(source, key, decode = False):

    destination = ''
    sourcelength = len(source)

    for i in range(sourcelength):
        keychar = ord(key[i % len(key)])
        destchar = rot(source[i], keychar, decode)
        destination += destchar
    return destination

def compute_freq_from_file(filepath):

    freqdict = {}

    with open(filepath, 'r',encoding='UTF8') as file:
        for line in file:
            pure_line = remove_whitespaces(line)
            update_freq(pure_line, freqdict)
    return freqdict
            
#https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python
def remove_whitespaces(text):

    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', text)

def update_freq(text, freqdict):

    for char in text:
        if char not in freqdict.keys():
            freqdict[char] = 1
        else:
            freqdict[char] += 1

def compute_prob(freqdict):

    probdict = {}
    size = sum(freqdict.values())

    for k in freqdict.keys():
        probdict[k] = freqdict[k] / size
    
    return probdict

def separator(name):
    print("\n**********************")
    print(name)
    print("**********************")


def read_encoded_file(filepath,offset):
    result = ''
    with open(filepath, 'r',encoding='UTF8') as file:
        for line in file:
            result += rot(line,offset,True)
    return result
#Statistic

def findMax(diction):
    result = {"a": 0}
    for key in diction.keys():
        if diction[key] > result[list(result.keys())[0]]:
            result = {key: diction[key]}
    return result       

#ROT
#separator("ROT")

#source = "tEsT123"
#offset = 10

#print("Source:",source)

#res = rot(source, offset)

#print("Result:", res)

#encoded = rot(res,offset, True)
#if source == encoded:
#    print("Decoding works")

#Vigenere
#separator("Vigenere")

#source = "aBc1ruT3"
#key = "abcd"

#print("Source:",source)

#res = vigenere(source, key)

#print("Result:", res)

#ref_dict = compute_freq_from_file('C:/Users/user/Downloads/written/journal/Article247_66.txt')
#ref_prob = compute_prob(ref_dict)
#ref_res = ord(max(ref_prob,key=lambda key: ref_prob[key]))
#enc_dict = compute_freq_from_file('C:/Users/user/Downloads/crypto.rot')
#enc_prob = compute_prob(enc_dict)
#enc_res = ord(max(enc_prob,key=lambda key: enc_prob[key]))
#print(read_encoded_file('C:/Users/user/Downloads/crypto.rot', abs(enc_res - ref_res)))

#print(findMax(compute_prob(compute_freq_from_file('C:/Users/user/Downloads/written/journal/Article247_66.txt'))))
#print(findMax(compute_prob(compute_freq_from_file('C:/Users/user/Downloads/textpl.txt'))))
