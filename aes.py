from Crypto.Cipher import AES
import base64
from Crypto.Random import get_random_bytes
from hashlib import sha256


def validate_key(key):
    """Проверяет и нормализует ключ"""
    if isinstance(key, str):
        key = key.encode("utf-8")
    if len(key) not in [16, 24, 32]:
        key = sha256(key).digest()[:32]
    return key


def aes_encrypt(text, key):
    """Шифрование AES-GCM.
    Возвращает nonce, тег аутентификации и шифртекст в base64."""
    try:
        key = validate_key(key)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(text.encode("utf-8"))
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Ошибка шифрования: {str(e)}")


def aes_decrypt(ciphertext, key):
    try:
        key = validate_key(key)
        data = base64.b64decode(ciphertext)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Ошибка дешифрования: {str(e)}")
