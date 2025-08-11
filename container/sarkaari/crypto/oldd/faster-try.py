import socket
import json
import time

SERVER = "crypto.traboda.net"
PORT = 17057

def send_query(data):
    with socket.socket() as s:
        s.settimeout(2)
        s.connect((SERVER, PORT))
        
        # Clear initial prompt
        s.recv(1024)
        
        # Send query
        s.send(json.dumps(data).encode() + b"\n")
        
        # Read response
        response = b""
        start_time = time.time()
        while time.time() - start_time < 1.5:  # Max 1.5s per request
            try:
                chunk = s.recv(1024)
                if not chunk:
                    break
                response += chunk
                if b'}' in response:  # JSON end detected
                    break
            except socket.timeout:
                break
        
        # Extract JSON
        try:
            json_str = response.split(b'{', 1)[1].rsplit(b'}', 1)[0]
            return json.loads(b'{' + json_str + b'}')
        except:
            print(f"BAD RESPONSE: {response}")
            return {"error": "parse failed"}

def get_ciphertext():
    return send_query({"option": "get_ciphertext"})["ciphertext"]

def check_padding(ct):
    return send_query({"option": "check_padding", "ciphertext": ct})["response"]

def get_flag(sid):
    return send_query({"option": "get_flag", "sessionID": sid}).get("flag", "?")

def exploit():
    # Get initial ciphertext (IV + CT)
    iv_ct = bytes.fromhex(get_ciphertext())
    iv, ct = iv_ct[:16], iv_ct[16:]
    
    plaintext = bytearray(16)
    for pos in reversed(range(16)):
        padding = 16 - pos
        crafted_iv = bytearray(iv)
        
        # Set known bytes
        for i in range(pos + 1, 16):
            crafted_iv[i] ^= plaintext[i] ^ padding
        
        # Brute-force current byte
        for guess in range(256):
            crafted_iv[pos] = guess
            if check_padding((crafted_iv + ct).hex()):
                plaintext[pos] = (guess ^ padding) ^ iv[pos]
                print(f"Byte {pos:2} -> {plaintext[pos:].hex()}")
                break
    
    # Remove padding and get flag
    session_id = bytes(plaintext[:-plaintext[-1]]).hex()
    print("FLAG:", get_flag(session_id))

if __name__ == "__main__":
    exploit()
