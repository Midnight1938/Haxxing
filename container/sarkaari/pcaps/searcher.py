import gmpy2
from Crypto.Util.number import long_to_bytes

ct = 710289350683868503644597519669917810036866060097512736293170169932115475815119142207293435658975273721020114420910211496808786789

# Compute cube root of the ciphertext (since e=3)
root, is_exact = gmpy2.iroot(ct, 3)
if is_exact:
    print("Decrypted message:", long_to_bytes(int(root)).decode())
else:
    print("Cube root attack failed - message too large for direct recovery")
