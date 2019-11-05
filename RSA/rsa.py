import random
from Crypto.PublicKey import RSA 
import string

def textToDigits(text):
    digits = []
    for char in text:
        digits.append(ord(char))
    return digits

def digitsToText(digits):
    text = ""
    for digit in digits:
        text += chr(digit)
    return text

def isPrimeNumber(number):
    numbers = [True] * (number+1)
    i = 2
    while i < number:
        while not numbers[i] and i < number:
            i += 1
        j = 2*i
        while j <= number:
            numbers[j] = False
            j+=i
        i+=1
    return numbers[number]

def nwd(a, b):
    m = a % b
    while(not m == 0):
        a = b
        b = m
        m = a % b
    return b

def relPrime(a, b):
    return nwd(a,b) == 1

def invModulo(a, b):
    u, w, x, z = 1, a, 0, b
    while w != 0:
        if w < z:
            u, x = x, u
            w, z = z, w
        q = int(w / z)
        u -= q * x
        w -= q * z
    if z != 1:
        return
    if x < 0:
        x += b
    return x

def modPow(a, b, c):
    binaryb = bin(b).split('b')[1]
    powers = []
    result = 1
    powers.append(a % c)
    powers.append((a*a) % c)
    for i in range(len(binaryb)-2):
        powers.append((powers[-1]**2) % c)
    for i in range(0, len(binaryb)):
        if(binaryb[i] == '1'):
            result *= powers[-(i+1)]
    return result % c

def generateKeys():
    primes = [i for i in range(2, 100) if isPrimeNumber(i)]
    p = random.choice(primes)
    q = random.choice(primes)
    n = p*q
    e = random.randint(1, 100)
    while not relPrime(e, (p-1)*(q-1)):
        e = random.randint(1, 100)
    d = invModulo(e, (p-1)*(q-1))
    return [e,n], [d,n]

def rsa(message, key):
    result = []
    for m in message:
        result.append(modPow(m, key[0], key[1]))
    return result

def encryptFile(path, pub_key):
    salt = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    result = ''
    with open(path, 'r', 'utf-8') as file:
        for line in file:
            result += pub_key.encrypt(line, salt)
    with open(path, 'w') as file:
        file.write(result)

def decryptFile(path, priv_key):
    result = ''
    with open(path, 'r', 'utf-8') as file:
        for line in file:
            result += priv_key.decrypt(line)
    with open(path, 'w') as file:
        file.write(result)
    


pub, priv = generateKeys()
encrypt = rsa([9,5,2,66,23,5],pub)
print(encrypt)
print(rsa(encrypt,priv))

