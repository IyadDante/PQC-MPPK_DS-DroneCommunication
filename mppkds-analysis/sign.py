#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:55:59 2023

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

print('org-msg entry: ', sys.argv[1])

with open(sys.argv[1] , 'rb') as f:
    data = f.read()
    hash_object1 = hashlib.sha256(data)
    #print("hash_value:", hash_object1.hexdigest())
    mu = int(hash_object1.hexdigest(), 16)
    #use ASCII convertor and put in report as a note 
    print ("Int_value_msg1:", mu)
    
    
with open('./private_key.json', 'r') as f:
   s = json.load(f)


def S(s, mu, m, n, lambda_, ell, p):
    
   #for j in range(1000000000000000000000):
        
    f = np.array(s[0])
    h = np.array(s[1])
    R0 = np.array(s[2]) 
    Rn = np.array(s[3])
    Ephi = np.array(s[4])
    Epsi = np.array(s[5])
    
    tp = p - 1
    
    # Random base
    g = np.random.randint(2, tp-1)
    
    # Evaluate on μ
    fm = np.polyval(np.flip(f), mu)
    a = np.mod(R0*fm, tp)
    A = powermod(g, a, p)
    
    # Evaluate on μ
    hm = np.polyval(np.flip(h), mu)
    b = np.mod(Rn*hm, tp)
    B = powermod(g, b, p)
    
    c = np.mod(Rn * (hm*f[0] - fm*h[0]), tp)
    C = powermod(g, c, p)
    
    d = np.mod(R0 * (hm*f[lambda_] - fm*h[lambda_]), tp)
    D = powermod(g, d, p)
    
    # Evaluate on μ
    Ephim = np.polyval(np.hstack([np.flip(Ephi), 0]), mu)
    Ephim = np.mod(Ephim, tp)
    
    # Evaluate on μ
    Epsim = np.polyval(np.hstack([np.flip(Epsi), 0]), mu)
    Epsim = np.mod(Epsim, tp)
    
    e = np.mod(R0*Rn*(hm*Ephim - fm*Epsim), tp)
    E = powermod(g, e, p)
    
    # Digital signature
    t = [A, B, C, D, E]
    
    with open(sys.argv[1][:-4] + "_dig_sig.json", 'w') as f:
       json.dump(t, f)
    return t

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
  #  s, v = keygen(m, n, lambda_, ell, p)
  #  print("Private Key: ", s)
   # print("Public Key: ", v)
    t = S(s, mu, m, n, lambda_, ell, p)
    print('Digital Signature:',t)
   # verify = V(v, mu, t, m, n, lambda_, ell, p)
    
    
if __name__ == '__main__':
    main()
