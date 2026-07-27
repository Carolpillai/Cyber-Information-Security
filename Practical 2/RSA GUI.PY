import tkinter as tk
from tkinter import messagebox
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

def do_genkeys():
    n, e, d = generate_keys(int(bits_var.get()))
    n_var.set(str(n))
    e_var.set(str(e))
    d_var.set(str(d))

def do_encrypt():
    try:
        cipher = encrypt(msg_var.get(), int(e_var.get()), int(n_var.get()))
        cipher_var.set(str(cipher))
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

def do_decrypt():
    try:
        plain = decrypt(int(cipher_var.get()), int(d_var.get()), int(n_var.get()))
        result_var.set(plain)
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

root = tk.Tk()
root.title("RSA - GUI")

bits_var = tk.StringVar(value="512")
n_var = tk.StringVar()
e_var = tk.StringVar()
d_var = tk.StringVar()
msg_var = tk.StringVar()
cipher_var = tk.StringVar()
result_var = tk.StringVar()

tk.Label(root, text="Key size (bits)").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=bits_var, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)
tk.Button(root, text="Generate Keys", command=do_genkeys).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="n").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=n_var, width=60, state="readonly").grid(row=1, column=1, columnspan=2, padx=5, pady=5)

tk.Label(root, text="e").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=e_var, width=60, state="readonly").grid(row=2, column=1, columnspan=2, padx=5, pady=5)

tk.Label(root, text="d").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=d_var, width=60, state="readonly").grid(row=3, column=1, columnspan=2, padx=5, pady=5)

tk.Label(root, text="Message").grid(row=4, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=msg_var, width=40).grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Encrypt", command=do_encrypt).grid(row=4, column=2, padx=5, pady=5)

tk.Label(root, text="Cipher").grid(row=5, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=cipher_var, width=40).grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text="Decrypt", command=do_decrypt).grid(row=5, column=2, padx=5, pady=5)

tk.Label(root, text="Result").grid(row=6, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=result_var, width=40, state="readonly").grid(row=6, column=1, padx=5, pady=5)

root.mainloop()
