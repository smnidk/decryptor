import string

RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET = string.ascii_lowercase + RUSSIAN_ALPHABET

def caesar_encrypt(text, shift):
    try:
        if not isinstance(shift, int):
            raise ValueError("Сдвиг должен быть целым числом.")
        encrypted = ""
        
        for char in text:
            if char.lower() in ALPHABET:
                alphabet = string.ascii_lowercase if char.lower() in string.ascii_lowercase else RUSSIAN_ALPHABET
                new_index = (alphabet.index(char.lower()) + shift) % len(alphabet)
                new_char = alphabet[new_index]
                encrypted += new_char.upper() if char.isupper() else new_char
            else:
                encrypted += char
        
        return encrypted
    except Exception as e:
        raise ValueError(f"Ошибка при шифровании Цезаря: {str(e)}")

def caesar_decrypt(text, shift):
    try:
        if not isinstance(shift, int):
            raise ValueError("Сдвиг должен быть целым числом.")
        decrypted = ""
        
        for char in text:
            if char.lower() in ALPHABET:
                alphabet = string.ascii_lowercase if char.lower() in string.ascii_lowercase else RUSSIAN_ALPHABET
                new_index = (alphabet.index(char.lower()) - shift) % len(alphabet)
                new_char = alphabet[new_index]
                decrypted += new_char.upper() if char.isupper() else new_char
            else:
                decrypted += char  # Сохраняем пробелы и другие символы
        
        return decrypted
    except Exception as e:
        raise ValueError(f"Ошибка при дешифровании Цезаря: {str(e)}")

def caesar_bruteforce(text):
    """Перебирает все сдвиги и возвращает список возможных расшифровок."""
    try:
        return {shift: caesar_decrypt(text, shift) for shift in range(1, len(RUSSIAN_ALPHABET))}
    except Exception as e:
        raise ValueError(f"Ошибка при переборе сдвигов: {str(e)}")