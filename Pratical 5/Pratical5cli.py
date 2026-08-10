def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

def main():
    print("=== Diffie-Hellman Key Exchange ===\n")

    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a primitive root / generator (g): "))

    print("\n--- Entity A ---")
    a_private = int(input("Enter Entity A's private key (a): "))

    print("\n--- Entity B ---")
    b_private = int(input("Enter Entity B's private key (b): "))

    print("\n=== Step 1: Public Key Generation ===")
    A = mod_exp(g, a_private, p)
    print(f"Entity A computes: A = g^a mod p = {g}^{a_private} mod {p} = {A}")

    B = mod_exp(g, b_private, p)
    print(f"Entity B computes: B = g^b mod p = {g}^{b_private} mod {p} = {B}")

    print("\n=== Step 2: Public Key Exchange (over insecure network) ===")
    print(f"Entity A sends A = {A} to Entity B")
    print(f"Entity B sends B = {B} to Entity A")
    print("An eavesdropper on the network sees only p, g, A, and B")

    print("\n=== Step 3: Shared Secret Computation ===")
    secret_A = mod_exp(B, a_private, p)
    print(f"Entity A computes: S = B^a mod p = {B}^{a_private} mod {p} = {secret_A}")

    secret_B = mod_exp(A, b_private, p)
    print(f"Entity B computes: S = A^b mod p = {A}^{b_private} mod {p} = {secret_B}")

    print("\n=== Step 4: Verification ===")
    if secret_A == secret_B:
        print(f"Shared secrets MATCH. Key exchange successful.")
        print(f"Shared Secret Key = {secret_A}")
    else:
        print("Shared secrets DO NOT MATCH. Key exchange failed.")

    print("\n=== Summary ===")
    print(f"Public parameters : p = {p}, g = {g}")
    print(f"Entity A private  : {a_private}   Entity A public : {A}")
    print(f"Entity B private  : {b_private}   Entity B public : {B}")
    print(f"Final shared key  : {secret_A if secret_A == secret_B else 'MISMATCH'}")

if __name__ == "__main__":
    main()
