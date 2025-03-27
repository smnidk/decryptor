import sys
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import binascii
import random

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

def encrypt_block(data, keys):
    """ Итеративное AES-шифрование блока с несколькими ключами. """
    for key in keys:
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.encrypt(data)
    return data

def encrypt(data, keys, depth):
    """ Основная функция шифрования """
    data = pad(data)
    blocks = [data[i:i+AES.block_size] for i in range(0, len(data), AES.block_size)]
    encrypted_blocks = []
    prev_blocks = [b"\x00" * AES.block_size] * depth
    
    for block in blocks:
        mixed_block = xor_bytes(block, *prev_blocks)
        enc_block = encrypt_block(mixed_block, keys)
        encrypted_blocks.append(enc_block)
        prev_blocks.pop(0)
        prev_blocks.append(enc_block)
    
    return b"".join(encrypted_blocks)

def main():
    if len(sys.argv) != 2:
        print("Использование: python aes_encrypt.py <data>")
        sys.exit(1)

    data = sys.argv[1].encode()

    try:
        # Запрос AES ключа
        aes_key_input = input("Введите AES ключ (в hex формате) или оставьте пустым для генерации случайного ключа: ")
        if aes_key_input:
            aes_keys = [binascii.unhexlify(aes_key_input)]
        else:
            key_lengths = [16, 24, 32]
            aes_keys = [get_random_bytes(random.choice(key_lengths)) for _ in range(3)]
            print(f"Сгенерированные AES ключи: {[binascii.hexlify(key).decode() for key in aes_keys]}")

        # Запрос RSA ключа
        rsa_option = input("Введите '1' для использования существующего RSA ключа или '2' для генерации нового: ")
        if rsa_option == '1':
            rsa_key_file = input("Введите путь к RSA публичному ключу: ")
            with open(rsa_key_file, 'rb') as f:
                rsa_key = RSA.import_key(f.read())
        elif rsa_option == '2':
            print("Генерация RSA ключей...")
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            with open("private_key.pem", "wb") as f:
                f.write(private_key.export_key())
            with open("public_key.pem", "wb") as f:
                f.write(public_key.export_key())
            print("RSA ключи сгенерированы и сохранены в файлы 'private_key.pem' и 'public_key.pem'.")
            rsa_key = public_key
        else:
            print("Неверный выбор.")
            sys.exit(1)

        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        rsa_block_size = rsa_key.size_in_bytes()

        # Шифрование AES-ключей
        encrypted_aes_keys = [cipher_rsa.encrypt(key) for key in aes_keys]
        encrypted_keys_block = b''.join(encrypted_aes_keys)
        
        # Шифрование данных
        num_keys = len(aes_keys)
        depth = 4
        encrypted_data = encrypt(data, aes_keys, depth)
        final_output = encrypted_keys_block + encrypted_data
        
        encrypted_hex = binascii.hexlify(final_output).decode()
        print(f"Зашифрованные данные: {encrypted_hex}")

        # Сохранение зашифрованных данных в файл
        with open("encrypted_data.bin", "wb") as f:
            f.write(final_output)

    except Exception as e:
        print(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    main()