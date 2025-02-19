from math import gcd
from functools import reduce

def kasiski_examination(ciphertext):
    """ Метод Касиски для определения длины ключа. """
    min_length = 3  # Минимальная длина повторяющихся последовательностей
    sequences = {}

    for i in range(len(ciphertext) - min_length):
        seq = ciphertext[i:i+min_length]
        if seq in sequences:
            sequences[seq].append(i)
        else:
            sequences[seq] = [i]

    distances = []
    for seq, positions in sequences.items():
        if len(positions) > 1:
            for j in range(len(positions) - 1):
                distances.append(positions[j+1] - positions[j])

    # Поиск наибольшего общего делителя (НОД) между расстояниями
    if distances:
        key_length = reduce(gcd, distances)
        return key_length if key_length > 1 else None
    return None
