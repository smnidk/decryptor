from aes import aes_decrypt
from triple_aes import triple_aes_decrypt

def decrypt_text(ciphertext, method, keys=None):
    if method == "aes":
        key = keys[0] if keys else input("Введите ключ: ").strip()
        return aes_decrypt(ciphertext, key)
    elif method == "triple_aes":
        if not keys:
            keys = [input(f"Введите ключ {i+1}: ").strip() for i in range(3)]
        return triple_aes_decrypt(ciphertext, keys)
    else:
        print("Ошибка: Неверный метод расшифрования.")
        return None