import sys
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import binascii
import os

def xor_bytes(*args):
    """ Побитовый XOR для нескольких блоков. """
    result = args[0]
    for block in args[1:]:
        result = bytes(a ^ b for a, b in zip(result, block))
    return result

def unpad(data):
    """ Удаление PKCS7 паддинга. """
    if len(data) == 0 or data[-1] > AES.block_size:
        raise ValueError("Некорректный паддинг.")
    return data[:-data[-1]]

def decrypt_block(data, keys):
    """ Итеративная AES-дешифрация блока с несколькими ключами. """
    for key in reversed(keys):
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.decrypt(data)
    return data

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

def main():
    if len(sys.argv) != 2:
        print("Использование: python aes_decrypt.py <encrypted_file>")
        sys.exit(1)

    encrypted_file = sys.argv[1]

    try:
        # Загрузка зашифрованных данных из файла
        with open(encrypted_file, "rb") as f:
            final_output = f.read()

        # Запрос RSA ключа
        rsa_key_file = input("Введите путь к RSA приватному ключу: ")
        if not os.path.isfile(rsa_key_file):
            print(f"Ошибка: Файл '{rsa_key_file}' не существует.")
            sys.exit(1)

        with open(rsa_key_file, 'rb') as f:
            rsa_key = RSA.import_key(f.read())
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        rsa_block_size = rsa_key.size_in_bytes()
        num_keys = 3
        depth = 4
        encrypted_keys_size = num_keys * rsa_block_size

        if len(final_output) < encrypted_keys_size:
            raise ValueError("Недостаточно данных для извлечения ключей.")
        
        encrypted_keys_block = final_output[:encrypted_keys_size]
        encrypted_data = final_output[encrypted_keys_size:]
        
        # Извлечение и расшифрование AES-ключей
        encrypted_aes_keys = [encrypted_keys_block[i*rsa_block_size:(i+1)*rsa_block_size] for i in range(num_keys)]
        aes_keys = [cipher_rsa.decrypt(enc_key) for enc_key in encrypted_aes_keys]
        
        # Дешифрование данных
        decrypted_data = decrypt(encrypted_data, aes_keys, depth)
        decrypted_hex = binascii.hexlify(decrypted_data).decode()
        print(f"Расшифрованные данные: {decrypted_hex}")

    except Exception as e:
        print(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    main()