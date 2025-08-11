from Crypto.Cipher import DES
import binascii
from multiprocessing import Pool, cpu_count

# Ciphertext (hex)
ciphertext_hex = "e1d5e1fcaae4aba0b735c8fb2ae8797728b073a34b14c57be236c819e6d5f4bbd94f5748ff9d1e008fcad8d403e23d02845a51513bb1e65027ed1bebdcb70973d411a0503cf06c261cb04e1ce1c12925"
ciphertext = binascii.unhexlify(ciphertext_hex)

# Function to test a range of keys
def test_keys(start_key, end_key):
    for key in range(start_key, end_key):
        try:
            # Print progress every 1,000,000 keys
            if key % 1_000_000 == 0:
                print(f"Trying key: {key:#018x}")  # Print key in hexadecimal format
            
            # Convert integer key to bytes
            key_bytes = key.to_bytes(8, byteorder='big')
            
            # Create DES cipher in ECB mode
            cipher = DES.new(key_bytes, DES.MODE_ECB)
            
            # Decrypt ciphertext
            plaintext = cipher.decrypt(ciphertext)
            
            # Check if plaintext starts with 'flag{' and ends with '}'
            if plaintext.startswith(b'flag{') and plaintext.endswith(b'}'):
                print(f"Key found: {key_bytes}")
                print(f"Plaintext: {plaintext.decode('latin-1')}")
                return True
        except (ValueError, UnicodeDecodeError):
            continue
    return False

# Brute-force DES key using multiprocessing
def brute_force_des():
    keyspace = 0xFFFFFFFFFFFFFF00  # Total number of keys (2^56)
    num_processes = cpu_count()  # Number of CPU cores
    chunk_size = keyspace // num_processes  # Divide keyspace into chunks

    # Create a pool of workers
    with Pool(processes=num_processes) as pool:
        # Create tasks for each chunk
        tasks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
        
        # Execute tasks in parallel
        results = pool.starmap(test_keys, tasks)
        
        # Check if any process found the key
        if any(results):
            print("Key found!")
        else:
            print("Key not found.")

brute_force_des()