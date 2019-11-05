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
