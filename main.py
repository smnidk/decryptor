from frequency import frequency_analysis
from caesar import caesar_bruteforce, caesar_decrypt
from text_utils import clean_text
from vigenere import vigenere_decrypt


def main():
    text = input("Введите зашифрованный текст: ")
    cleaned_text = clean_text(text)

    print("\nВыберите тип шифра:")
    print("1 - Шифр Цезаря")
    print("2 - Шифр Виженера")
    choice = input("Введите номер: ")

    if choice == "1":
        print("\nВыберите способ расшифровки Цезаря:")
        print("1 - Указать сдвиг")
        print("2 - Брутфорс (перебор всех вариантов)")
        caesar_choice = input("Введите номер: ")

        if caesar_choice == "1":
            shift = int(input("Введите сдвиг: "))
            print("\nРасшифрованный текст (Цезарь):")
            print(caesar_decrypt(cleaned_text, shift))
        elif caesar_choice == "2":
            print("\nВозможные расшифровки шифра Цезаря:")
            for shift, decrypted in caesar_bruteforce(cleaned_text).items():
                print(f"Сдвиг {shift}: {decrypted}")
        else:
            print("Некорректный выбор.")

    elif choice == "2":
        key = input("Введите ключ для Виженера: ")
        print("\nРасшифрованный текст (Виженер):")
        print(vigenere_decrypt(cleaned_text, key))

    else:
        print("Некорректный выбор.")

    print("\nАнализ частоты букв:")
    print(frequency_analysis(cleaned_text))


if __name__ == "__main__":
    main()
