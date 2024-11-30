#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 00:00:32 2023

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

# With open('/Users/atinder/Desktop/original_text_2091words12.txt', 'rb') as f:
# message = b'This is a secret message.'
# hash_object1 = hashlib.sha256(message)
# print("hash_value:", hash_object1.hexdigest())
# mu = int(hash_object1.hexdigest(), 16)
# print ("Int_value_msg1:", mu)
    


# Generate a new RSA key pair
start_time = time.time()
#def generate_primes():
    #p = 19
   # q = 17
   # while True:
     #   p = random.randint(1000, 10000)
     #   if is_prime(p):
        #    break
   # while True:
        #q = random.randint(1000, 10000)
       # if is_prime(q):
       #     break
  #  return p, q

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
        l,u = u, l % u
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

# Generate public and private keys
def generate_keys(p=19, q=17):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    d = mod_inv(e, phi_n)
    #return (e, n), (d, n)
    with open('RSAprivate_key.json', 'w') as f:
         json.dump((d,n), f)
    with open('RSApublic_key.json', 'w') as f:
         json.dump((e, n), f)
    return (e, n), (d, n)
    #print("public keys:",(e, n))
end_time = time.time()
key_gen_time = (end_time - start_time) * 100000


def main():

    public_key, private_key = generate_keys(p=19, q=17)
    print("Public key (e, n):", public_key)
    print("Private key (d, n):", private_key)
    
    
if __name__ == '__main__':
    main()
