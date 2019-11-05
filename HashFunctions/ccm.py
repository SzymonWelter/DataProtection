# pip3 install pycryptodomex

from Cryptodome.Cipher import AES

dictionary = {
    'ciphertext': b'\x1b\xe2\x10\xd7{\xb9\x06\x0f\xb7\xf2+\x17\xd1h\xb5\x1d@\nw\xa0,\x93\x8cZ\xaap\nz\xc7^\xefN\x8bt@\xed\xa3#',
    'tag': b'}\xfc\xb0\xcf\xdc\xbaW\xf2\xf6\x064T\x02\xa7\x9f\x16',
    'keys': [b'\xd6\xcc\xecn_\x8a9\x9dF\xef\x8a\xf6\x8d\x02\xc1\xa1',
             b's\xa1\xdd\x9a\x06.\xe5\xe6Qv\xff\xde;V\xb6\x8e', b'\xaf\xa2K\xf9\xa1M~U\xd3s\xbc\xb8\x86\x9a\x13\xce',
             b'4\x06\x86\x91!L\xb1\xb4\xa1\x8c"B\x9cR\no', b'\xa7\x03\xbc\xd9\x040\x10?=\x85\xe0T\xea>\xab\x07',
             b'\xf7\xa5\xbeY\xef\r\x00t\xd4\xaaf\x90\xba\xb3\x80\x0b',
             b'6\x8b*\xee\xcb\xe1T\xd1\x1a\xac\xbdO\x8cR\xdf\xdc',
             b"S\x9f\xb2![9\xa7T\x08E\x98'\xf7\x80\xc8\xa1", b'\xa7\x9b\x07m\xcd\x8e2\xa3\x9c!\xcc\xe0\x06\xfb\xbc$',
             b"\xec\xa0\x81w\xa6\xc8\xa0\x12\x88\xbb\x17~Dj'I"], 'nonces': [b'\x04\x03\xa3o\xf1\xa6\xa2\xf2\xab\x8b#',
                                                                            b'y|\xccY"h\xbfq\x99\x11h',
                                                                            b'\x89\xd5h\xd0\x1fU\xac\x7f}\xa5\x84',
                                                                            b'c&8\x8a\xf5\r\x18l\xd8\xc7`',
                                                                            b'B\xf1\xc6\x8ec\x82\xfd\xae\x81\xc6\xd4',
                                                                            b'\xf2\x9f\x85z\xf3\x7fS\x00\xf9\x7fR',
                                                                            b'\xaf\xbf=\xbekLN\xf3\xe7\x0c0',
                                                                            b'\xc9\xba\xd8\xdd\xcf\x08)\x8a\x8d\xd7\xf6',
                                                                            b'\x12\xf5yJ\xc4\xc6|CQ\xf9\xf6',
                                                                            b'\xd7\x96Z\x89q\xea"\x1ab\xf4\xff']}

ciphertext = dictionary['ciphertext']
tag = dictionary['tag']
keys = dictionary['keys']
nonces = dictionary['nonces']


def encrypt_CCM(data, key, nonce):
    cipher = AES.new(key, AES.MODE_CCM, nonce)
    ciphertext = cipher.encrypt(data)
    tag = cipher.digest()
    return ciphertext, tag


def decrypt_CCM(ciphertext, key, nonce, tag):
    cipher = AES.new(key, AES.MODE_CCM, nonce)

    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
    except ValueError:
        return False

    return plaintext


message = b'\xe1~\x8a\xd1\x96\x84\xc38v\xc7\x8e\x04\x1f\x12\x96p#\xaa\x11t\x17\x9b\x93(/\x7fg\xfa\x9b.\xdd\xe3\x02\xef<\xca\xe7\xac'

# odszyfrowanie z błędną "solą""
if __name__ == '__main__':
    for key in keys:
        for nonce in nonces:
            decrypted = decrypt_CCM(ciphertext, key, nonce, tag)
            if decrypted:
                print("Key: {}\n Nonce: {}".format(key, nonce))
                print(decrypted)
                exit()

# odszyfrowanie poprawne
# decrypted = decrypt_CCM(ciphertext,key,nonce,tag)

# if decrypted:
#	print("Odszyfrowano! Twoja wiadomość:")
#	print(decrypted)
# else:
#	print("Niepoprawne odszyfrowanie!")
