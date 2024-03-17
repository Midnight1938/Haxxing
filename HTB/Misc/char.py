from pwn import *

port = remote('94.237.63.83', 50921)

flag = ''
id = 0

while True:
    port.sendlineafter(b'index: ', str(id).encode())
    port.recvuntil(b': ')
    char = port.recvS(1)
    
    flag += char
    id += 1
    
    if char == '}':
        break

print(flag)