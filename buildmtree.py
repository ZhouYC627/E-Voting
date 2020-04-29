#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 19:09:10 2020

@author: Yichen Zhou
"""

import hashlib
import json

import sys
    
class MerkleHashTree():
    
    def __init__(self):
        self.size = 0
        self.tree = {}
        
    def _hash(self, ss):
        return hashlib.sha256(ss.encode()).hexdigest()
    
    def add(self, ss):
        if type(ss) == int:
            ss = str(ss)
        hashValue = self._hash(ss)
        self.size += 1
        self.tree[self.size-1, self.size] = hashValue
        
    def addHash(self, h, k1, k2):
        if k1 + 1 == k2:
            self.size += 1
        self.tree[k1, k2] = h
    
    def mth(self, k1, k2):
        if (k1, k2) in self.tree:
           m  = self.tree[(k1, k2)]
        else:   # add new node
            k = k1 + largestPower2(k2-k1)
            m = self._hash(self.mth(k1, k) + self.mth(k,k2))
            self.tree[(k1, k2)] = m
        return m
    
    def getRoot(self):
        return self.rootHash(self.size)
    
    def rootHash(self, n):
        if not n: n = self.size
        if n>0:
            return self.mth(0, n)
        else:
            return self._hash('')
    
    def tree2Json(self, k1, k2):
        root = {}
        if k1 == k2: 
            return root
        root['d'] = (k1, k2)
        root['hash'] = self.mth(k1, k2)
        if k1+1 < k2:
            k = k1 + largestPower2(k2-k1)
            root['left'] = self.tree2Json(k1, k)
            root['right'] = self.tree2Json(k, k2)
        return root
    
    def find(self, h):
        for i in range(self.size):
            if self.mth(i, i+1)==h:
                return i
        return -1
                
    def auditPath(self, m, n=None):
        if not n: n = self.size
        def _auditPath(m, k1, k2):
            """ Recursively collect audit path """
            if (k2-k1) == 1:
                return [ ] # terminate 
            k = k1 + largestPower2(k2-k1)
            if m < k:
                path = _auditPath(m, k1, k) + [self.mth(k,k2),]
            else:
                path = _auditPath(m, k, k2) + [self.mth(k1,k),]
            return path
        
        return _auditPath(m, 0, n)
        
    
def largestPower2(n):
    c = 1
    while c < n :
        c = c << 1
    return c >> 1

def main(argv):
    mth = MerkleHashTree()
    input = argv[1:]
    #input = ["[alice,", "bob,", "carlol,", "david]"]
    for arg in input:
        str = arg.strip('[],.')
        #print(str)
        mth.add(str)
    #print(mth.rootHash)
    #print(mth.tree)
    with open('merkle.tree', 'w') as outfile:
        json.dump(mth.tree2Json(0, mth.size), outfile, indent=8)    

if __name__ == '__main__':
    main(sys.argv)
'''
input = ["[alice,", "bob,", "carlol,", "david]"]
mth = MerkleHashTree()
for arg in input:
    str = arg.strip('[],.')
    #print(str)
    mth.add(str)
'''
