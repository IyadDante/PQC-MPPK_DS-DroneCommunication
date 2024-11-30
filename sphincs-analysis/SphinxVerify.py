#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 04:13:06 2023

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


	with open(sys.argv[1], 'r') as f:
	   hashValue = str(json.load(f))
	   #print("mu_int", sys.argv[1]) 


	with open(sys.argv[2], 'r') as f:
	   signature = json.load(f)
	signature = binascii.unhexlify(signature)
	
	with open('SphincsPublicKey.json', 'r') as f:
	   public_key = json.load(f)
	public_key = binascii.unhexlify(public_key)
	
	valid = sphincs.verify(binascii.unhexlify(hashValue), signature, public_key)
	#print("Valid signature?", valid)
    
if __name__ == '__main__':
    main()
