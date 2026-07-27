import sys
import hmac
import hashlib

def generate_mac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_mac(message, key, mac):
    expected = generate_mac(message, key)
    return hmac.compare_digest(expected, mac)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python 2B_mac_cli.py generate <message> <key>")
        print("       python 2B_mac_cli.py verify <message> <key> <mac>")
    else:
        mode = sys.argv[1]
        if mode == "generate":
            message, key = sys.argv[2], sys.argv[3]
            print(generate_mac(message, key))
        elif mode == "verify":
            message, key, mac = sys.argv[2], sys.argv[3], sys.argv[4]
            print("Valid MAC" if verify_mac(message, key, mac) else "Invalid MAC")
        else:
            print("Invalid mode")
