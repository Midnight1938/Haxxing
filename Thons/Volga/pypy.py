from pwn import *

# Craft the sample messages
incomplete_padding_message = b'123456789012345'  # Message with incomplete padding
incomplete_polynomial_message = b'12345678'      # Message with incomplete polynomial

from pwn import *

# Connect to the remote server
port = remote("chals.damctf.xyz", 31413)

# Initialize variables
flag = ''

# Loop to retrieve the flag
while True:
    # Send the current index to the server
    port.sendlineafter(b'(hex): ', str(id).encode())
    # Receive the character at the specified index
    port.recvuntil(b': ')
    char = port.recv(1)
    
    # Append the received character to the flag
    flag += char.decode()
    id += 1
    
    # Check if the received character is '}'
    if char == b'}':
        break

# Print the flag
print(flag)
