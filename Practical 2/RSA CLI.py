import sys
import random

def is_prime(n, k=20):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gen_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_prime(n):
            return n

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = egcd(b % a, a)
    return g, y - (b // a) * x, x

def modinv(a, m):
    g, x, _ = egcd(a, m)
    return x % m

def generate_keys(bits=512):
    p = gen_prime(bits)
    q = gen_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    return n, e, d

def encrypt(message, e, n):
    m = int.from_bytes(message.encode(), "big")
    if m >= n:
        raise ValueError("Message too large for key size")
    return pow(m, e, n)

def decrypt(cipher, d, n):
    m = pow(cipher, d, n)
    length = (m.bit_length() + 7) // 8
    return m.to_bytes(length, "big").decode()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 3B_rsa_cli.py genkeys <bits>")
        print("       python 3B_rsa_cli.py encrypt <message> <e> <n>")
        print("       python 3B_rsa_cli.py decrypt <cipher> <d> <n>")
    else:
        mode = sys.argv[1]
        if mode == "genkeys":
            bits = int(sys.argv[2]) if len(sys.argv) > 2 else 512
            n, e, d = generate_keys(bits)
            print("n =", n)
            print("e =", e)
            print("d =", d)
        elif mode == "encrypt":
            message, e, n = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
            print(encrypt(message, e, n))
        elif mode == "decrypt":
            cipher, d, n = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
            print(decrypt(cipher, d, n))
        else:
            print("Invalid mode")
