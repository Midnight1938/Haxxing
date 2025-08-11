import socket
import json
from time import sleep

SERVER = "crypto.traboda.net"
PORT = 57377

def send_query(data):
    with socket.socket() as s:
        s.connect((SERVER, PORT))
        
        # Clear initial "Query?" prompt
        s.recv(1024)
        
        # Send query
        s.send(json.dumps(data).encode() + b"\n")
        
        # Read response (handle multiple lines)
        response = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            response += chunk
            try:  # Check if we have complete JSON
                decoded = response.decode()
                json_start = decoded.find('{')
                json_end = decoded.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    return json.loads(decoded[json_start:json_end])
            except:
                continue

        raise Exception("Failed to parse response")

def get_ciphertext():
    res = send_query({"option": "get_ciphertext"})
    return bytes.fromhex(res["ciphertext"])

def check_padding(ct_hex):
    res = send_query({"option": "check_padding", "ciphertext": ct_hex})
    return res["response"]

def get_flag(session_id_hex):
    res = send_query({"option": "get_flag", "sessionID": session_id_hex})
    return res.get("flag", "FLAG NOT FOUND")

def exploit():
    iv_ct = get_ciphertext()
    iv, ct = iv_ct[:16], iv_ct[16:]
    
    plaintext = bytearray(16)
    intermediate = bytearray(16)

    for byte_pos in reversed(range(16)):
        padding_value = 16 - byte_pos
        
        # Prepare modified IV
        crafted_iv = bytearray(iv)
        for i in range(byte_pos + 1, 16):
            crafted_iv[i] ^= intermediate[i] ^ padding_value

        # Brute-force current byte
        for guess in range(256):
            crafted_iv[byte_pos] = guess
            ct_hex = (crafted_iv + ct).hex()
            
            if check_padding(ct_hex):
                intermediate[byte_pos] = guess ^ padding_value
                plaintext[byte_pos] = intermediate[byte_pos] ^ iv[byte_pos]
                print(f"Byte {byte_pos:2} -> 0x{plaintext[byte_pos]:02x}")
                break

    # Remove PKCS#7 padding
    session_id = plaintext[:-plaintext[-1]].decode()
    print(f"Session ID: {session_id}")
    
    # Get flag
    print("Flag:", get_flag(session_id.encode().hex()))

if __name__ == "__main__":
    exploit()
