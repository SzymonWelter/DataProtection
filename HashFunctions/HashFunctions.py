import subprocess
import hashlib 
import crypt
import string
import random
import itertools

class Htpasswd:
    filepath = ''

    def __init__(self, filepath):
        self.filepath = filepath

    def CheckIfUserExists(self, username, password):
        command = ['sudo', 'htpasswd', '-vb', self.filepath, username, password]
        result = subprocess.run(command)
        if result.returncode != 0:
            print('User with provided password dont exists in database')
            return
        print('User with provided password exists in database')

    def ChangePassword(self, username):
        command = ['sudo', 'htpasswd', self.filepath, username]
        result = subprocess.run(command)

    def AddUser(self, username, password):
        command = ['sudo', 'htpasswd','-b', self.filepath, username, password]
        result = subprocess.run(command)
        if result.returncode != 0:
            print('can not create user with specified name')
            return
        print('user created')

def md5sum(password):

    m = hashlib.md5(password)
    print(m.digest)
    print(m.hexdigest)

def trivial_hash(data):
        hash = 0
        for char in data:
                hash += ord(char)
        return hash % 999

def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def differentFile(data_len, result):
    data = randomString(data_len)
    while trivial_hash(data) != result:
        data += chr(32)

    with open('text-new','w') as file:
        file.write(data)
        

def bruteforce(hashes, dictionary, passlen):
    result = dict()
    for passwd in itertools.product(dictionary, repeat=passlen):
        passwd = ''.join(passwd)
        for h in hashes:
            pass_hash = crypt.crypt(passwd, h)
            if h == pass_hash:
                result[h] = passwd
                hashes.remove(h)
        if len(hashes) == 0:
            break
    return result

with open('text','r') as file:
    data = file.read()
    result = trivial_hash(data)
    print(result)
    differentFile(100, result)

with open('text-new','r') as file:
    data = file.read()
    result = trivial_hash(data)
    print(result)