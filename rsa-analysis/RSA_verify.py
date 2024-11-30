#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 04:13:06 2023

@author: atinder
@editor: mohammed
"""

import random
import hashlib
import numpy as np
import math
import time
import cProfile
import json
import sys

    
with open(sys.argv[1], 'r') as f:
   mu_int = str(json.load(f))
   #print("mu_int", sys.argv[1])

with open(sys.argv[2], 'r') as f:
   cipher_text = json.load(f)
   #print("cipher_text", sys.argv[2])

with open('RSApublic_key.json', 'r') as f:
   (d, n) = json.load(f)
   public_key = (d, n)

# Check if a number is prime
def is_prime(N):
    if N == 2 or N == 3:
        return True
    if N <= 1 or N % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(N)) + 1, 2):
        if N % i == 0:
            return False
    return True

# Compute the greatest common divisor of a and b
def gcd(l, u):
    while u != 0:
        l, u = u, l % u
    return l

# Compute the modular multiplicative inverse of a modulo m
def mod_inv(l, F):
    if gcd(l, F) != 1:
        return None
    u1, u2, u3 = 1, 0, l
    v1, v2, v3 = 0, 1, F
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1,
            u2 - q * v2,
            u3 - q * v3,
            v1,
            v2,
            v3,
        )
    return u1 % F

# Decrypt the message
def decrypt(cipher_text, public_key):
    d, n = public_key
    plaintext = [chr(pow(c, d, n)) for c in cipher_text]
    plaintext="".join(plaintext)
    
    # Verification
    left = mu_int
    right = plaintext
    
    if left == right:
        verdict = 'VALID'
    else:
        verdict = 'INVALID'
    
    verify = {
        "left": left,
        "right": right
        }
    
    #print("left: ", verify["left"])
    #print("right: ", verify["right"])
    #print("verdict says that this signature is: " , verdict)
    
    return "".join(plaintext)


def main():
    plaintext = decrypt(cipher_text, public_key)
    
if __name__ == '__main__':
    main()

