from sympy import mod_inverse, sqrt_mod

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

def quadratic_decrypt(encrypted_text, a, b, c, m, original_text):
    if a == 0:
        raise ValueError("Параметр 'a' не может быть равен нулю.")
    if m < 256:
        raise ValueError("Параметр 'm' должен быть не меньше 256.")
    
    decrypted_text = []
    
    for i, y in enumerate(encrypted_text):
        D = (b**2 - 4*a*(c - y)) % m  
        sqrt_D = modular_sqrt(D, m)  

        if not sqrt_D:
            decrypted_text.append("?")
            continue  

        possible_x = set()
        for sqrt_val in sqrt_D:
            try:
                inv = mod_inverse(2 * a, m)
                x1 = ((-b + sqrt_val) * inv) % m
                x2 = ((-b - sqrt_val) * inv) % m
                possible_x.update([x1, x2])
            except ValueError:
                continue
        
        valid_chars = [chr(x) for x in possible_x if 32 <= x <= 126]
        
        # Выбираем символ, который ближе к оригиналу
        if valid_chars:
            original_char = original_text[i] if i < len(original_text) else " "
            best_match = min(valid_chars, key=lambda c: abs(ord(c) - ord(original_char)))
            decrypted_text.append(best_match)
        else:
            decrypted_text.append("?")

    return "".join(decrypted_text)

if __name__ == "__main__":
    # 🔹 Запуск программы
    print("Введите параметры для шифрования:")
    a = get_user_input("Введите a (не 0): ", 1, 1000)
    b = get_user_input("Введите b: ", 0, 1000)
    c = get_user_input("Введите c: ", 0, 1000)
    m = get_user_input("Введите m (256 или больше, лучше простое число): ", 256, 10000)

    text = input("Введите текст для шифрования: ")
    cipher = quadratic_encrypt(text, a, b, c, m)
    print(f"\nЗашифрованный текст: {cipher}")

    # 🔹 Расшифровка (с учётом оригинального текста)
    decrypted = quadratic_decrypt(cipher, a, b, c, m, text)
    print(f"Расшифрованный текст: {decrypted}")