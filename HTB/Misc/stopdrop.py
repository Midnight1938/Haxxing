from pwn import *

port = remote('94.237.57.59', 57064)

port.sendlineafter(b'(y/n) ', b'y')
port.recvline()

while True:
    recv = port.recvlineS().strip()
    
    if 'GORGE' not in recv and 'PHREAK' not in recv and 'FIRE' not in recv:
        print(recv)
        break
    
    res = recv.replace(", ", "-")
    res = res.replace("GORGE", "STOP")
    res = res.replace("PHREAK", "DROP")
    res = res.replace("FIRE", "ROLL")
    print(res)
    
    port.sendlineafter(b'do? ', res.encode())