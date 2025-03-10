import os
import struct
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# Функция генерации ключей
def derive_keys(password, salt, k):
    """Генерация k ключей из пароля"""
    return [PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=lambda msg: sha256(msg).digest()) for _ in range(k)]

# Дополнение данных до размера блока AES
def pad(data):
    padding_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([padding_len] * padding_len)

# Удаление дополнения
def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]

# Шифрование файла
def encrypt_file(input_file, output_file, password, n, k):
    salt = os.urandom(16)  # Генерация соли
    keys = derive_keys(password, salt, k)  # Генерация k ключей

    iv = os.urandom(AES.block_size)  # Начальный вектор
    prev_blocks = [b'\x00' * AES.block_size] * n  # Буфер для предыдущих n блоков

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(salt)  # Сохранение соли
        f_out.write(iv)    # Сохранение IV

        cipher = AES.new(keys[0], AES.MODE_CBC, iv)  # Первый ключ и IV
        while True:
            block = f_in.read(AES.block_size)
            if not block:
                break
            if len(block) < AES.block_size:
                block = pad(block)

            # XOR с предыдущими блоками
            for i in range(n):
                block = bytes(a ^ b for a, b in zip(block, prev_blocks[i]))

            encrypted_block = cipher.encrypt(block)
            f_out.write(encrypted_block)

            # Сдвиг буфера предыдущих блоков
            prev_blocks.pop(0)
            prev_blocks.append(encrypted_block)

            # Переключение на следующий ключ (если k > 1)
            cipher = AES.new(keys[len(prev_blocks) % k], AES.MODE_CBC, iv)

# Расшифровка файла
def decrypt_file(input_file, output_file, password, n, k):
    with open(input_file, 'rb') as f_in:
        salt = f_in.read(16)  # Читаем соль
        iv = f_in.read(AES.block_size)  # Читаем IV
        keys = derive_keys(password, salt, k)  # Восстанавливаем ключи

        prev_blocks = [b'\x00' * AES.block_size] * n  # Буфер для предыдущих n блоков

        with open(output_file, 'wb') as f_out:
            cipher = AES.new(keys[0], AES.MODE_CBC, iv)

            while True:
                encrypted_block = f_in.read(AES.block_size)
                if not encrypted_block:
                    break

                decrypted_block = cipher.decrypt(encrypted_block)

                # Обратный XOR с предыдущими блоками
                for i in range(n):
                    decrypted_block = bytes(a ^ b for a, b in zip(decrypted_block, prev_blocks[i]))

                if len(encrypted_block) < AES.block_size:
                    decrypted_block = unpad(decrypted_block)

                f_out.write(decrypted_block)

                # Сдвиг буфера предыдущих блоков
                prev_blocks.pop(0)
                prev_blocks.append(encrypted_block)

                # Переключение на следующий ключ (если k > 1)
                cipher = AES.new(keys[len(prev_blocks) % k], AES.MODE_CBC, iv)

# Тестовый запуск
if __name__ == "__main__":
    password = b"my_secure_password"
    n = 2  # Используем предыдущие 2 блока
    k = 3  # Используем 3 ключа

    encrypt_file("input.txt", "encrypted.aes", password, n, k)
    decrypt_file("encrypted.aes", "decrypted.txt", password, n, k)
