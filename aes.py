from Crypto.Cipher import AES
import base64

def aes_encrypt(text, key):
    try:
        if len(key.encode('utf-8')) not in [16, 24, 32]:
            raise ValueError("Ключ должен быть длиной 16, 24 или 32 байта.")
        cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
        return base64.b64encode(nonce + ciphertext).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Ошибка при шифровании AES: {str(e)}")

def aes_decrypt(ciphertext, key):
    try:
        if len(key.encode('utf-8')) not in [16, 24, 32]:
            raise ValueError("Ключ должен быть длиной 16, 24 или 32 байта.")
        data = base64.b64decode(ciphertext)
        nonce = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Ошибка при дешифровании AES: {str(e)}")