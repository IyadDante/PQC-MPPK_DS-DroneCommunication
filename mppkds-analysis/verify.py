#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:05:32 2023

@author: atinder
@editor: mohammed
"""
def powermod(base, exponent, modulus):
    """Calculate (base ^ exponent) % modulus efficiently."""
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result

import random
import hashlib
import numpy as np
import math
import time
import cProfile
import json
import sys
print('argv entries : ', sys.argv)
print('org-msg : ', sys.argv [1])
print('dig-sig : ', sys.argv [2])

with open(sys.argv[1], 'rb') as f:
    data = f.read()
    hash_object1 = hashlib.sha256(data)
    print("hash_value:", hash_object1.hexdigest())
    mu = int(hash_object1.hexdigest(), 16)
#use ASCII convertor and put in report as a note 
    print ("Int_value_msg1:", mu)
    
    
    with open(sys.argv[2], 'r') as f:
       t = json.load(f)
    with open('public_key.json', 'r') as f:
       v = json.load(f)

def V(v, mu, t, m, n, lambda_, ell, p):
    # v = public key
    P = np.array(v[0]); Q = np.array(v[1]); N0 = np.array(v[2]); Nn = np.array(v[3])
    
    A = t[0]; B = t[1]; C = t[2]; D = t[3]; E = t[4]
    tp = p - 1  # Euler's totient of p
    
    # Noise variables
    r = np.random.randint(1, tp-1, size=m)
    # r = [2 2]
    
    # Evaluate P, Q, N0, and Nn
    barP = 0; barQ = 0
    for i in range(1, n+lambda_):
        for j1 in range(0, ell[0]+1):
            for j2 in range(0, ell[1]+1):
                barP = (barP + P[i-1, j1*2+j2]*powermod(r[0], j1, tp)*powermod(r[1], j2, tp)*powermod(mu, i, tp)) % tp
                barQ = (barQ + Q[i-1, j1*2+j2]*powermod(r[0], j1, tp)*powermod(r[1], j2, tp)*powermod(mu, i, tp)) % tp
    
    barN0 = 0; barNn = 0
    for j1 in range(0, ell[0]+1):
        for j2 in range(0, ell[1]+1):
            barN0 = (barN0 + N0[j1*2+j2]*powermod(r[0], j1, tp)*powermod(r[1], j2, tp)) % tp
            barNn = (barNn + Nn[j1*2+j2]*powermod(r[0], j1, tp)*powermod(r[1], j2, tp)) % tp
    
    barNn = (barNn * pow(mu, n+lambda_, tp)) % tp
    
    # Verification
    left = powermod(A, barQ, p)
    right = (powermod(B, barP, p) * powermod(C, barN0, p) * powermod(D, barNn, p) * E) % p
    
    if left == right:
        verdict = 'VALID'
    else:
        verdict = 'INVALID'
    
    verify = {
        "left": left,
        "right": right
        }
    
    print("left: ", verify["left"])
    print("right: ", verify["right"])
    
    print("verdict says that this encryption is: " , verdict)
    
    return verify



def main():
    # Finite Field index
    p = 19
    # Euler's totient of p
    tp = p - 1
    # number of noise variables
    m = 2
    # degree of base polynomial
    n = 2
    # degree of multiplier polynomials
    lambda_ = 1 # linear
    # upper limits
    ell = [1,1]
    #mu = random.randint(0, p-1)
    # Key generation
   # s, v = keygen(m, n, lambda_, ell, p)
   # print("Private Key: ", s)
    #print("Public Key: ", v)
    #t = S(s, mu, m, n, lambda_, ell, p)
    #print(t)
    verify = V(v, mu, t, m, n, lambda_, ell, p)
    
    
if __name__ == '__main__':
    main()
