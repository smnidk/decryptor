import random
import string
from vigenere import vigenere_decrypt
from text_utils import clean_text
from kasiski import kasiski_examination
from frequency import find_vigenere_key
from itertools import cycle


def generate_random_text(length=100):
    """ Генерирует случайный текст из букв английского алфавита. """
    return ''.join(random.choices(string.ascii_uppercase + " ", k=length))

def vigenere_encrypt(plaintext, key):
    """ Шифрует текст шифром Виженера. """
    alphabet = string.ascii_uppercase
    ciphertext = []
    key_cycle = cycle(key.upper())

    for char in plaintext:
        if char in alphabet:
            key_char = next(key_cycle)
            shift = alphabet.index(key_char)
            new_index = (alphabet.index(char) + shift) % len(alphabet)
            ciphertext.append(alphabet[new_index])
        else:
            ciphertext.append(char)

    return "".join(ciphertext)

def test_vigenere():
    """ Генерирует случайный текст, шифрует его и пытается расшифровать. """
    plaintext = generate_random_text(200)
    key = ''.join(random.choices(string.ascii_uppercase, k=random.randint(3, 7)))  # Случайный ключ длиной 3-7 символов

    ciphertext = vigenere_encrypt(clean_text(plaintext), key)
    print(f"🔑 Исходный ключ: {key}")
    print(f"📝 Зашифрованный текст: {ciphertext}")

    # Взлом шифра
    key_length = kasiski_examination(ciphertext)
    if not key_length:
        print("❌ Не удалось определить длину ключа.")
        return

    guessed_key = find_vigenere_key(ciphertext, key_length)
    print(f"📝 Определённый ключ: {guessed_key}")

    decrypted_text = vigenere_decrypt(ciphertext, guessed_key)
    print("\n🔓 Расшифрованный текст:", decrypted_text)

if __name__ == "__main__":
    test_vigenere()
