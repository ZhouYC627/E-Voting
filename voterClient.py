#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 20:31:06 2020

@author: Yichen Zhou
"""

import genkeys as gk
import myCrypt
import sys, os
import random

class Voter:
    def __init__(self, voterId):
        
        self.pk = {}
        self.sig_pk = {}
        self.voterId = voterId
        
        with open(str(voterId)+'.pub', 'r') as f:
            self.pk['n'] = int(f.readline())
            self.pk['e'] = int(f.readline())
            self.sig_pk['n'] = int(f.readline())
            self.sig_pk['e'] = int(f.readline())
        
        n = self.sig_pk['n']
        while True:
            self.r = random.randint(2, n - 1)
            if gk.gcd(self.r, n) == 1:
                break
        


    def blindMessage(self, m, n, e):
         
         # m'= m * r^e
         blindMessage = (m * pow(self.r,e,n)) % n
         
         return blindMessage
         
    def unwrapSignature(self, signedBlindMessage, n):
        # y = y'/r = x^c
        rInv = gk.modular_inverse(self.r, n)
        
        return ((signedBlindMessage * rInv) % n)
    
    def getEligibility(self):
        return self.eligible





    def blind(self, vote):

        
        self.m =  vote.to_bytes(gk.VOTE_SIZE, sys.byteorder) + os.urandom(gk.RANDOM_SIZE)
        self.m = int.from_bytes(self.m, sys.byteorder)
        print(self.m)
        blindMessage = alice.blindMessage(self.m, self.sig_pk['n'], self.sig_pk['e'])
        
        bmFileName = str(self.voterId) + '.bm'
        #print(blindMessage)
        with open(bmFileName, 'w') as fbm:
            fbm.write(str(self.voterId) + '\n' + str(blindMessage))
        # encrypte bline message with Alice's public key
        myCrypt.encrypt(self.pk['n'], self.pk['e'], bmFileName, bmFileName + '.cip')
        print("Blind messsage: " + bmFileName + " encrypted by public key")
    
    
    def unblind(self, signedFileName):
        with open(signedFileName, 'r') as signf:
            signedMessage = int(signf.readline())
        #print(signedMessage)
    
        signedMessage = alice.unwrapSignature(signedMessage, self.sig_pk['n'])
        #print(signedMessage)
    
        #ballot = str(self.voterId) + '.ballot'
        ballot = 'anonym' + '.ballot'
        with open(ballot, 'w') as bf:
            bf.write(str(self.m) + '\n' + str(signedMessage))
        print("Unblind the signed ballot, output to file: " + ballot)
        print("You can submit it now.")
 
'''           
while True:
    opCode = input()
    
    if opCode == '0':
        voterId = input("Input Id to load public key: ")
        alice = Voter(voterId) 
        vote = int(input("Vote for candidate: "))
        alice.blind(vote) 
    elif opCode == '1':
        signF = input("Signed filename:")
        alice.unblind(signF)
    
    elif opCode == '9':
        break
'''

voterId = input("Input Id to load public key: ")
alice = Voter(voterId) 
vote = int(input("Vote for candidate: "))
alice.blind(vote) 
signF = input("Signed filename:")
alice.unblind(signF)
