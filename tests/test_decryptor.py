import pytest
from decryptor.aes import aes_encrypt, aes_decrypt
from decryptor.aes_modified import encrypt, decrypt
from decryptor.caesar import caesar_encrypt, caesar_decrypt
from decryptor.vigenere import vigenere_encrypt, vigenere_decrypt
from decryptor.quadratic_cipher import quadratic_encrypt, quadratic_decrypt


# Тесты для AES (aes.py)
def test_aes_decrypt():
    key = "secret_key_16bytes"
    plaintext = "Hello AES!"
    ciphertext = aes_encrypt(plaintext, key)
    assert aes_decrypt(ciphertext, key) == plaintext


# Тесты для модифицированного AES (aes_modified.py)
def test_modified_aes_decrypt():
    # Используем ключи длиной 16 байт (128 бит)
    keys = [b"16bytekey1234567", b"another16bytekey"]  # 16 bytes each
    depth = 2
    data = b"Secret Data"
    encrypted = encrypt(data, keys, depth)
    assert decrypt(encrypted, keys, depth) == data


# Тесты для Цезаря (caesar.py)
@pytest.mark.parametrize("shift", [3, 5, 13])
def test_caesar_decrypt(shift):
    plaintext = "Hello Caesar!"
    encrypted = caesar_encrypt(plaintext, shift)
    assert caesar_decrypt(encrypted, shift) == plaintext


@pytest.mark.skip(reason="Игнорируем внутренние тесты библиотеки")
def test_crypto_self_tests():
    pass


# Тесты для Виженера (vigenere.py)
def test_vigenere_decrypt():
    key = "KEY"
    plaintext = "ATTACKATDAWN"
    encrypted = vigenere_encrypt(plaintext, key)
    assert vigenere_decrypt(encrypted, key) == plaintext.upper()


# Тесты для квадратичного шифра (quadratic_cipher.py)
def test_quadratic_decrypt():
    params = {"a": 1, "b": 2, "c": 3, "m": 257}
    plaintext = "Hello Quadratic!"
    encrypted = quadratic_encrypt(plaintext, **params)
    assert quadratic_decrypt(encrypted, **params) == plaintext


# Тест обработки ошибок
def test_decrypt_errors():
    # Неверный ключ для AES
    with pytest.raises(ValueError):
        aes_decrypt("invalid_ciphertext", "wrong_key")

    # Недостаточно ключей для модифицированного AES
    with pytest.raises(ValueError):
        decrypt(b"data", [b"key1"], 2)  # Исправлено имя функции
