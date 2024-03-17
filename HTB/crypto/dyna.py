def to_identity_map(a):
    return ord(a) - 0x41 # this was built in

def from_identity_map(a):
    return chr(a % 26 + 0x41) # this was built in

with open('output.txt') as f:
    f.readline()
    enc = f.readline()

flag = ''
for i in range(len(enc)):
    ech = enc[i]
    if not ech.isalpha():
        m = ech
    else:
        echi = to_identity_map(ech)
        m = from_identity_map(echi - i) # reverse of the (echi - i), rest is same
    flag += m

print(f'HTB{{{flag}}}')