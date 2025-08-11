from FLAG import flag
from os import urandom
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from string import ascii_letters, digits
from secrets import choice

KEY = urandom(16)
IV = urandom(16)

sessionID = "".join([choice(ascii_letters + digits) for n in range(15)])

def encrypt(message, KEY=KEY, IV=IV):
    message = pad(message.encode(), 16).hex().encode()
    Cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return Cipher.encrypt(message)

def decrypt(ciphertext, KEY=KEY, IV=IV):
    Cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = Cipher.decrypt(bytes.fromhex(ciphertext))
    try:
        unpad(decrypted, 16)
        return True
    except ValueError:
        return False

def check_message(msg):
    msg = bytes.fromhex(msg).decode()
    return msg == sessionID

ct = encrypt(sessionID, KEY, IV)

def ProcessQuery(query):
    if "option" not in query:
        return {"error": "Must enter a valid option."}

    elif query["option"] == "get_ciphertext":
        return {"ciphertext": (IV + ct).hex()}

    elif query["option"] == "check_padding":
        resp = decrypt(query["ciphertext"], KEY, IV)
        return {"response": resp}

    elif query["option"] == "get_flag":
        resp = check_message(query["sessionID"])
        if resp:
            return {"flag": flag}
        else:
            return {"error": "Incorrect SessionID."}
    else:
        return {"error": "Invalid option."}
