import random
import hashlib
import numpy as np
import math
import time
import cProfile
import json
import sys



#print('org-msg entry: ', sys.argv[1])

with open(sys.argv[1] , 'rb') as f:
    data = f.read()
    hash_object1 = hashlib.sha256(data)
    #print("hash_value:", hash_object1.hexdigest())
    mu_int = int(hash_object1.hexdigest(), 16)
    #print ("mu_int_value:", mu_int)

    with open(sys.argv[1][:-4] + "_mu_int.json", 'w') as f:
       json.dump(mu_int, f)
    
with open('RSAprivate_key.json', 'r') as f:
   (e, n) = json.load(f)
   private_key = (e, n)


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

# Encrypt a message
def encrypt(mu_int, private_key):
    
    mu_str = str(mu_int)
    cipher_text = [pow(ord(c), private_key[0], private_key[1]) for c in mu_str]
    
    with open(sys.argv[1][:-4] + "_dig_sig.json", 'w') as f:
       json.dump(cipher_text, f)
       
    return cipher_text

def main():

    cipher_text = encrypt(mu_int, private_key)
    #print("Cipher Text: ", cipher_text)
    
    
if __name__ == '__main__':
    main()
