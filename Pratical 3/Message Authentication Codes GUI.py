import tkinter as tk
from tkinter import messagebox
import hmac
import hashlib

def generate_mac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_mac(message, key, mac):
    expected = generate_mac(message, key)
    return hmac.compare_digest(expected, mac)

def do_generate():
    if not msg_var.get() or not key_var.get():
        messagebox.showerror("Error", "Message and key required")
        return
    out.set(generate_mac(msg_var.get(), key_var.get()))

def do_verify():
    if not msg_var.get() or not key_var.get() or not mac_var.get():
        messagebox.showerror("Error", "Message, key and MAC required")
        return
    result = verify_mac(msg_var.get(), key_var.get(), mac_var.get())
    messagebox.showinfo("Result", "Valid MAC" if result else "Invalid MAC")

root = tk.Tk()
root.title("MAC Generator/Verifier - GUI")

msg_var = tk.StringVar()
key_var = tk.StringVar()
mac_var = tk.StringVar()
out = tk.StringVar()

tk.Label(root, text="Message").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=msg_var, width=50).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Key").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=key_var, width=30).grid(row=1, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Generate MAC", command=do_generate).grid(row=2, column=0, padx=5, pady=5)
tk.Label(root, text="Generated MAC").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=out, width=70, state="readonly").grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="MAC to Verify").grid(row=4, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=mac_var, width=70).grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Verify MAC", command=do_verify).grid(row=5, column=0, padx=5, pady=5)

root.mainloop()
