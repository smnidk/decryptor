# Расширенный алфавит для поддержки русского языка
RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET = "abcdefghijklmnopqrstuvwxyz" + RUSSIAN_ALPHABET

def vigenere_encrypt(text, key):
    try:
        if not key:
            raise ValueError("Ключ не может быть пустым.")
        key = key.lower()
        encrypted = ""
        key_index = 0

        for char in text:
            if char.lower() in ALPHABET:
                # Определяем, какой алфавит использовать (английский или русский)
                alphabet = "abcdefghijklmnopqrstuvwxyz" if char.lower() in "abcdefghijklmnopqrstuvwxyz" else RUSSIAN_ALPHABET
                shift = alphabet.index(key[key_index % len(key)])
                new_index = (alphabet.index(char.lower()) + shift) % len(alphabet)
                new_char = alphabet[new_index]
                encrypted += new_char.upper() if char.isupper() else new_char
                key_index += 1
            else:
                encrypted += char  # Сохраняем пробелы и другие символы

        return encrypted
    except Exception as e:
        raise ValueError(f"Ошибка при шифровании Виженера: {str(e)}")

def vigenere_decrypt(text, key):
    try:
        if not key:
            raise ValueError("Ключ не может быть пустым.")
        key = key.lower()
        decrypted = ""
        key_index = 0

        for char in text:
            if char.lower() in ALPHABET:
                # Определяем, какой алфавит использовать (английский или русский)
                alphabet = "abcdefghijklmnopqrstuvwxyz" if char.lower() in "abcdefghijklmnopqrstuvwxyz" else RUSSIAN_ALPHABET
                shift = alphabet.index(key[key_index % len(key)])
                new_index = (alphabet.index(char.lower()) - shift) % len(alphabet)
                new_char = alphabet[new_index]
                decrypted += new_char.upper() if char.isupper() else new_char
                key_index += 1
            else:
                decrypted += char  # Сохраняем пробелы и другие символы

        return decrypted
    except Exception as e:
        raise ValueError(f"Ошибка при дешифровании Виженера: {str(e)}")