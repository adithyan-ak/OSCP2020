import string

def encrypt(key, msg):
    key = list(key)
    msg = list(msg)
    for char_key in key:
        for i in range(len(msg)):
            if i == 0:
                tmp = ord(msg[i]) + ord(char_key) + ord(msg[-1])
            else:
                tmp = ord(msg[i]) + ord(char_key) + ord(msg[i-1])

            while tmp > 255:
                tmp -= 256
            msg[i] = chr(tmp)
    return ''.join(msg)

def decrypt(key, msg):
    key = list(key)
    msg = list(msg)
    for char_key in reversed(key):
        for i in reversed(range(len(msg))):
            if i == 0:
                tmp = ord(msg[i]) - (ord(char_key) + ord(msg[-1]))
            else:
                tmp = ord(msg[i]) - (ord(char_key) + ord(msg[i-1]))
            while tmp < 0:
                tmp += 256
            msg[i] = chr(tmp)
    return ''.join(msg)

# Read message
with open('ciphertext', 'rb') as file:
    ciphertext = file.read()

# Bruteforce passwords
myFile = open('/usr/share/wordlists/rockyou.txt', "rt")
for myLine in iter(myFile):
    password = myLine.strip('\n')
    print('Trying: {}'.format(password))
    out = decrypt(password, ciphertext)
    numPlainText = 0
    for i in out:
        if i in string.printable:
            numPlainText += 1
    if numPlainText > 140:
        print(out)
        raw_input('Press any key to continue')
