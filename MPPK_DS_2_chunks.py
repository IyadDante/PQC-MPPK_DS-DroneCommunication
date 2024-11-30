#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 18:47:57 2023

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

with open('/Users/atinder/Desktop/original_text2.txt', 'rb') as f:
    # Find the size of the input file
    f.seek(0, 2)
    file_size = f.tell()
    f.seek(0)
    # Divide the file into two chunks
    chunk_size = file_size // 2
    # Read the first chunk
    data = f.read(chunk_size)
    # Hash the first chunk using SHA-256 algorithm
    hash_object1 = hashlib.sha256(data)
    # Read the second chunk
    data = f.read()
    # Hash the second chunk using SHA-256 algorithm
    hash_object2 = hashlib.sha256(data)
print("hash_value_chunk_1:", hash_object1.hexdigest())
print("hash_value_chunk_2:",hash_object2.hexdigest())

# Convert the hashed values to base 36 integers
m_u_chunk1=int(hash_object1.hexdigest(), 16)
m_u_chunk2=int(hash_object2.hexdigest(), 16)

base_36_chunks=[m_u_chunk1,m_u_chunk2]

print("Int_value_chunks:",base_36_chunks)

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

    return s, v


def S(s, mu, m, n, lambda_, ell, p):
    
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
    
    print("Digital Signature: ", t)
    
    return t 

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
    p = 257
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
    mu = random.randint(0, p-1)
    # Key generation
    s, v = keygen(m, n, lambda_, ell, p)
    print("Private Key: ", s)
    print("Public Key: ", v)
    #t = S(s, mu, m, n, lambda_, ell, p)
    for chunk in base_36_chunks:
        t = S(s, chunk, m, n, lambda_, ell, p)
        verify = V(v, chunk, t, m, n, lambda_, ell, p)
        
    
    
    
    
if __name__ == '__main__':
    main()