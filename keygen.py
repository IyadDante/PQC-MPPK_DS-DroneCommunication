#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:26:58 2023

@author: atinder
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:41:54 2023

@author: Atinderpal Singh 
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

with open('Message.txt', 'rb') as f:
#with open('/Users/atinder/Desktop/original_text_2091words12.txt', 'rb') as f:
    data = f.read()
    hash_object1 = hashlib.sha256(data)
    print("hash_value:", hash_object1.hexdigest())
    mu = int(hash_object1.hexdigest(), 16)
#use ASCII convertor and put in report as a note 
    print ("Int_value_msg1:", mu)

# Start the timer
start_time = time.time()
def keygen(m, n, lambda_, ell, p):
    tp = p - 1

    # 1. Base Polynomial
    c = np.random.randint(0, tp-1, size=(n+1, (ell[0]+1)*(ell[1]+1)))

    # 2. Univariate polynomials
    f = np.random.randint(0, tp-1, size=(1, lambda_+1))
    h = np.random.randint(0, tp-1, size=(1, lambda_+1))

    # 3. Product polynomials
    phi = np.zeros((n+lambda_+1, (ell[0]+1)*(ell[1]+1)))
    psi = np.zeros((n+lambda_+1, (ell[0]+1)*(ell[1]+1)))
    for i in range(n+1):
        for j in range(lambda_+1):
            phi[i+j,:] += c[i,:] * f[0,j]
            psi[i+j,:] += c[i,:] * h[0,j]
    phi %= tp
    psi %= tp

    # 4. Polynomials
    Ephi = np.random.randint(0, tp-1, size=(1, n+lambda_-1))
    Epsi = np.random.randint(0, tp-1, size=(1, n+lambda_-1))

    # 5.
    R0 = np.random.randint(1, (tp-2)//2, size=(1,)) * 2
    Rn = np.random.randint(1, (tp-2)//2, size=(1,)) * 2

    # 6. Noise functions
    N0 = np.mod(R0 * c[0,:], tp)
    Nn = np.mod(Rn * c[n,:], tp)

    # 7.
    Phi = phi[1:n+lambda_, :]
    Psi = psi[1:n+lambda_, :]

    # 8.
    P = np.zeros((n+lambda_-1, (ell[0]+1)*(ell[1]+1)))
    Q = np.zeros((n+lambda_-1, (ell[0]+1)*(ell[1]+1)))
    for i in range(n+lambda_-1):
        P[i,:] = R0 * np.concatenate(([Phi[i,0]-Ephi[0,i]], Phi[i,1:]))
        Q[i,:] = Rn * np.concatenate(([Psi[i,0]-Epsi[0,i]], Psi[i,1:]))
    P %= tp
    Q %= tp

    # Private-key and public-key pair
    s = [f.tolist()[0], h.tolist()[0], R0.tolist()[0], Rn.tolist()[0], Ephi.tolist()[0], Epsi.tolist()[0]]
    v = [P.tolist(), Q.tolist(), N0.tolist(), Nn.tolist()]
    with open('private_key.json', 'w') as f:
        json.dump(s, f)
    with open('public_key.json', 'w') as f:
        json.dump(v, f)
    return s, v

#f.write(','.join(str(s) if isinstance(s, int) else ','.join(str(i) for i in key) for key in keys))
# End the timer
end_time = time.time()

# Calculate the signing latency in milliseconds
latency = (end_time - start_time) * 1000

# Print the signing latency in milliseconds
print('keygenlatency:', latency, 'milliseconds')

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
    s, v = keygen(m, n, lambda_, ell, p)
    print("Private Key: ", s)
    print("Public Key: ", v)
  #  t = S(s, mu, m, n, lambda_, ell, p)
   #1 print(t)
  #  verify = V(v, mu, t, m, n, lambda_, ell, p)
    
    
if __name__ == '__main__':
    main()

















