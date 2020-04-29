#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:59:31 2020

@author: Yichen Zhou
"""
from random import randrange
import sys
import os

VOTE_SIZE = 2
RANDOM_SIZE = 14

def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True



def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    #p = getrandbits(length)
    #p = int(os.urandom(length).encode('hex'), 16)
    length = length >> 3 # bits to bytes
    p = int.from_bytes(os.urandom(length), sys.byteorder)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=128):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


def gcd(a,b): 
    if b==0: 
        return a 
    else: 
        return gcd(b, a % b)

    
def modular_inverse(a, b):
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a
    ob = b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob 
    if ly < 0:
        ly += oa
    return lx

def generateKey():
    # Generates public and private keys and saves them to a file.
    p = generate_prime_number()
    q = generate_prime_number()
    phi = (p - 1)*(q - 1)
    n = p*q


    while True:
        e = randrange(2, phi)
        if gcd(e, phi) == 1:
            break
        
    d = modular_inverse(e, phi)
   
    publicKey = {"n" : n, "e": e}
    privateKey = {"n" : n, "d": d}

    return[(publicKey),(privateKey)]

def main(argv):
    name = argv[1]
    p = generate_prime_number()
    q = generate_prime_number()
    
    assert is_prime(p)
    assert is_prime(q)
    
    n = p * q
    #print(p, q, n)
    t = (p - 1) * (q - 1)
    
    
    # select e
    while True:
        e = randrange(2, t)
        if gcd(e, t) == 1:
            break

    d = modular_inverse(e, t)


    pk = name + ".pub"
    sk = name + ".prv"
    
    
    with open(pk, "w") as pub:
        pub.write(str(n))
        pub.write('\n')
        pub.write(str(e))

    with open(sk, "w") as prv:
        prv.write(str(n))
        prv.write('\n')
        prv.write(str(d))
        

if __name__ == "__main__":
    main(sys.argv)
  