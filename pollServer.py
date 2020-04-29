#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:52:54 2020

@author: Yichen Zhou
"""

from buildmtree import MerkleHashTree
import genkeys as gk
import myCrypt
import sys


#server = bs.Signer()
KEY_SIZE =128
opCode = 1
idCount = 1000

voters = {}

sig_pk, sig_sk = gk.generateKey()

def register(eligible):
    if eligible== 'y':
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
        print("Public Key:" + str(voterId)+'.pub')
        
    else:
        print("You cannot vote.")
        input()
        
def signMessage(message):
    return pow(message, sig_sk['d'], sig_sk['n'])

def validBallot(m, signedMessage):
    return m == pow(signedMessage, sig_pk['e'], sig_pk['n'])


def checkBallot(mth, m):
    if type(m) == int:
        m = str(m)
    hash_m = mth._hash(m)
    return mth.find(hash_m)

def m2v(m):
    if type(m) == str:
        m = int(m)
    v = m.to_bytes(gk.VOTE_SIZE + gk.RANDOM_SIZE, sys.byteorder)
    return int.from_bytes(v[:gk.VOTE_SIZE], sys.byteorder)

mth = MerkleHashTree()
votes = []

while True:
    print("Please input Operation code:\n 0: register;\n 1: sign;\n 2: submit ballot;\n 3: count;\n 4: verify vote;\n 9: exit\n")

    opCode = input()
    
    if opCode == '0': # register
        eligible = input("Are you eligible? (y/n) :")  
        #voterInfo = 'Alice'     
        register(eligible)
    elif opCode == '1': # sign
        voterId = int(input("Voter Id: "))
        #voterId = 1000
        
        if voterId not in voters:
            print("Invalid Id, please register first\n")
            continue
        
        sk = voters[voterId]
        
        
        bmFile = str(voterId) + '.bm'
        myCrypt.decrypt(sk['n'], sk['d'], bmFile + '.cip', bmFile)
        print("Reading blind message from: " + bmFile)
        with open(bmFile, 'r') as bmf:
            encrypted_voterId = int(bmf.readline())
            blindMessage = int(bmf.readline())
            #print(blindMessage)
            
        if encrypted_voterId != voterId:
            print("Fail to verify voter!\nTry again")
            continue
        
        print("Registered voter")
        with open(str(voterId) + '.sign', 'w') as signf:
            signf.write(str(signMessage(blindMessage)))
            print("Signed to:" + str(voterId) + '.sign')
            
    elif opCode == '2':
        ballot = input("Ballot filename: ")
        with open(ballot, 'r') as bf:
            m = int(bf.readline())
            print(m)
            signedMessage = int(bf.readline())
            if validBallot(m, signedMessage):
                print("valid ballot")
            else:
                print("invalid ballot")
                continue
        
        # rule out repeated votes
        exist = checkBallot(mth, str(m))
        if exist >=0 :
            print("Repeated Vote! Invalid!")
            continue
        
        #v = m2v(m)


        print("Ballot received.")
        
        votes.append(m)
        mth.add(m)
        
    
    elif opCode == '3': # Count
        
        print("Verifying all votes...")
        vTree = MerkleHashTree()
        for m in votes:
            vTree.add(m)
        if vTree.getRoot()==mth.getRoot():
            print("Good!")
        else:
            print("Bad!")
            break
        print(mth.tree2Json(0, mth.size))


        candidates = {}
        for m in votes:
            v = m2v(m)
            if v in candidates:
                candidates[v] += 1
            else:
                candidates[v] = 1
        print(candidates)

    elif opCode == '4': # Verify votes
        #mFileName = input("input your vote hash")
        #with open(mFileName, 'r') as mf:
        #    m = int(mf.readline())
        m = input("Your vote:")
        if checkBallot(mth, m) < 0:
            print("This vote has not been tallied!")
        else:
            print("This vote has been tallied!")
            
    elif opCode == '9':
        break



        
    








