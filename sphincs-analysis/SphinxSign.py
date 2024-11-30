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
import sys

def main():

	with open(sys.argv[1] , 'rb') as f:
	   data = f.read()
	   message = hashlib.sha256(data)
	   hashValue = message.hexdigest()
	   
	with open(sys.argv[1][:-4] + "_HashValue.json", 'w') as f:
	   json.dump(hashValue, f)
	   
	#Signing 
	with open('SphincsPrivateKey.json', 'r') as f:
	   secret_key = json.load(f)
	#Convert the secret key from a string of hexadecimal digits to bytes
	secret_key = binascii.unhexlify(secret_key)
	#Convert the hashvalue to bytes
	signature = sphincs.sign(binascii.unhexlify(hashValue), secret_key)
	
	with open(sys.argv[1][:-4] + "_DigSig.json", 'w') as f:
	   json.dump(binascii.hexlify(signature).decode('ascii'), f)
    
    
if __name__ == '__main__':
    main()
