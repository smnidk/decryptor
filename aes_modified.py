from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hashlib import sha256
import os

def xor_bytes(*args):
    """ Побитовый XOR для нескольких блоков. """
    result = args[0]
    for block in args[1:]:
        result = bytes(a ^ b for a, b in zip(result, block))
    return result

def pad(data):
    """ PKCS7 паддинг. """
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    """ Удаление PKCS7 паддинга. """
    return data[:-data[-1]]

def encrypt_block(data, keys):
    """ Итеративное AES-шифрование блока с несколькими ключами. """
    for key in keys:
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.encrypt(data)
    return data

def decrypt_block(data, keys):
    """ Итеративная AES-дешифрация блока с несколькими ключами. """
    for key in reversed(keys):
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.decrypt(data)
    return data

def encrypt(data, keys, depth):
    """ Основная функция шифрования """
    data = pad(data)
    blocks = [data[i:i+AES.block_size] for i in range(0, len(data), AES.block_size)]
    encrypted_blocks = []
    prev_blocks = [b"\x00" * AES.block_size] * depth  # Инициализация нулевыми блоками
    
    for block in blocks:
        mixed_block = xor_bytes(block, *prev_blocks)
        enc_block = encrypt_block(mixed_block, keys)
        encrypted_blocks.append(enc_block)
        prev_blocks.pop(0)
        prev_blocks.append(enc_block)
    
    return b"".join(encrypted_blocks)

def decrypt(data, keys, depth):
    """ Основная функция расшифровки """
    blocks = [data[i:i+AES.block_size] for i in range(0, len(data), AES.block_size)]
    decrypted_blocks = []
    prev_blocks = [b"\x00" * AES.block_size] * depth
    
    for enc_block in blocks:
        mixed_block = decrypt_block(enc_block, keys)
        dec_block = xor_bytes(mixed_block, *prev_blocks)
        decrypted_blocks.append(dec_block)
        prev_blocks.pop(0)
        prev_blocks.append(enc_block)
    
    return unpad(b"".join(decrypted_blocks))

# === Преобразование строки в ключ ===
def string_to_key(input_str, key_size=16):
    """ Преобразует строку в фиксированный ключ (16, 24 или 32 байта). """
    hash_value = sha256(input_str.encode()).digest()  # Хешируем строку
    return hash_value[:key_size]  # Берем нужную длину ключа

# === Ввод параметров ===
def get_keys(num_keys):
    """ Функция получения ключей от пользователя. """
    keys = []
    choice = input("Вы хотите ввести ключи вручную? (y/n): ").strip().lower()
    if choice == 'y':
        for i in range(num_keys):
            key_input = input(f"Введите ключ {i+1} (строка или hex): ")
            if all(c in '0123456789abcdefABCDEF' for c in key_input) and len(key_input) in (32, 48, 64):
                key = bytes.fromhex(key_input)  # Если введен hex, используем его
            else:
                key = string_to_key(key_input)  # Иначе, преобразуем строку в ключ
            keys.append(key)
    else:
        keys = [get_random_bytes(16) for _ in range(num_keys)]
        print("Сгенерированные ключи:")
        for i, key in enumerate(keys):
            print(f"Ключ {i+1}: {key.hex()}")
    return keys

# === ГЛАВНАЯ ЛОГИКА ===
mode = input("Выберите режим: (e) шифрование / (d) дешифрование: ").strip().lower()
num_keys = int(input("Введите количество ключей: "))
depth = int(input("Введите количество предыдущих блоков для XOR: "))
keys = get_keys(num_keys)

if mode == 'e':
    plaintext = input("Введите сообщение для шифрования: ").encode()
    encrypted = encrypt(plaintext, keys, depth)
    print("Encrypted:", encrypted.hex())

elif mode == 'd':
    encrypted_hex = input("Введите зашифрованные данные (hex): ")
    encrypted = bytes.fromhex(encrypted_hex)
    decrypted = decrypt(encrypted, keys, depth)
    print("Decrypted:", decrypted.decode(errors='ignore'))

else:
    print("Неверный режим работы!")
