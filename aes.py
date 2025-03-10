from Crypto.Cipher import AES
import base64

def aes_encrypt(text, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def aes_decrypt(ciphertext, key):
    data = base64.b64decode(ciphertext)
    nonce = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode('utf-8')