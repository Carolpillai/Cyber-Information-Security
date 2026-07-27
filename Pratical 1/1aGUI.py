import tkinter as tk
from tkinter import messagebox

def encrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isupper():
            result += chr((ord(ch) - 65 + shift) % 26 + 65)
        elif ch.islower():
            result += chr((ord(ch) - 97 + shift) % 26 + 97)
        else:
            result += ch
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def do_encrypt():
    try:
        out.set(encrypt(text_var.get(), int(shift_var.get())))
    except ValueError:
        messagebox.showerror("Error", "Shift must be an integer")

def do_decrypt():
    try:
        out.set(decrypt(text_var.get(), int(shift_var.get())))
    except ValueError:
        messagebox.showerror("Error", "Shift must be an integer")

root = tk.Tk()
root.title("Substitution Cipher (Caesar) - GUI")

text_var = tk.StringVar()
shift_var = tk.StringVar(value="3")
out = tk.StringVar()

tk.Label(root, text="Text").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=text_var, width=40).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Shift").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=shift_var, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Encrypt", command=do_encrypt).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Decrypt", command=do_decrypt).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Result").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=out, width=40, state="readonly").grid(row=3, column=1, padx=5, pady=5)

root.mainloop()
