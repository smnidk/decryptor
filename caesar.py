# caesar.py (модифицированная версия)
import logging
import string

# Настройка логгирования
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def caesar_encrypt(text, shift):
    try:
        if not isinstance(text, str):
            raise TypeError("Текст должен быть строкой")
        if not text:
            raise ValueError("Пустая строка")

        alphabet = string.ascii_lowercase
        encrypted = []

        for char in text:
            if char.lower() in alphabet:
                original_index = alphabet.index(char.lower())
                new_index = (original_index + shift) % len(alphabet)
                new_char = alphabet[new_index]
                encrypted.append(new_char.upper() if char.isupper() else new_char)
            else:
                encrypted.append(char)

        return "".join(encrypted)
    except Exception as e:
        logger.error(f"Ошибка в caesar_encrypt: {str(e)}", exc_info=True)
        raise


def caesar_decrypt(text, shift):
    try:
        if not isinstance(text, str):
            raise TypeError("Текст должен быть строкой")
        if not isinstance(shift, int):
            raise TypeError("Сдвиг должен быть целым числом")

        return caesar_encrypt(text, -shift)

    except Exception as e:
        logger.error(f"Ошибка в caesar_decrypt: {str(e)}", exc_info=True)
        raise


def caesar_bruteforce(text):
    try:
        if not isinstance(text, str):
            raise TypeError("Текст должен быть строкой")

        return {shift: caesar_decrypt(text, shift) for shift in range(1, 26)}

    except Exception as e:
        logger.error(f"Ошибка в caesar_bruteforce: {str(e)}", exc_info=True)
        raise
