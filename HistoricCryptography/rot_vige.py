import re
import math

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

    with open(filepath, 'r') as file:
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

def entropy(text):
    freqdict = {}
    update_freq(text, freqdict)
    probdict = compute_prob(freqdict)
    result = 0

    for char in text:
        result -= probdict[char] * math.log(probdict[char],2)
    
    return result


def separator(name):
    print("\n**********************")
    print(name)
    print("**********************")

#Statistic


#ROT
separator("ROT")

source = "tEsT123"
offset = 10

print("Source:",source)

res = rot(source, offset)

print("Result:", res)

encoded = rot(res,offset, True)
if source == encoded:
    print("Decoding works")

#Vigenere
separator("Vigenere")

source = "aBc1ruT3"
key = "abcd"

print("Source:",source)

res = vigenere(source, key)

print("Result:", res)

print(compute_freq_from_file('C:/Users/Z6SZW/Downloads/masc_500k_texts-written/written/journal/Article247_66.txt'))