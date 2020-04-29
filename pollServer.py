#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:52:54 2020

@author: Yichen Zhou
"""

import blindSignature as bs
from Crypto.PublicKey import RSA
import genkeys as gk
import myCrypt
import sys


#server = bs.Signer()
KEY_SIZE =128
opCode = 1
idCount = 1000

names = {'Alice', 'Bob'}
voters = {}

sig_pk, sig_sk = gk.generateKey()

def register(personalInfo):
    if (personalInfo in names):
        pk, sk = gk.generateKey()
        
        # generate unique id
        global idCount
        voterId = idCount
        idCount += 1
        with open(str(voterId)+'.pub', 'w') as f:
            f.write(str(pk['n']) + '\n')
            f.write(str(pk['e']) + '\n')
            f.write(str(sig_pk['n']) + '\n')
            f.write(str(sig_pk['e']) + '\n')
            
        # store voter's id and private key
        voters[voterId] = sk;
        
        print('Registed!')
        
def signMessage(message):
    return pow(message, sig_sk['d'], sig_sk['n'])

def validBallot(m, signedMessage):
    return m == pow(signedMessage, sig_pk['e'], sig_pk['n'])


print("Please input Operation code:\n 0: register;\n 1: sign;\n 9: exit\n")
while True:
    opCode = input()
    
    if opCode == '0': # register
        #voterName = input("Personal Info: ")  
        voterInfo = 'Alice'     
        register(voterInfo)
    elif opCode == '1': # sign
        #voterId = input("Voter Id")
        voterId = 1000
        
        if voterId not in voters:
            print("Invalid Id, please register first\n")
            continue
        
        sk = voters[voterId]
        
        
        bmFile = str(voterId) + '.bm'
        myCrypt.decrypt(sk['n'], sk['d'], bmFile + '.cip', bmFile)
        with open(bmFile, 'r') as bmf:
            encrypted_voterId = int(bmf.readline())
            blindMessage = int(bmf.readline())
            print(blindMessage)
            
        if encrypted_voterId != voterId:
            print("Fail to verify voter!\nTry again")
            continue
        
        print("Registered voter")
        with open(str(voterId) + '.sign', 'w') as signf:
            signf.write(str(signMessage(blindMessage)))
            print("Signed to:" + str(voterId) + '.sign')
            
    elif opCode == '2':
        with open('ballot', 'r') as bf:
            m = int(bf.readline())
            print(m)
            signedMessage = int(bf.readline())
            if validBallot(m, signedMessage):
                print("valid ballot")
            else:
                print("invalid ballot")
                continue
        
        v = m.to_bytes(gk.VOTE_SIZE + gk.RANDOM_SIZE, sys.byteorder)
        v = int.from_bytes(v[:gk.VOTE_SIZE], sys.byteorder)
        print(v)
        
    
            
    elif opCode == '9':
        break
    print('.')



        
    








