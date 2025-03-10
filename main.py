from aes import aes_encrypt, aes_decrypt
from triple_aes import triple_aes_encrypt, triple_aes_decrypt, generate_keys

def main():
    while True:
        print("\nВыберите действие:")
        print("1. Зашифровать AES")
        print("2. Расшифровать AES")
        print("3. Зашифровать тройным AES")
        print("4. Расшифровать тройным AES")
        print("5. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            text = input("Введите текст для шифрования: ").strip()
            key = input("Введите ключ: ").strip()
            print("Зашифрованный текст:", aes_encrypt(text, key))

        elif choice == "2":
            text = input("Введите зашифрованный текст: ").strip()
            key = input("Введите ключ: ").strip()
            print("Расшифрованный текст:", aes_decrypt(text, key))

        elif choice == "3":
            text = input("Введите текст для шифрования: ").strip()
            key_choice = input("Введите '1' для ввода трех ключей или '2' для генерации случайных ключей: ").strip()
            if key_choice == "1":
                keys = [input(f"Введите ключ {i+1}: ").strip() for i in range(3)]
            elif key_choice == "2":
                keys = generate_keys()
                print("Сгенерированные ключи:", keys)
            else:
                print("Ошибка: Неверный ввод, попробуйте снова.")
                continue
            print("Зашифрованный текст:", triple_aes_encrypt(text, keys))

        elif choice == "4":
            text = input("Введите зашифрованный текст: ").strip()
            keys = [input(f"Введите ключ {i+1}: ").strip() for i in range(3)]
            print("Расшифрованный текст:", triple_aes_decrypt(text, keys))

        elif choice == "5":
            print("Выход...")
            break

        else:
            print("Ошибка: Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()