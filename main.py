def get_keys(num_keys):
    """ Функция получения ключей от пользователя. """
    from aes_modified import string_to_key
    from Crypto.Random import get_random_bytes

    keys = []
    choice = input("Вы хотите ввести ключи вручную? (y/n): ").strip().lower()
    if choice == 'y':
        for i in range(num_keys):
            key_input = input(f"Введите ключ {i+1} (строка или hex): ")
            if all(c in '0123456789abcdefABCDEF' for c in key_input) and len(key_input) in (32, 48, 64):
                key = bytes.fromhex(key_input)  # Если введен hex, используем его
            else:
                key = string_to_key(key_input)  # Иначе, преобразуем строку в ключ
            keys.append(key)
    else:
        keys = [get_random_bytes(16) for _ in range(num_keys)]
        print("Сгенерированные ключи:")
        for i, key in enumerate(keys):
            print(f"Ключ {i+1}: {key.hex()}")
    return keys

def main():
    while True:
        print("Выберите шифр:")
        print("1. Цезарь")
        print("2. Виженер")
        print("3. Квадратичный шифр")
        print("4. AES")
        print("5. Модифицированный AES")
        print("6. Выйти")
        
        choice = input("Введите номер шифра: ")
        
        if choice == '1':
            from caesar import caesar_encrypt, caesar_decrypt
            action = input("Шифрование (e) или дешифрование (d): ")
            text = input("Введите текст: ")
            shift = int(input("Введите сдвиг: "))
            if action == 'e':
                print(caesar_encrypt(text, shift))
            else:
                print(caesar_decrypt(text, shift))
        
        elif choice == '2':
            from vigenere import vigenere_encrypt, vigenere_decrypt
            action = input("Шифрование (e) или дешифрование (d): ")
            text = input("Введите текст: ")
            key = input("Введите ключ: ")
            if action == 'e':
                print(vigenere_encrypt(text, key))
            else:
                print(vigenere_decrypt(text, key))
        
        elif choice == '3':
            from quadratic_cipher import quadratic_encrypt, quadratic_decrypt
            action = input("Шифрование (e) или дешифрование (d): ")
            if action == 'e':
                text = input("Введите текст для шифрования: ")
                a = int(input("Введите a (не 0): "))
                b = int(input("Введите b: "))
                c = int(input("Введите c: "))
                m = int(input("Введите m (256 или больше, лучше простое число): "))
                print(quadratic_encrypt(text, a, b, c, m))
            else:
                encrypted = input("Введите зашифрованные данные (через запятую): ")
                encrypted = [int(x) for x in encrypted.split(',')]
                a = int(input("Введите a (не 0): "))
                b = int(input("Введите b: "))
                c = int(input("Введите c: "))
                m = int(input("Введите m (256 или больше, лучше простое число): "))
                print(quadratic_decrypt(encrypted, a, b, c, m))
        
        elif choice == '4':
            from aes import aes_encrypt, aes_decrypt
            action = input("Шифрование (e) или дешифрование (d): ")
            text = input("Введите текст: ")
            key = input("Введите ключ: ")
            if action == 'e':
                print(aes_encrypt(text, key))
            else:
                print(aes_decrypt(text, key))
        
        elif choice == '5':
            from aes_modified import encrypt, decrypt
            action = input("Шифрование (e) или дешифрование (d): ")
            if action == 'e':
                text = input("Введите текст: ").encode()  # Преобразуем текст в bytes
                num_keys = int(input("Введите количество ключей: "))
                depth = int(input("Введите количество предыдущих блоков для XOR: "))
                keys = get_keys(num_keys)
                print(encrypt(text, keys, depth).hex())
            else:
                encrypted_hex = input("Введите зашифрованные данные (hex): ")
                encrypted = bytes.fromhex(encrypted_hex)
                num_keys = int(input("Введите количество ключей: "))
                depth = int(input("Введите количество предыдущих блоков для XOR: "))
                keys = get_keys(num_keys)
                print(decrypt(encrypted, keys, depth).decode(errors='ignore'))
        
        elif choice == '6':
            print("Выход из программы.")
            break
        
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()