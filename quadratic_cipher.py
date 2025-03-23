def quadratic_encrypt(text, a, b, c, m):
    """ Шифрование квадратичным шифром. """
    encrypted = []
    for char in text:
        x = ord(char)
        encrypted_char = (a * x**2 + b * x + c) % m
        encrypted.append(encrypted_char)
    return encrypted

def quadratic_decrypt(encrypted, a, b, c, m):
    """ Дешифрование квадратичным шифром. """
    from sympy import symbols, Eq, solve

    decrypted = []
    x = symbols('x')
    for enc_char in encrypted:
        # Решаем квадратное уравнение для каждого зашифрованного символа
        equation = Eq(a * x**2 + b * x + c, enc_char % m)
        solutions = solve(equation, x)
        # Ищем допустимое целочисленное решение
        for sol in solutions:
            if sol.is_integer and 0 <= sol <= 255:  # Проверяем, что решение в диапазоне ASCII
                decrypted.append(chr(int(sol)))
                break
        else:
            # Если решение не найдено, добавляем пробел (или можно выбросить ошибку)
            decrypted.append(' ')
    return ''.join(decrypted)

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python quadratic_cipher.py <mode> <params>")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == 'e':
        text = input("Введите текст для шифрования: ")
        a = int(input("Введите a (не 0): "))
        b = int(input("Введите b: "))
        c = int(input("Введите c: "))
        m = int(input("Введите m (256 или больше, лучше простое число): "))
        encrypted = quadratic_encrypt(text, a, b, c, m)
        print("Зашифрованный текст:", encrypted)

    elif mode == 'd':
        encrypted = input("Введите зашифрованные данные (через запятую): ")
        encrypted = [int(x) for x in encrypted.split(',')]
        a = int(input("Введите a (не 0): "))
        b = int(input("Введите b: "))
        c = int(input("Введите c: "))
        m = int(input("Введите m (256 или больше, лучше простое число): "))
        decrypted = quadratic_decrypt(encrypted, a, b, c, m)
        print("Расшифрованный текст:", decrypted)

    else:
        print("Invalid mode. Use 'e' for encryption or 'd' for decryption.")
        sys.exit(1)

if __name__ == "__main__":
    main()