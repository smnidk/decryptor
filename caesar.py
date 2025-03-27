import string

RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET = string.ascii_lowercase + RUSSIAN_ALPHABET

def caesar_encrypt(text: str, shift: int) -> str:
    if not isinstance(shift, int):
        raise ValueError("Сдвиг должен быть целым числом.")
    
    encrypted = []
    
    for char in text:
        if char.lower() in ALPHABET:
            alphabet = string.ascii_lowercase if char.lower() in string.ascii_lowercase else RUSSIAN_ALPHABET
            new_index = (alphabet.index(char.lower()) + shift) % len(alphabet)
            new_char = alphabet[new_index]
            encrypted.append(new_char.upper() if char.isupper() else new_char)
        else:
            encrypted.append(char)
    
    return ''.join(encrypted)

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)

# Пример использования
if __name__ == "__main__":
    try:
        text = input("Введите текст: ")
        shift = int(input("Введите сдвиг: "))
        
        encrypted = caesar_encrypt(text, shift)
        print(f"Зашифрованный текст: {encrypted}")
        
        decrypted = caesar_decrypt(encrypted, shift)
        print(f"Расшифрованный текст: {decrypted}")
    
    except ValueError as e:
        print(f"Ошибка: {e}")