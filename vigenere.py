def vigenere_encrypt(text, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    key = key.lower()
    encrypted = ""
    key_index = 0

    for char in text:
        if char.lower() in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            new_index = (alphabet.index(char.lower()) + shift) % len(alphabet)
            new_char = alphabet[new_index]
            encrypted += new_char.upper() if char.isupper() else new_char
            key_index += 1
        else:
            encrypted += char

    return encrypted

def vigenere_decrypt(text, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    key = key.lower()
    decrypted = ""
    key_index = 0

    for char in text:
        if char.lower() in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            new_index = (alphabet.index(char.lower()) - shift) % len(alphabet)
            new_char = alphabet[new_index]
            decrypted += new_char.upper() if char.isupper() else new_char
            key_index += 1
        else:
            decrypted += char

    return decrypted
