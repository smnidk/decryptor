from sympy import mod_inverse, sqrt_mod
from collections import Counter
import string

# Частоты символов английского языка (в порядке убывания)
ENGLISH_FREQ = " etaoinshrdlcumwfgypbvkjxqz"


def get_user_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Введите число от {min_value} до {max_value}.")
        except ValueError:
            print("Ошибка! Введите целое число.")


def quadratic_encrypt(text, a, b, c, m):
    """Шифрование текста квадратичным шифром."""
    if a == 0:
        raise ValueError("Параметр 'a' не может быть равен нулю.")
    if m < 256:
        raise ValueError("Параметр 'm' должен быть не меньше 256.")
    return [(a * (ord(ch) ** 2) + b * ord(ch) + c) % m for ch in text]


def modular_sqrt(a, p):
    """Находит корень a по модулю p, если существует."""
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    return sorted(sqrt_mod(a, p, all_roots=True))


def get_best_char(candidates):
    """Выбирает наиболее вероятный символ из кандидатов на основе частотного анализа."""
    if not candidates:
        return "?"

    # Предпочтение букв и пробела
    for char in candidates:
        if char in ENGLISH_FREQ:
            return char

    # Если нет букв, выбираем первый печатаемый символ
    return candidates[0]


def quadratic_decrypt(encrypted_text, a, b, c, m):
    """Дешифрование квадратичного шифра с выбором оптимального варианта."""
    if a == 0:
        raise ValueError("Параметр 'a' не может быть равен нулю.")
    if m < 256:
        raise ValueError("Параметр 'm' должен быть не меньше 256.")

    decrypted_text = []

    for y in encrypted_text:
        D = (b**2 - 4 * a * (c - y)) % m
        sqrt_D = modular_sqrt(D, m)

        possible_x = set()
        if sqrt_D:
            for sqrt_val in sqrt_D:
                try:
                    inv = mod_inverse(2 * a, m)
                    x1 = ((-b + sqrt_val) * inv) % m
                    x2 = ((-b - sqrt_val) * inv) % m
                    possible_x.update([x1, x2])
                except ValueError:
                    continue

        # Фильтрация по печатаемым ASCII-символам (32-126)
        valid_chars = [chr(x) for x in possible_x if 32 <= x <= 126]

        # Выбираем лучший вариант
        decrypted_text.append(get_best_char(valid_chars) if valid_chars else "?")

    return "".join(decrypted_text)


if __name__ == "__main__":
    print("Введите параметры для шифрования:")
    a = get_user_input("Введите a (не 0): ", 1, 1000)
    b = get_user_input("Введите b: ", 0, 1000)
    c = get_user_input("Введите c: ", 0, 1000)
    m = get_user_input("Введите m (256 или больше, лучше простое число): ", 256, 10000)

    text = input("Введите текст для шифрования: ")
    cipher = quadratic_encrypt(text, a, b, c, m)
    print(f"\nЗашифрованный текст: {cipher}")
