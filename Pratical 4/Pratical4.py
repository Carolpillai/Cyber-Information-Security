import sys
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

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
    print("Keys generated: private.pem, public.pem")

def sign(message):
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

    print("Message   :", message)
    print("SHA256    :", digest.hex())
    print("Signature :", signature.hex())
    print("Status    : SIGNED")

def verify(message):
    with open("public.pem", "rb") as f:
        key = serialization.load_pem_public_key(f.read())

    digest = hashlib.sha256(message.encode()).digest()

    with open("signature.bin", "rb") as f:
        signature = f.read()

    print("Message   :", message)
    print("SHA256    :", digest.hex())
    print("Signature :", signature.hex())

    try:
        key.verify(
            signature,
            digest,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("Status    : VALID")
    except InvalidSignature:
        print("Status    : INVALID")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rsa_signature_cli.py [genkeys|sign|verify] [message]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "genkeys":
        generate_keys()
    elif action == "sign":
        sign(sys.argv[2])
    elif action == "verify":
        verify(sys.argv[2])
    else:
        print("Invalid action")
