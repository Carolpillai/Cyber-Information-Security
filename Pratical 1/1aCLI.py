import sys

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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python 1A_substitution_cli.py [encrypt|decrypt] <text> <shift>")
    else:
        mode, text, shift = sys.argv[1], sys.argv[2], int(sys.argv[3])
        if mode == "encrypt":
            print(encrypt(text, shift))
        elif mode == "decrypt":
            print(decrypt(text, shift))
        else:
            print("Invalid mode")
