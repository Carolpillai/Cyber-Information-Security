import tkinter as tk
from tkinter import messagebox, scrolledtext

BG = "#ffe4ec"
PANEL = "#ffc2d9"
BTN = "#ff85a2"
BTN_HOVER = "#ff5c8a"
TEXT = "#5c1a33"
GREEN = "#2e7d32"
RED = "#c62828"

LABEL_FONT = ("Segoe UI", 10, "bold")
BOX_FONT = ("Consolas", 9)

def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

def compute():
    try:
        p = int(p_entry.get())
        g = int(g_entry.get())
        a_private = int(a_entry.get())
        b_private = int(b_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Enter valid integers for p, g, a, and b")
        return

    A = mod_exp(g, a_private, p)
    B = mod_exp(g, b_private, p)
    secret_A = mod_exp(B, a_private, p)
    secret_B = mod_exp(A, b_private, p)

    output.config(state="normal")
    output.delete("1.0", tk.END)

    output.insert(tk.END, "=== Step 1: Public Key Generation ===\n")
    output.insert(tk.END, f"Entity A: A = g^a mod p = {g}^{a_private} mod {p} = {A}\n")
    output.insert(tk.END, f"Entity B: B = g^b mod p = {g}^{b_private} mod {p} = {B}\n\n")

    output.insert(tk.END, "=== Step 2: Public Key Exchange ===\n")
    output.insert(tk.END, f"A sends A = {A} to B\n")
    output.insert(tk.END, f"B sends B = {B} to A\n")
    output.insert(tk.END, "Eavesdropper sees only: p, g, A, B\n\n")

    output.insert(tk.END, "=== Step 3: Shared Secret Computation ===\n")
    output.insert(tk.END, f"Entity A: S = B^a mod p = {B}^{a_private} mod {p} = {secret_A}\n")
    output.insert(tk.END, f"Entity B: S = A^b mod p = {A}^{b_private} mod {p} = {secret_B}\n\n")

    output.insert(tk.END, "=== Step 4: Verification ===\n")
    if secret_A == secret_B:
        output.insert(tk.END, "Shared secrets MATCH — key exchange successful\n", "match")
        output.insert(tk.END, f"Shared Secret Key = {secret_A}\n\n", "match")
        status.config(text="Status: SUCCESS", fg=GREEN)
    else:
        output.insert(tk.END, "Shared secrets DO NOT MATCH — key exchange failed\n", "mismatch")
        status.config(text="Status: FAILED", fg=RED)

    output.insert(tk.END, "=== Summary ===\n")
    output.insert(tk.END, f"Public parameters : p = {p}, g = {g}\n")
    output.insert(tk.END, f"Entity A private = {a_private}, public = {A}\n")
    output.insert(tk.END, f"Entity B private = {b_private}, public = {B}\n")
    output.insert(tk.END, f"Final shared key  = {secret_A if secret_A == secret_B else 'MISMATCH'}\n")

    output.tag_config("match", foreground=GREEN, font=("Consolas", 9, "bold"))
    output.tag_config("mismatch", foreground=RED, font=("Consolas", 9, "bold"))
    output.config(state="disabled")

root = tk.Tk()
root.title("Diffie-Hellman Key Exchange")
root.geometry("620x760")
root.configure(bg=BG)

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=20, pady=15)

tk.Label(main, text="Diffie-Hellman Key Exchange", bg=BG, fg=TEXT,
         font=("Segoe UI", 16, "bold")).pack(pady=(0, 15))

form = tk.Frame(main, bg=BG)
form.pack(fill="x", pady=(0, 10))

def add_field(parent, label_text, row):
    tk.Label(parent, text=label_text, bg=BG, fg=TEXT, font=LABEL_FONT).grid(row=row, column=0, sticky="w", pady=6)
    entry = tk.Entry(parent, bg=PANEL, fg=TEXT, font=BOX_FONT, relief="flat", width=25)
    entry.grid(row=row, column=1, padx=10, pady=6)
    return entry

p_entry = add_field(form, "Prime (p):", 0)
g_entry = add_field(form, "Generator (g):", 1)
a_entry = add_field(form, "Entity A private key (a):", 2)
b_entry = add_field(form, "Entity B private key (b):", 3)

tk.Button(main, text="Compute Key Exchange", command=compute, bg=BTN, fg="white",
          activebackground=BTN_HOVER, font=("Segoe UI", 11, "bold"),
          relief="flat", padx=10, pady=8, width=26).pack(pady=15)

tk.Label(main, text="Detailed Output", bg=BG, fg=TEXT, font=LABEL_FONT).pack(anchor="w", pady=(0, 4))
output = scrolledtext.ScrolledText(main, height=20, width=68, bg=PANEL, fg=TEXT, font=BOX_FONT, relief="flat", state="disabled")
output.pack(fill="both", expand=True)

status = tk.Label(main, text="Status: —", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold"))
status.pack(anchor="w", pady=(8, 0))

root.mainloop()
