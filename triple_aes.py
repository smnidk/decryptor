from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def triple_aes_encrypt(text, keys):
    key1, key2, key3 = keys

    # First encryption
    cipher1 = AES.new(key1.encode('utf-8'), AES.MODE_EAX)
    nonce1 = cipher1.nonce
    ciphertext1, tag1 = cipher1.encrypt_and_digest(text.encode('utf-8'))

    # Second encryption
    cipher2 = AES.new(key2.encode('utf-8'), AES.MODE_EAX)
    nonce2 = cipher2.nonce
    ciphertext2, tag2 = cipher2.encrypt_and_digest(ciphertext1)

    # Third encryption
    cipher3 = AES.new(key3.encode('utf-8'), AES.MODE_EAX)
    nonce3 = cipher3.nonce
    ciphertext3, tag3 = cipher3.encrypt_and_digest(ciphertext2)

    return base64.b64encode(nonce1 + nonce2 + nonce3 + ciphertext3).decode('utf-8')

def triple_aes_decrypt(ciphertext, keys):
    key1, key2, key3 = keys

    data = base64.b64decode(ciphertext)
    nonce1 = data[:16]
    nonce2 = data[16:32]
    nonce3 = data[32:48]
    ciphertext3 = data[48:]

    # Third decryption
    cipher3 = AES.new(key3.encode('utf-8'), AES.MODE_EAX, nonce=nonce3)
    ciphertext2 = cipher3.decrypt(ciphertext3)

    # Second decryption
    cipher2 = AES.new(key2.encode('utf-8'), AES.MODE_EAX, nonce=nonce2)
    ciphertext1 = cipher2.decrypt(ciphertext2)

    # First decryption
    cipher1 = AES.new(key1.encode('utf-8'), AES.MODE_EAX, nonce=nonce1)
    plaintext = cipher1.decrypt(ciphertext1)

    return plaintext.decode('utf-8')

def generate_keys():
    return [get_random_bytes(16).hex() for _ in range(3)]