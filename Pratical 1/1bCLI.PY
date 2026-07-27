import sys

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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python 1B_transposition_cli.py [encrypt|decrypt] <text> <key>")
    else:
        mode, text, key = sys.argv[1], sys.argv[2], sys.argv[3]
        if mode == "encrypt":
            print(encrypt(text, key))
        elif mode == "decrypt":
            print(decrypt(text, key))
        else:
            print("Invalid mode")
