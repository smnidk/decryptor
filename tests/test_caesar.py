import pytest
from decryptor.caesar import caesar_encrypt, caesar_decrypt, caesar_bruteforce
import logging


@pytest.mark.parametrize(
    "text,shift,expected",
    [
        ("abc", 3, "def"),
        ("XYZ", 5, "CDE"),
        ("Hello, World!", 7, "Olssv, Dvysk!"),
        ("z", 1, "a"),
        ("a", 25, "z"),
    ],
)
def test_valid_encryption(text, shift, expected):
    assert caesar_encrypt(text, shift) == expected


@pytest.mark.parametrize(
    "text,shift,expected",
    [
        ("def", 3, "abc"),
        ("CDE", 5, "XYZ"),
        ("Olssv, Dvysk!", 7, "Hello, World!"),
    ],
)
def test_valid_decryption(text, shift, expected):
    assert caesar_decrypt(text, shift) == expected


def test_invalid_inputs():
    with pytest.raises(TypeError):
        caesar_encrypt(123, 5)
    with pytest.raises(TypeError):
        caesar_decrypt("test", "invalid")


def test_bruteforce():
    encrypted = caesar_encrypt("secret", 15)
    results = caesar_bruteforce(encrypted)
    assert results[15] == "secret"


def test_edge_cases():
    assert caesar_encrypt("abc", 30) == caesar_encrypt("abc", 4)
    assert caesar_encrypt("def", -3) == "abc"


def test_error_logging(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(TypeError):
        caesar_encrypt(123, 5)

    assert any(
        "Ошибка в caesar_encrypt" in record.message and record.exc_info[0] is TypeError
        for record in caplog.records
    )


def test_non_alpha_chars():
    assert caesar_encrypt("!@#$%^", 10) == "!@#$%^"
    assert caesar_decrypt("!@#$%^", 10) == "!@#$%^"
