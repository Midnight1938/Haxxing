import socket
import json
from time import sleep

SERVER = "crypto.traboda.net"
PORT = 43305

def send_query(data):
    """Send query to server and return JSON response."""
    with socket.socket() as s:
        s.connect((SERVER, PORT))
        # Clear initial prompt
        s.recv(1024)
        # Send query
        s.send(json.dumps(data).encode() + b"\n")
        # Read response
        response = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            response += chunk
            try:
                decoded = response.decode()
                json_start = decoded.find('{')
                json_end = decoded.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    return json.loads(decoded[json_start:json_end])
            except:
                continue
        raise Exception("Failed to parse response")

def get_ciphertext():
    """Get ciphertext from server."""
    res = send_query({"option": "get_ciphertext"})
    return bytes.fromhex(res["ciphertext"])

def check_padding(ct_hex):
    """Check if padding is valid."""
    res = send_query({"option": "check_padding", "ciphertext": ct_hex})
    return res["response"]

def get_flag(session_id_hex):
    """Retrieve flag using recovered session ID."""
    res = send_query({"option": "get_flag", "sessionID": session_id_hex})
    return res.get("flag", "FLAG NOT FOUND")

def exploit():
    """Perform padding oracle attack."""
    iv_ct = get_ciphertext()
    iv, ct = iv_ct[:16], iv_ct[16:]
    
    plaintext = bytearray(16)
    intermediate = bytearray(16)

    for byte_pos in reversed(range(16)):
        padding_value = 16 - byte_pos
        print(f"Decrypting byte {byte_pos}...", end=" ", flush=True)

        # Prepare modified IV
        crafted_iv = bytearray(iv)
        for i in range(byte_pos + 1, 16):
            crafted_iv[i] ^= intermediate[i] ^ padding_value

        # Retry mechanism for robustness
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Optimized guessing order: prioritize likely values first
                candidates = [padding_value] + list(range(32, 127)) + list(range(0, 32)) + list(range(127, 256))
                for guess in candidates:
                    crafted_iv[byte_pos] = guess
                    ct_hex = (crafted_iv + ct).hex()
                    if check_padding(ct_hex):
                        intermediate[byte_pos] = guess ^ padding_value
                        plaintext[byte_pos] = intermediate[byte_pos] ^ iv[byte_pos]
                        print(f"0x{plaintext[byte_pos]:02x} ('{chr(plaintext[byte_pos]) if 32 <= plaintext[byte_pos] < 127 else '.'}')")
                        break
                else:
                    raise Exception(f"Failed to decrypt byte {byte_pos}")
                break  # Exit retry loop on success
            except Exception as e:
                print(f"Error: {e}, retrying ({attempt+1}/{max_retries})...")
                sleep(0.1)  # Short delay before retrying
        
        else:
            print(f"Failed to decrypt byte {byte_pos} after {max_retries} retries.")
            return
    
    # Remove PKCS#7 padding
    try:
        session_id = plaintext[:-plaintext[-1]].decode()
        print(f"Session ID: {session_id}")
        
        # Get flag
        flag = get_flag(session_id.encode().hex())
        print("Flag:", flag)
    except Exception as e:
        print(f"Error decoding session ID: {e}")

if __name__ == "__main__":
    exploit()
