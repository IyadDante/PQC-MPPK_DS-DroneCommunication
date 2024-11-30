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

with open('/Users/atinder/Desktop/original_text2.txt', 'rb') as f:
    data = f.read()
    hash_object1 = hashlib.sha256(data)
    print("hash_value:", hash_object1.hexdigest())
    mu1 = int(hash_object1.hexdigest(), 16)
    print ("Int_value_msg1:", mu1)
    
with open('/Users/atinder/Desktop/original_text2.txt', 'rb') as f:
    data = f.read()
    hash_object2 = hashlib.sha256(data)
    print("hash_value:", hash_object2.hexdigest())
    mu2 = int(hash_object2.hexdigest(), 16)
    print ("Int_value_msg1:", mu2)
    


def keygen(m, n, lambda_, ell, p1, p2):
    tp1 = p1 - 1
    tp2 = p2 - 1

    # 1. Base Polynomial
    c1 = np.random.randint(0, tp1-1, size=(n+1, (ell[0]+1)*(ell[1]+1)))
    c2 = np.random.randint(0, tp2-1, size=(n+1, (ell[0]+1)*(ell[1]+1)))
    
    # 2. Univariate polynomials
    f11 = np.random.randint(0, tp1-1, size=(1, lambda_+1))
    f12 = np.random.randint(0, tp1-1, size=(1, lambda_+1))
    f21 = np.random.randint(0, tp2-1, size=(1, lambda_+1))
    f22 = np.random.randint(0, tp2-1, size=(1, lambda_+1))
    #h = np.random.randint(0, tp-1, size=(1, lambda_+1))

    # 3. Product polynomials
    phi11 = np.zeros((n+lambda_+1, (ell[0]+1)*(ell[1]+1)))
    phi12 = np.zeros((n+lambda_+1, (ell[0]+1)*(ell[1]+1)))
    phi21 = np.zeros((n+lambda_+1, (ell[0]+1)*(ell[1]+1)))
    phi22 = np.zeros((n+lambda_+1, (ell[0]+1)*(ell[1]+1)))
    #psi = np.zeros((n+lambda_+1, (ell[0]+1)*(ell[1]+1)))
    for i in range(n+1):
        for j in range(lambda_+1):
            phi11[i+j,:] += c1[i,:] * f11[0,j]
            phi12[i+j,:] += c1[i,:] * f12[0,j]
            phi21[i+j,:] += c2[i,:] * f21[0,j]
            phi22[i+j,:] += c2[i,:] * f22[0,j]
            #psi[i+j,:] += c[i,:] * h[0,j]
    phi11 %= tp1
    phi12 %= tp1
    phi21 %= tp2
    phi22 %= tp2
    #psi %= tp

    # 4. Polynomials
    E11 = np.random.randint(0, tp1-1, size=(1, n+lambda_-1))
    E12 = np.random.randint(0, tp1-1, size=(1, n+lambda_-1))
    E21 = np.random.randint(0, tp2-1, size=(1, n+lambda_-1))
    E22 = np.random.randint(0, tp2-1, size=(1, n+lambda_-1))
    #Epsi = np.random.randint(0, tp-1, size=(1, n+lambda_-1))

    # 5.
    R11 = np.random.randint(1, (tp1-2)//2, size=(1,)) * 2
    R12 = np.random.randint(1, (tp1-2)//2, size=(1,)) * 2
    R21 = np.random.randint(1, (tp2-2)//2, size=(1,)) * 2
    R22 = np.random.randint(1, (tp2-2)//2, size=(1,)) * 2
    #Rn = np.random.randint(1, (tp-2)//2, size=(1,)) * 2

    # 6. Noise functions
    N11 = np.mod(R11 * c1[0,:], tp1)
    N12 = np.mod(R12 * c1[0,:], tp1)
    N21 = np.mod(R21 * c2[0,:], tp2)
    N22 = np.mod(R22 * c2[0,:], tp2)
   # Nn = np.mod(Rn * c[n,:], tp)

    # 7.
    Phi11 = phi11[1:n+lambda_, :]
    Phi12 = phi12[1:n+lambda_, :]
    Phi21 = phi21[1:n+lambda_, :]
    Phi22 = phi22[1:n+lambda_, :]
    #Psi = psi[1:n+lambda_, :]

    # 8.
    P11 = np.zeros((n+lambda_-1, (ell[0]+1)*(ell[1]+1)))
    P12 = np.zeros((n+lambda_-1, (ell[0]+1)*(ell[1]+1)))
    P21 = np.zeros((n+lambda_-1, (ell[0]+1)*(ell[1]+1)))
    P22 = np.zeros((n+lambda_-1, (ell[0]+1)*(ell[1]+1)))
    #Q = np.zeros((n+lambda_-1, (ell[0]+1)*(ell[1]+1)))
    for i in range(n+lambda_-1):
        P11[i,:] = R11 * np.concatenate(([Phi11[i,0]-E11[0,i]], Phi11[i,1:]))
        P12[i,:] = R12 * np.concatenate(([Phi12[i,0]-E12[0,i]], Phi12[i,1:]))
        P21[i,:] = R21 * np.concatenate(([Phi21[i,0]-E21[0,i]], Phi21[i,1:]))
        P22[i,:] = R22 * np.concatenate(([Phi22[i,0]-E12[0,i]], Phi22[i,1:]))
        #Q[i,:] = Rn * np.concatenate(([Psi[i,0]-Epsi[0,i]], Psi[i,1:]))
    P11 %= tp1
    P12 %= tp1
    P21 %= tp2
    P22 %= tp2
    #Q %= tp

    # Private-key and public-key pair
    s1 = [f11.tolist()[0], f12.tolist()[0], R11.tolist()[0], R12.tolist()[0], E11.tolist()[0], E12.tolist()[0]]
    v1 = [P11.tolist(), P12.tolist(), N11.tolist(), N12.tolist()]
    s2 = [f21.tolist()[0], f22.tolist()[0], R21.tolist()[0], R22.tolist()[0], E21.tolist()[0], E22.tolist()[0]]
    v2 = [P21.tolist(), P22.tolist(), N21.tolist(), N22.tolist()]
    return s1, v1, s2, v2


def S(s1, mu1, s2, mu2, m, n, lambda_, ell, p1,p2):
    
    f11 = np.array(s1[0])
    f12 = np.array(s1[1])
    #h = np.array(s[1])
    R11 = np.array(s1[2]) 
    R12 = np.array(s1[3])
    #Rn = np.array(s[3])
    E11 = np.array(s1[4])
    E12 = np.array(s1[5])
    #Epsi = np.array(s[5])
    
    #twin
    
    f21 = np.array(s2[0])
    f22 = np.array(s2[1])
    #h = np.array(s[1])
    R21 = np.array(s2[2]) 
    R22 = np.array(s2[3])
    #Rn = np.array(s[3])
    E21 = np.array(s2[4])
    E22 = np.array(s2[5])
    #Epsi = np.array(s[5])
    
    tp1 = p1 - 1
    tp2 = p2 - 1
    # Random base
    g1 = np.random.randint(2, tp1-1)
    g2 = np.random.randint(2, tp2-1)
    
    # Evaluate on μ
    f11m = np.polyval(np.flip(f11), mu1)
    a1 = np.mod(R11*f11m, tp1)
    A1 = powermod(g1, a1, p1)
    #twin
    f21m = np.polyval(np.flip(f21), mu2)
    a2 = np.mod(R21*f21m, tp2)
    A2 = powermod(g2, a2, p2)
    
    # Evaluate on μ
    f12m = np.polyval(np.flip(f12), mu1)
    b1 = np.mod(R12*f12m, tp1)
    B1 = powermod(g1, b1, p1)
    
    c1 = np.mod(R12 * (f12m*f11[0] - f11m*f12[0]), tp1)
    C1 = powermod(g1, c1, p1)
    
    d1 = np.mod(R11 * (f12m*f11[lambda_] - f11m*f12[lambda_]), tp1)
    D1 = powermod(g1, d1, p1)
    
    #twin
    
    f22m = np.polyval(np.flip(f22), mu2)
    b2 = np.mod(R22*f22m, tp2)
    B2 = powermod(g2, b2, p2)
    
    c2 = np.mod(R22 * (f22m*f21[0] - f21m*f22[0]), tp2)
    C2 = powermod(g2, c2, p2)
    
    d2 = np.mod(R21 * (f22m*f21[lambda_] - f21m*f22[lambda_]), tp2)
    D2 = powermod(g2, d2, p2)
    
    # Evaluate on μ
    Ephi11m = np.polyval(np.hstack([np.flip(E11), 0]), mu1)
    Ephi11m = np.mod(Ephi11m, tp1)
    #twin 
    Ephi21m = np.polyval(np.hstack([np.flip(E21), 0]), mu2)
    Ephi21m = np.mod(Ephi21m, tp2)
    
    # Evaluate on μ
    Ephi12m = np.polyval(np.hstack([np.flip(E12), 0]), mu1)
    Ephi12m = np.mod(Ephi12m, tp1)
    
    e1 = np.mod(R11*R12*(f12m*Ephi11m - f11m*Ephi12m), tp1)
    E1 = powermod(g1, e1, p1)
    
    # Digital signature
    t1 = [A1, B1, C1, D1, E1]

    #twin
    # Evaluate on μ
    Ephi22m = np.polyval(np.hstack([np.flip(E22), 0]), mu2)
    Ephi22m = np.mod(Ephi22m, tp2)
    
    e2 = np.mod(R21*R22*(f22m*Ephi21m - f21m*Ephi22m), tp2)
    E2 = powermod(g2, e2, p2)
    
    # Digital signature
    t2 = [A2, B2, C2, D2, E2]
    
    return t1, t2

def V(v1, mu1, t1, v2, mu2, t2, m, n, lambda_, ell, p1, p2):
    # v = public key
    P11 = np.array(v1[0]); 
    P12 = np.array(v1[1]); 
    #Q = np.array(v[1]); 
    N11 = np.array(v1[2]); 
    N12 = np.array(v1[3]); 
    
    P21 = np.array(v2[0]);
    P22 = np.array(v2[1]);
    
    N21 = np.array(v2[2]); 
    N22 = np.array(v2[3]); 
   # Nn = np.array(v[3])
    
    A1 = t1[0]; B1 = t1[1]; C1 = t1[2]; D1 = t1[3]; E1 = t1[4];
    A2 = t2[0]; B2 = t2[1]; C2 = t2[2]; D2 = t2[3]; E2 = t2[4];
    tp1 = p1 - 1  # Euler's totient of p
    tp2 = p2 - 1 
    # Noise variables
    r1 = np.random.randint(1, tp1-1, size=m)
    r2 = np.random.randint(1, tp2-1, size=m)
    # r = [2 2]
    
    # Evaluate P, Q, N0, and Nn
    barP11 = 0; barP12 = 0; barP21 = 0; barP22 = 0;
    for i in range(1, n+lambda_):
        for j1 in range(0, ell[0]+1):
            for j2 in range(0, ell[1]+1):
                barP11 = (barP11 + P11[i-1, j1*2+j2]*powermod(r1[0], j1, tp1)*powermod(r1[1], j2, tp1)*powermod(mu1, i, tp1)) % tp1
                #barQ = (barQ + Q[i-1, j1*2+j2]*powermod(r[0], j1, tp)*powermod(r[1], j2, tp)*powermod(mu, i, tp)) % tp
                #barP12 = (barP12 + P12[j1*2+j2]*(r1[0]**j1)*(r1[1]**j2)*(mu1**i)) % tp1
                barP12 = (barP12 + P12[i-1, j1*2+j2]*powermod(r1[0], j1, tp1)*powermod(r1[1], j2, tp1)*powermod(mu1, i, tp1)) % tp1
                barP21 = (barP21 + P21[i-1, j1*2+j2]*powermod(r2[0], j1, tp2)*powermod(r2[1], j2, tp2)*powermod(mu2, i, tp2)) % tp2
                barP22 = (barP22 + P22[i-1, j1*2+j2]*powermod(r2[0], j1, tp2)*powermod(r2[1], j2, tp2)*powermod(mu2, i, tp2)) % tp2
    
    barP11 %= tp1
    barP12 %= tp1
    barP21 %= tp2
    barP22 %= tp2
   
    barN11 = 0; barN12 = 0 ;barN21 = 0; barN22 = 0
    
    for j1 in range(0, ell[0]+1):
        for j2 in range(0, ell[1]+1):
            barN11 = (barN11 + N11[j1*2+j2]*powermod(r1[0], j1, tp1)*powermod(r1[1], j2, tp1)) % tp1
            barN12 = (barN12 + N12[j1*2+j2]*powermod(r1[0], j1, tp1)*powermod(r1[1], j2, tp1)) % tp1
            barN21 = (barN21 + N21[j1*2+j2]*powermod(r2[0], j1, tp2)*powermod(r2[1], j2, tp2)) % tp2
            barN22 = (barN22 + N22[j1*2+j2]*powermod(r2[0], j1, tp2)*powermod(r2[1], j2, tp2)) % tp2
            #barNn = (barNn + Nn[j1*2+j2]*powermod(r[0], j1, tp)*powermod(r[1], j2, tp)) % tp
    
    barN11 %= tp1
    barN12 = (barN12 * pow(mu1, n+lambda_, tp1)) % tp1
    barN21 %= tp2
    barN22 = (barN22 * pow(mu2, n+lambda_, tp2)) % tp2
    
    # Verification
    left1 = powermod(A1, barP12, p1)
    right1 = (powermod(B1, barP11, p1) * powermod(C1, barN11, p1) * powermod(D1, barN12, p1) * E1) % p1
    
    left2 = powermod(A2, barP22, p2)
    right2 = (powermod(B2, barP21, p2) * powermod(C2, barN21, p2) * powermod(D2, barN22, p2) * E2) % p2
    
    if left1 == right1 and left2 == right2:
        verdict = 'VALID'
    else:
        verdict = 'INVALID'
    
    verify1 = {
        "left1": left1,
        "right1": right1
        }
    
    print("left1: ", verify1["left1"])
    print("right1: ", verify1["right1"])
    
    verify2 = {
        "left2": left2,
        "right2": right2
        }
    
    print("left2: ", verify2["left2"])
    print("right2: ", verify2["right2"])
    
    print("verdict says that this encryption is: " , verdict)
    
    return verify1, verify2
    

def main():
    # Twin Primes
    p1 = 19
    p2 = 17
    # Euler's totient of twin primes p1 & p2
    tp1 = p1 - 1
    tp2 = p2 - 1
    # number of noise variables
    m = 2
    # degree of base polynomial
    n = 2
    # degree of multiplier polynomials
    lambda_ = 1 # linear
    # upper limits
    ell = [1,1]
    #mu1 = random.randint(0, p1-1)
    #mu2 = random.randint(0, p2-1)
    # Key generation
    s1, v1, s2, v2 = keygen(m, n, lambda_, ell, p1, p2)
    print("Private Key1: ", s1)
    print("Public Key1: ", v1)
    print("Private Key2: ", s2)
    print("Public Key2: ", v2)
    t1, t2 = S(s1, mu1, s2, mu2, m, n, lambda_, ell, p1,p2)
    print(t1)
    print(t2)
    verify1, verify2 = V(v1, mu1, t1, v2, mu2, t2, m, n, lambda_, ell, p1, p2)
    
    
if __name__ == '__main__':
    main()