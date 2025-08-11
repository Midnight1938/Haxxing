import socket
import json
import binascii
from time import sleep

SERVER = "crypto.traboda.net"
PORT = 36207
BLOCK_SIZE = 16

def send(data):
    """Raw socket communication with retries"""
    for _ in range(3):
        try:
            with socket.socket() as s:
                s.settimeout(5)
                s.connect((SERVER, PORT))
                s.recv(1024)  # Clear prompt
                s.send(json.dumps(data).encode() + b"\n")
                return json.loads(s.recv(1024).decode().strip())
        except (socket.error, json.JSONDecodeError):
            sleep(1)
            continue
    raise ConnectionError("Failed to communicate with server")

def decrypt_block(target_block, prev_block):
    plaintext = bytearray(BLOCK_SIZE)
    for pos in reversed(range(BLOCK_SIZE)):
        pad_value = BLOCK_SIZE - pos
        modified_prev = bytearray(prev_block)
        
        # Set known bytes for valid padding
        for i in range(pos + 1, BLOCK_SIZE):
            modified_prev[i] ^= (pad_value ^ (pad_value + 1))
        
        # Brute-force current byte
        for guess in range(256):
            modified_prev[pos] = guess
            ct_hex = binascii.hexlify(modified_prev + target_block).decode()
            
            if send({"option": "check_padding", "ciphertext": ct_hex})["response"]:
                plaintext[pos] = (guess ^ pad_value) ^ prev_block[pos]
                break
        
        # Prepare for next byte
        for i in range(pos, BLOCK_SIZE):
            modified_prev[i] = (plaintext[i] ^ prev_block[i]) ^ (pad_value + 1)
    
    return bytes(plaintext)

def exploit():
    # Get initial ciphertext
    data = send({"option": "get_ciphertext"})
    iv_ct = bytes.fromhex(data["ciphertext"])
    iv, c1, c2 = iv_ct[:16], iv_ct[16:32], iv_ct[32:48]

    # Decrypt blocks
    plain_c2 = decrypt_block(c2, c1)
    plain_c1 = decrypt_block(c1, iv)

    # Process final plaintext
    hex_str = (plain_c1 + plain_c2).decode()
    padded = bytes.fromhex(hex_str)
    session_id = padded[:-padded[-1]].decode()

    # Get flag
    flag_data = send({
        "option": "get_flag",
        "sessionID": session_id.encode().hex()
    })
    print(f"FLAG: {flag_data.get('flag', 'NOT FOUND')}")

if __name__ == "__main__":
    exploit()
