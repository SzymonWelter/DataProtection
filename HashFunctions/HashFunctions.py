import subprocess
import hashlib 
import crypt
import string
import random
import itertools
import passlib.hash
import timeit

class Htpasswd:
    filepath = ''
    users = {}
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        self.users = {}
        with open(self.filepath,  'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                self.users[username] = password
            
    def save(self):
        with open(self.filepath,  'w') as file:
            for key in self.users:
                line = key + ':' + self.users[key]
                file.write(line + '\n')
        print('saved')

    def CheckIfUserExists(self, username, password):
        if  not self.users.keys().__contains__(username):
            print('username is not in database')

        salt = self.users[username].split('$')[2]
        password = passlib.hash.apr_md5_crypt.hash(password, salt=salt)
        if password == self.users[username]:
            return True
        else:
            return False
        


    def ChangePassword(self, username):
        print('Old password:')
        oldPassword = input()
        if not self.CheckIfUserExists(username, oldPassword):
            print('wrong password')
            return
        salt = self.users[username].split('$')[2]
        print('New password:')
        newPassword = input()
        password = passlib.hash.apr_md5_crypt.hash(newPassword, salt=salt)
        self.users[username] = password



    def AddUser(self, username, password):
        command = ['sudo', 'htpasswd','-b', self.filepath, username, password]
        result = subprocess.run(command)
        if result.returncode != 0:
            print('can not create user with specified name')
            return
        print('user created')

    def BruteForce_md5(self, passlen,method):
        hashes = self.users.values()
        result = {}
        for h in hashes:
            for passwd in itertools.product(string.ascii_lowercase, repeat=passlen):
                passwd = ''.join(passwd)
                pass_hash = method(passwd, salt = h.split('$')[2])            
                print(pass_hash)
                if h == pass_hash:
                    result[h] = passwd
                    break
        return result

    

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
        

def md5_ascii():
    crypt.crypt(''.join(random.choices(string.ascii_lowercase, k=3)), crypt.METHOD_MD5)


def crypt_ascii():
    crypt.crypt(''.join(random.choices(string.ascii_lowercase, k=3)), crypt.METHOD_CRYPT)


def compare_time(iterations):
    m5time = timeit.timeit(md5_ascii, number=iterations)
    print(f'md5: {iterations / m5time} hashes per second.' )
    cryptime = timeit.timeit(crypt_ascii, number=iterations)
    print(f'crypt: {iterations / cryptime} hashes per second')


compare_time(10000)
