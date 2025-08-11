from Crypto.Util.number import getPrime, bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from FLAG import flag
import os

e = 3
p = getPrime(512)
q = getPrime(512)
N = p * q

password = os.urandom(8)

prefix = b"Hey! Hope you're having a great day :) Here's the super secret password: "+password

m = prefix

m_int = bytes_to_long(m)

c = pow(m_int, e, N)

cipher = AES.new(pad(password,16), AES.MODE_ECB)
enc_flag = cipher.encrypt(pad(flag,16))

with open("output.txt","w") as file:
    file.write(f"N = {N}")
    file.write(f"\ne = {e}")
    file.write(f"\nc = {c}")
    file.write(f"\nenc_flag = '{enc_flag.hex()}'")
