from triple_aes import generate_keys

def generate_keys_for_triple_aes():
    keys = generate_keys()
    print("Сгенерированные ключи:", keys)
    return keys