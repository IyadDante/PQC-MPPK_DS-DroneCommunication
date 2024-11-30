import hashlib
import numpy as np
import json
import random

def powermod(base, exponent, modulus):
    """Calculate (base ^ exponent) % modulus efficiently."""
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


def sign_message(message):
    """
    Sign a given message using the MPPK algorithm.
    :param message: The message to be signed (string).
    :return: Digital signature as a list.
    """
    # Finite Field index
    p = 19  # Ensure p is defined before using it
    tp = p - 1
    m = 2
    n = 2
    lambda_ = 1  # Linear
    ell = [1, 1]

    # Hash the message
    hash_object = hashlib.sha256(message.encode())
    print("Hash value:", hash_object.hexdigest())
    mu = int(hash_object.hexdigest(), 16)

    # Reduce `mu` to fit within the field size
    mu = mu % p  # Scale down to field size

    print("Int value of message (reduced):", mu)

    # Load private key
    with open('private_key.json', 'r') as f:
        s = json.load(f)

    f = np.array(s[0])
    h = np.array(s[1])
    R0 = np.array(s[2])
    Rn = np.array(s[3])
    Ephi = np.array(s[4])
    Epsi = np.array(s[5])

    # Random base
    g = np.random.randint(2, tp - 1)

    fm = np.polyval(np.flip(f), mu)
    a = np.mod(R0 * fm, tp)
    A = powermod(g, a, p)

    hm = np.polyval(np.flip(h), mu)
    b = np.mod(Rn * hm, tp)
    B = powermod(g, b, p)

    c = np.mod(Rn * (hm * f[0] - fm * h[0]), tp)
    C = powermod(g, c, p)

    d = np.mod(R0 * (hm * f[lambda_] - fm * h[lambda_]), tp)
    D = powermod(g, d, p)

    Ephim = np.polyval(np.hstack([np.flip(Ephi), 0]), mu)
    Ephim = np.mod(Ephim, tp)

    Epsim = np.polyval(np.hstack([np.flip(Epsi), 0]), mu)
    Epsim = np.mod(Epsim, tp)

    e = np.mod(R0 * Rn * (hm * Ephim - fm * Epsim), tp)
    E = powermod(g, e, p)

    # Digital signature
    t = [A, B, C, D, E]

    return t



if __name__ == "__main__":
    # Example usage
    message = "Example telemetry data"
    signature = sign_message(message)
    print("Digital Signature:", signature)
