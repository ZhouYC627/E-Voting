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

voterId = 1000
pk = {}
sig_pk = {}

VOTE_SIZE = 2
RANDOM_SIZE = 14

class Voter:
    def __init__(self, n, eligible=True):
        self.eligible = eligible
        
        '''
        while True:
            self.r = random.randint(2, n - 1)
            if gk.gcd(self.r, n) == 1:
                break
        '''
        self.r = 37873806644082383478458252412751201524495315897618792659525329616769323318906
        
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

with open(str(voterId)+'.pub', 'r') as f:
    pk['n'] = int(f.readline())
    pk['e'] = int(f.readline())
    sig_pk['n'] = int(f.readline())
    sig_pk['e'] = int(f.readline())

sig_pk = {'n': 53128908078574294373606002113429558723820542853806750777228868933504583592389, 'e': 3878595324844751204948065592472856792067471054963070252780930172866355538531}
sig_sk = {'n': 53128908078574294373606002113429558723820542853806750777228868933504583592389, 'd': 44590113836575741656904861073097404271005280558578159274614812347102415668191}


alice = Voter(sig_pk['n'])
m = 54957808117987922404636758262565634049
def blind(vote):
    #m =  vote.to_bytes(VOTE_SIZE, sys.byteorder) + os.urandom(RANDOM_SIZE)
    #m = int.from_bytes(m, sys.byteorder)
    blindMessage = alice.blindMessage(m, sig_pk['n'], sig_pk['e'])
    
    bmFileName = str(voterId) + '.bm'
    print(blindMessage)
    with open(bmFileName, 'w') as fbm:
        fbm.write(str(voterId) + '\n' + str(blindMessage))
    # encrypte bline message with Alice's public key
    myCrypt.encrypt(pk['n'], pk['e'], bmFileName, bmFileName + '.cip')


def unblind(signedFileName):
    with open(signedFileName, 'r') as signf:
        signedMessage = int(signf.readline())
    print(signedMessage)

    signedMessage = alice.unwrapSignature(signedMessage, sig_pk['n'])
    print(signedMessage)

    ballot = 'ballot'
    with open(ballot, 'w') as bf:
        bf.write(str(m) + '\n' + str(signedMessage))
        
#blind(1) 

unblind('1000.sign')



