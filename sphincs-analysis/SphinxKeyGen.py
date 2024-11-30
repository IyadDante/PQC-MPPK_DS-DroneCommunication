#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 23, 2023

@author: atinder
@editor: mohammed
"""
import pyspx.shake_128f as sphincs
import os, binascii
import random
import hashlib
import numpy as np
import math
import time
import cProfile
import json

# Key generation: private + public key
def main():
    # Key generation: private + public key
	seed = os.urandom(sphincs.crypto_sign_SEEDBYTES)
	public_key, secret_key = sphincs.generate_keypair(seed)
	#print("Public key:", binascii.hexlify(public_key))
	#print("Private key:", binascii.hexlify(secret_key))

	with open('SphincsPublicKey.json', 'w') as f:
	   json.dump(binascii.hexlify(public_key).decode('ascii'), f)

	with open('SphincsPrivateKey.json', 'w') as f:
	   json.dump(binascii.hexlify(secret_key).decode('ascii'), f)

if __name__ == '__main__':
    main()
    
    
