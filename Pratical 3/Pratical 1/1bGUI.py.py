import tkinter as tk
from tkinter import messagebox

def key_order(key):
    return sorted(range(len(key)), key=lambda i: key[i])

def encrypt(text, key):
    cols = len(key)
    rows = -(-len(text) // cols)
    padded = text.ljust(rows * cols, "X")
    grid = [padded[r * cols:(r + 1) * cols] for r in range(rows)]
    order = key_order(key)
    result = ""
    for i in order:
        for row in grid:
            result += row[i]
    return result

def decrypt(text, key):
    cols = len(key)
    rows = len(text) // cols
    order = key_order(key)
    grid = [["" for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for i in order:
        for r in range(rows):
            grid[r][i] = text[idx]
            idx += 1
    return "".join("".join(row) for row in grid)

def do_encrypt():
    if not key_var.get():
        messagebox.showerror("Error", "Key required")
        return
    out.set(encrypt(text_var.get(), key_var.get()))

def do_decrypt():
    if not key_var.get():
        messagebox.showerror("Error", "Key required")
        return
    out.set(decrypt(text_var.get(), key_var.get()))

root = tk.Tk()
root.title("Transposition Cipher (Columnar) - GUI")

text_var = tk.StringVar()
key_var = tk.StringVar(value="CIPHER")
out = tk.StringVar()

tk.Label(root, text="Text").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=text_var, width=40).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Key").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=key_var, width=20).grid(row=1, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Encrypt", command=do_encrypt).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Decrypt", command=do_decrypt).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Result").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=out, width=40, state="readonly").grid(row=3, column=1, padx=5, pady=5)

root.mainloop()