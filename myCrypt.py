#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:37:33 2020

@author: Yichen Zhou
"""

from Crypto.Cipher import AES

import os
import sys    
D = 1
E = 0
KEY_SIZE = 128

def exp_mode(base, exponent, n):
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []

    pre_base = base
    base_array.append(pre_base)

    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n 
        base_array.append(next_base)
        pre_base = next_base

    a_w_b = __multi(base_array, bin_array)
    return a_w_b % n

def __multi(array, bin_array):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
    return result

def encryptK(m, n, e):
    c = exp_mode(m, e, n)
    return c

def decryptK(c, n, d):
    m = exp_mode(c, d, n)
    return m    

encoding = 'utf-8'

def encrypt(n, e, mFile, cFile):
    #with open(pkFile, "r") as pf:
    #    n = int(pf.readline())
    #    e = int(pf.readline())
    #print("n, e")
    #print(n, e)
    with open(mFile, "rb") as mf:
        
        # Generate random key length of KEY_SIZE
        k = os.urandom(KEY_SIZE>>3)
        #print(int.from_bytes(k, sys.byteorder))
        Kp = encryptK(int.from_bytes(k, sys.byteorder), n, e)
        #print(Kp)
        cipher = AES.new(k, AES.MODE_ECB)
        
        with open(cFile, "wb") as cf:
            cf.write(Kp.to_bytes(KEY_SIZE, sys.byteorder))
            while True:
                chunk = mf.read(KEY_SIZE)
                if len(chunk)==0:
                    break
                
                elif len(chunk) % 16 != 0:
                    length = 16 - (len(chunk) % 16)
                    chunk += bytes([length])*length
                    #print(chunk)
                    
                #chunk = Padding.appendPadding(chunk, KEY_SIZE, mode='Space')
                #print(chunk)
                #print(len(chunk))
                ct = cipher.encrypt(chunk)
                cf.write(ct)
    
def decrypt(n, d, cFile, mFile):
    #with open(prFile, "r") as pf:
    #    n = int(pf.readline())
    #    d = int(pf.readline())
    #print("n, d")
    #print(n, d)
    with open(cFile, "rb") as cf:
        
        Kp = int.from_bytes(cf.read(KEY_SIZE), sys.byteorder)
        #print(Kp)
        k = decryptK(Kp, n, d)
        #print(k)
        k = k.to_bytes(KEY_SIZE>>3, sys.byteorder)
        cipher = AES.new(k, AES.MODE_ECB)
        
        result = b''
        while True:
            chunk = cf.read(KEY_SIZE)
            #print("***", chunk)
            if len(chunk)==0:
                break
            pt = cipher.decrypt(chunk)
            #pt = Padding.removePadding(pt, mode='Space')
            #print(pt.decode())
            result += pt
            
        with open(mFile, "w+") as mf:
            result = result[:-result[-1]]

            mf.write(result.decode(encoding))
        #print(result)

        
#encrypt("alice.pub", "message.txt", "message.cip")   
#decrypt("alice.prv", "message.cip", "decrypted.txt")

def main(argv):
    
    if argv[1]=="-d":
        mode = D
    elif argv[1]=="-e":
        mode = E
    else:
        print("usage: -e for encryption; -d for decryption")
        #exit()
    if mode == D:
        decrypt(argv[2], argv[3], argv[4])
    elif mode == E:
        encrypt(argv[2], argv[3], argv[4])
        
    
        
if __name__ == "__main__":
    main(sys.argv)
