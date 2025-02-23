import collections
import string

ENGLISH_LETTER_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 
    'Q': 0.10, 'Z': 0.07
}

def frequency_analysis(text):
    """Возвращает частоту букв в тексте."""
    text = text.upper()
    letter_counts = collections.Counter(c for c in text if c.isalpha())
    total = sum(letter_counts.values())
    return {char: (count / total * 100) for char, count in letter_counts.items()} if total > 0 else {}

def find_shift(freqs):
    """Определяет сдвиг по частотному анализу (наиболее частая буква = 'E')."""
    if not freqs:
        return 0
    most_frequent_letter = max(freqs, key=freqs.get)
    shift = (ord(most_frequent_letter) - ord('E')) % 26
    return shift

def find_vigenere_key(ciphertext, key_length):
    """Определяет ключ Виженера на основе частотного анализа."""
    key = []
    for i in range(key_length):
        subsequence = ciphertext[i::key_length]  # Извлекаем i-ю подгруппу букв
        freqs = frequency_analysis(subsequence)
        shift = find_shift(freqs)
        key.append(chr(ord('A') + shift))
    return "".join(key)
