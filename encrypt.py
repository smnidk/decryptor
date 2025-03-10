from aes import aes_encrypt
from triple_aes import triple_aes_encrypt, generate_keys

def encrypt_text(text, method, keys=None):
    if method == "aes":
        key = keys[0] if keys else input("Введите ключ: ").strip()
        return aes_encrypt(text, key)
    elif method == "triple_aes":
        if not keys:
            key_choice = input("Введите '1' для ввода трех ключей или '2' для генерации случайных ключей: ").strip()
            if key_choice == "1":
                keys = [input(f"Введите ключ {i+1}: ").strip() for i in range(3)]
            elif key_choice == "2":
                keys = generate_keys()
                print("Сгенерированные ключи:", keys)
            else:
                print("Ошибка: Неверный ввод, попробуйте снова.")
                return None
        return triple_aes_encrypt(text, keys)
    else:
        print("Ошибка: Неверный метод шифрования.")
        return None
    