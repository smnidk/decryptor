from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hashlib import sha256
import secrets


def generate_random_key(key_size=16):
    """Генерирует случайный ключ в hex-формате"""
    return secrets.token_hex(key_size)


def xor_bytes(*args):
    """Побитовый XOR для нескольких блоков."""
    result = args[0]
    for block in args[1:]:
        result = bytes(a ^ b for a, b in zip(result, block))
    return result


def pad(data):
    """PKCS7 паддинг."""
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_len] * pad_len)


def unpad(data):
    """Удаление PKCS7 паддинга."""
    return data[: -data[-1]]


def encrypt_block(data, keys):
    """Итеративное AES-шифрование блока с несколькими ключами."""
    for key in keys:
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.encrypt(data)
    return data


def decrypt_block(data, keys):
    """Итеративная AES-дешифрация блока с несколькими ключами."""
    for key in reversed(keys):
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.decrypt(data)
    return data


def encrypt(data, keys, depth):
    """Основная функция шифрования"""
    data = pad(data)
    blocks = [data[i : i + AES.block_size] for i in range(0, len(data), AES.block_size)]
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
    """Основная функция расшифровки"""
    blocks = [data[i : i + AES.block_size] for i in range(0, len(data), AES.block_size)]
    decrypted_blocks = []
    prev_blocks = [b"\x00" * AES.block_size] * depth

    for enc_block in blocks:
        mixed_block = decrypt_block(enc_block, keys)
        dec_block = xor_bytes(mixed_block, *prev_blocks)
        decrypted_blocks.append(dec_block)
        prev_blocks.pop(0)
        prev_blocks.append(enc_block)

    return unpad(b"".join(decrypted_blocks))


def string_to_key(input_str, key_size=16):
    """Преобразует строку в фиксированный ключ (16, 24 или 32 байта)."""
    hash_value = sha256(input_str.encode()).digest()  # Хешируем строку
    return hash_value[:key_size]  # Берем нужную длину ключа


def main():
    import sys
    import binascii

    if len(sys.argv) < 6:
        print(
            "Usage: python aes_modified.py <mode> <data> <num_keys> <depth> <key1> [<key2> ...]"
        )
        sys.exit(1)

    mode = sys.argv[1]
    data = binascii.unhexlify(sys.argv[2])
    num_keys = int(sys.argv[3])
    depth = int(sys.argv[4])
    keys = [binascii.unhexlify(key) for key in sys.argv[5 : 5 + num_keys]]

    if mode == "e":
        result = encrypt(data, keys, depth)
    elif mode == "d":
        result = decrypt(data, keys, depth)
    else:
        print("Invalid mode. Use 'e' for encryption or 'd' for decryption.")
        sys.exit(1)

    print(binascii.hexlify(result).decode())


if __name__ == "__main__":
    main()
