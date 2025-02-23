from frequency import frequency_analysis
from caesar import caesar_bruteforce
from text_utils import clean_text
from vigenere import vigenere_decrypt


def main():
    text = input("Введите зашифрованный текст: ")
    key = input("Введите ключ для Виженера: ")
    cleaned_text = clean_text(text)

    print("\nАнализ частоты букв:")
    print(frequency_analysis(cleaned_text))

    print("\nВозможные расшифровки шифра Цезаря:")
    for shift, decrypted in caesar_bruteforce(cleaned_text).items():
        print(f"Сдвиг {shift}: {decrypted}")
    
    print("\nРасшифрованный текст (Виженер):")
    print(vigenere_decrypt(cleaned_text, key))

if __name__ == "__main__":
    main()
