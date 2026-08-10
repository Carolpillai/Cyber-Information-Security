import tkinter as tk
from tkinter import messagebox, scrolledtext
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

BG = "#ffe4ec"
PANEL = "#ffc2d9"
BTN = "#ff85a2"
BTN_HOVER = "#ff5c8a"
TEXT = "#5c1a33"
GREEN = "#2e7d32"
RED = "#c62828"

BOX_WIDTH = 62
LABEL_FONT = ("Segoe UI", 10, "bold")
BOX_FONT = ("Consolas", 9)

def generate_keys():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_bytes = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("private.pem", "wb") as f:
        f.write(private_bytes)
    with open("public.pem", "wb") as f:
        f.write(public_bytes)
    messagebox.showinfo("Keys Generated", "private.pem and public.pem created")

def sign_message():
    message = sign_msg_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("Missing Input", "Enter a message to sign")
        return
    try:
        with open("private.pem", "rb") as f:
            key = serialization.load_pem_private_key(f.read(), password=None)
        digest = hashlib.sha256(message.encode()).digest()
        signature = key.sign(
            digest,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        with open("signature.bin", "wb") as f:
            f.write(signature)
        with open("original_message.txt", "w") as f:
            f.write(message)

        original_box.config(state="normal")
        original_box.delete("1.0", tk.END)
        original_box.insert(tk.END, message)
        original_box.config(state="disabled")

        signature_box.config(state="normal")
        signature_box.delete("1.0", tk.END)
        signature_box.insert(tk.END, signature.hex())
        signature_box.config(state="disabled")

        sign_status.config(text="Status: SIGNED", fg=TEXT)
    except FileNotFoundError:
        messagebox.showerror("Error", "Generate keys first")

def find_tamper_position(original, current):
    min_len = min(len(original), len(current))
    for i in range(min_len):
        if original[i] != current[i]:
            return i
    if len(original) != len(current):
        return min_len
    return -1

def verify_message():
    message = verify_msg_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("Missing Input", "Enter a message to verify")
        return
    try:
        with open("public.pem", "rb") as f:
            key = serialization.load_pem_public_key(f.read())
        with open("signature.bin", "rb") as f:
            signature = f.read()
        digest = hashlib.sha256(message.encode()).digest()

        try:
            with open("original_message.txt", "r") as f:
                original = f.read()
        except FileNotFoundError:
            original = None

        compare_box.config(state="normal")
        compare_box.delete("1.0", tk.END)
        if original is not None:
            compare_box.insert(tk.END, f"Original : {original}\n")
            compare_box.insert(tk.END, f"Received : {message}\n")

        try:
            key.verify(
                signature,
                digest,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            verify_status.config(text="Status: VALID", fg=GREEN)
            if original is not None:
                compare_box.insert(tk.END, "\nNo tampering detected — message matches original")
        except InvalidSignature:
            verify_status.config(text="Status: INVALID", fg=RED)
            if original is not None:
                pos = find_tamper_position(original, message)
                if pos == -1:
                    compare_box.insert(tk.END, "\nText identical but signature mismatch — key or signature file changed")
                else:
                    compare_box.insert(tk.END, f"\nTampering detected at character position {pos}")

        compare_box.config(state="disabled")
    except FileNotFoundError:
        messagebox.showerror("Error", "Sign a message first")

root = tk.Tk()
root.title("RSA Digital Signature")
root.geometry("620x900")
root.configure(bg=BG)

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=20, pady=15)

tk.Label(main, text="RSA Digital Signature Tool", bg=BG, fg=TEXT,
         font=("Segoe UI", 16, "bold")).pack(pady=(0, 12))

tk.Button(main, text="Generate Keys", command=generate_keys, bg=BTN, fg="white",
          activebackground=BTN_HOVER, font=("Segoe UI", 11, "bold"),
          relief="flat", padx=10, pady=8, width=22).pack(pady=(0, 15))

sep1 = tk.Frame(main, bg=BTN, height=2)
sep1.pack(fill="x", pady=10)

tk.Label(main, text="SIGN", bg=BG, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(anchor="w")

tk.Label(main, text="Message to Sign", bg=BG, fg=TEXT, font=LABEL_FONT).pack(anchor="w", pady=(8, 2))
sign_msg_entry = tk.Text(main, height=3, width=BOX_WIDTH, bg=PANEL, fg=TEXT, font=BOX_FONT, relief="flat")
sign_msg_entry.pack(fill="x")

tk.Button(main, text="Sign", command=sign_message, bg=BTN, fg="white",
          activebackground=BTN_HOVER, font=("Segoe UI", 11, "bold"),
          relief="flat", padx=20, pady=8, width=22).pack(pady=10)

tk.Label(main, text="Original Message (stored)", bg=BG, fg=TEXT, font=LABEL_FONT).pack(anchor="w", pady=(4, 2))
original_box = tk.Text(main, height=2, width=BOX_WIDTH, bg=PANEL, fg=TEXT, font=BOX_FONT, relief="flat", state="disabled")
original_box.pack(fill="x")

tk.Label(main, text="Signature", bg=BG, fg=TEXT, font=LABEL_FONT).pack(anchor="w", pady=(8, 2))
signature_box = scrolledtext.ScrolledText(main, height=4, width=BOX_WIDTH, bg=PANEL, fg=TEXT, font=BOX_FONT, relief="flat", state="disabled")
signature_box.pack(fill="x")

sign_status = tk.Label(main, text="Status: —", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold"))
sign_status.pack(anchor="w", pady=(6, 0))

sep2 = tk.Frame(main, bg=BTN, height=2)
sep2.pack(fill="x", pady=15)

tk.Label(main, text="VERIFY", bg=BG, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(anchor="w")

tk.Label(main, text="Message to Verify", bg=BG, fg=TEXT, font=LABEL_FONT).pack(anchor="w", pady=(8, 2))
verify_msg_entry = tk.Text(main, height=3, width=BOX_WIDTH, bg=PANEL, fg=TEXT, font=BOX_FONT, relief="flat")
verify_msg_entry.pack(fill="x")

tk.Button(main, text="Verify", command=verify_message, bg=BTN, fg="white",
          activebackground=BTN_HOVER, font=("Segoe UI", 11, "bold"),
          relief="flat", padx=20, pady=8, width=22).pack(pady=10)

tk.Label(main, text="Original vs Received", bg=BG, fg=TEXT, font=LABEL_FONT).pack(anchor="w", pady=(4, 2))
compare_box = scrolledtext.ScrolledText(main, height=5, width=BOX_WIDTH, bg=PANEL, fg=TEXT, font=BOX_FONT, relief="flat", state="disabled")
compare_box.pack(fill="x")

verify_status = tk.Label(main, text="Status: —", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold"))
verify_status.pack(anchor="w", pady=(6, 0))

root.mainloop()
