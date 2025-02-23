import re

def clean_text(text):
    """Удаляет все символы, кроме букв, и приводит к нижнему регистру."""
    return re.sub(r'[^a-zA-Z]', '', text).lower()
