#!/usr/bin/env python3
"""
@author: Jose Humberto Guevara
"""

import binascii
import string

#concept based on: https://crypto.stackexchange.com/questions/59/taking-advantage-of-one-time-pad-key-reuse
#answer by user abijith Kp


#reading the files
def read_info(filename):
    try:
        with open(filename, 'rb') as file:
            return binascii.hexlify(file.read())
    except FileNotFoundError:
        print("File not found: " + filename)
        return None

def read_plain(filename):
    try:
        with open(filename, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found: " + filename)
        return None

#based on https://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

#converting hexadecimal to string, not used in the final version, but still useful.
def hexToText(hexString):
    return ''.join(chr(int(hexString[i:i+2], 16)) for i in range(0, len(hexString), 2))

#converting string to hexadecimal
def textToHex(String):
    return "".join("{:02x}".format(ord(c)) for c in String)

#doing the one time pad
def OTP(message1, message2, hexa):
    cipherText = xor_strings(message1,message2)
    #this part was to test the concept explained by the user abijith Kp
    if hexa == "true":
        cipherText = textToHex(cipherText)
    return cipherText

def finding_info(file1, file2):
    #xoring strings
    cipher = xor_strings(file1, file2)

    #A "<title> Department of Computer Science | The University of New Mexico</title>" http://www.cs.unm.edu/
    #B <title>Jo Cooks - Pretty Darn Delicious Recipes</title><meta name="viewport" https://www.jocooks.com/
    #C <title> UNM Student Union Building (SUB) | The University of New Mexico</title> http://sub.unm.edu/
    #D "Buy bitcoins in three ways sign up, create your order, and make your payment" https://bitcoinofamerica.org/
    word = "UNM Student Union Building (SUB) | The University of New Mexico"

    leng = len(word)
    
    #check = get_all_substrings(file1,'unm')

    #working with possible strings, help gotten from Luc Sim for this part, because the way I was doing it caused strange characters.
    for pos in range(12,len(cipher)-leng):
        xorWord = cipher[pos:pos+leng]

        resultWord = xor_strings(xorWord, word)

        weird = False
        for i in resultWord:
            if i not in string.printable:
                weird = True
                break

        #takes out some uncommon characters.
        if weird == False and '#' not in resultWord and '$' not in resultWord and '*' not in resultWord and '~' not in resultWord and '^' not in resultWord and '%' not in resultWord and '@' not in resultWord:
            print(resultWord)
        weird = False  

def finding_file(file1, file1plaintext, file2plaintext):
    key = xor_strings(file1, file1plaintext)
    
    file3 = xor_strings(key, file2plaintext)

    finding_info(file1, file3)
    

def main():
    #reading files
    file1 = read_info("D")
    file2 = read_info("B")
    
    file1plaintext = read_plain("plaintext4.txt")
    file2plaintext = read_plain("plaintext2.txt")

    #converting files
    file1 = hexToText(file1)
    file2 = hexToText(file2)

    #files that are going to be compared
    finding_info(file1,file2)

    #finding_file(file1,  file1plaintext.decode("utf-8"), file2plaintext.decode("utf-8"))
    
if __name__ == "__main__":
    main()
