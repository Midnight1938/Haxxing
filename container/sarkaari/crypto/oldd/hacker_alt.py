import socket
import json
import argparse
from time import sleep
from concurrent.futures import ThreadPoolExecutor

SERVER = "crypto.traboda.net"
PORT = None  # Will be set via command-line

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


# Keep track of successful results
found_byte = None

def check_padding_for_guess(guess, crafted_iv, ct, byte_pos, padding_value):
    """Check a single guess value in a separate thread"""
    global found_byte
    
    if found_byte is not None:
        return None  # Another thread already found the value
    
    crafted = bytearray(crafted_iv)
    crafted[byte_pos] = guess
    ct_hex = (crafted + ct).hex()
    
    try:
        with socket.socket() as s:
            s.connect((SERVER, PORT))
            s.recv(1024)  # Clear initial prompt
            s.send(json.dumps({"option": "check_padding", "ciphertext": ct_hex}).encode() + b"\n")
            
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
                        result = json.loads(decoded[json_start:json_end])
                        if result["response"]:
                            # Found valid padding
                            intermediate_value = guess ^ padding_value
                            plaintext_byte = intermediate_value ^ crafted_iv[byte_pos]
                            found_byte = (guess, intermediate_value, plaintext_byte)
                            return found_byte
                        return None
                except:
                    continue
    except Exception as e:
        return None
    
    return None

def exploit():
    """Perform parallel padding oracle attack."""
    global found_byte
    
    iv_ct = send_query({"option": "get_ciphertext"})
    iv_ct = bytes.fromhex(iv_ct["ciphertext"])
    iv, ct = iv_ct[:16], iv_ct[16:]
    
    plaintext = bytearray(16)
    intermediate = bytearray(16)
    
    # Parallelize the attack
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        for byte_pos in reversed(range(16)):
            padding_value = 16 - byte_pos
            print(f"Decrypting byte {byte_pos}...", end=" ", flush=True)
            
            found_byte = None
            crafted_iv = bytearray(iv)
            
            for i in range(byte_pos + 1, 16):
                crafted_iv[i] ^= intermediate[i] ^ padding_value
            
            # Optimize guess order for alphanumeric session IDs
            candidates = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123)) + \
                        [padding_value] + list(range(32, 48)) + list(range(58, 65)) + \
                        list(range(91, 97)) + list(range(123, 127)) + \
                        list(range(0, 32)) + list(range(127, 256))
            
            # Remove duplicates while preserving order
            candidates = list(dict.fromkeys(candidates))
            
            # Submit all guesses concurrently
            futures = [executor.submit(check_padding_for_guess, guess, crafted_iv, ct, byte_pos, padding_value) 
                      for guess in candidates]
            
            # Wait for any successful result
            success = False
            for future in futures:
                result = future.result()
                if result:
                    guess, intermediate_value, plaintext_byte = result
                    intermediate[byte_pos] = intermediate_value
                    plaintext[byte_pos] = plaintext_byte
                    print(f"0x{plaintext_byte:02x} ('{chr(plaintext_byte) if 32 <= plaintext_byte < 127 else '.'}')")
                    success = True
                    break
            
            if not success:
                print(f"Failed to decrypt byte {byte_pos}")
                return
    
    # Process the decrypted data
    try:
        hex_str = plaintext.decode()
        session_id = bytes.fromhex(hex_str).decode()
        print(f"Session ID: {session_id}")
        
        flag = send_query({"option": "get_flag", "sessionID": session_id})
        print("Flag:", flag.get("flag", "FLAG NOT FOUND"))
    except Exception as e:
        print(f"Error decoding session ID: {e}")
