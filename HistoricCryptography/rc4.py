def ksa(key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(text):
    i = 0
    j = 0
    while True:
        i = ( i + 1 ) % 256
        j = ( j + text[i] ) % 256 
        text[i], text[j] = text[j], text[i]

        key = text[(text[i] + text[j])]
        yield key


