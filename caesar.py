import string

def caesar_encrypt(text, shift):
    alphabet = string.ascii_lowercase
    encrypted = ""
    
    for char in text:
        if char.lower() in alphabet:
            new_index = (alphabet.index(char.lower()) + shift) % len(alphabet)
            new_char = alphabet[new_index]
            encrypted += new_char.upper() if char.isupper() else new_char
        else:
            encrypted += char
    
    return encrypted

def caesar_decrypt(text, shift):
    alphabet = string.ascii_lowercase
    decrypted = ""
    
    for char in text:
        if char.lower() in alphabet:
            new_index = (alphabet.index(char.lower()) - shift) % len(alphabet)
            new_char = alphabet[new_index]
            decrypted += new_char.upper() if char.isupper() else new_char
        else:
            decrypted += char
    
    return decrypted

def caesar_bruteforce(text):
    """Перебирает все сдвиги и возвращает список возможных расшифровок."""
    return {shift: caesar_decrypt(text, shift) for shift in range(1, 26)}
