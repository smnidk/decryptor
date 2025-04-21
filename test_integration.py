import unittest
from unittest.mock import patch
import caesar
import vigenere
import logging

# Настройка логгирования
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)


def integrated_cipher_processor(text, caesar_shift, vigenere_key):
    try:
        caesar_result = caesar.caesar_encrypt(text, caesar_shift)
        vigenere_result = vigenere.vigenere_encrypt(caesar_result, vigenere_key)
        return vigenere_result
    except Exception as e:
        logging.error(f"Ошибка в integrated_cipher_processor: {str(e)}", exc_info=True)
        raise


class TestIntegratedCiphers(unittest.TestCase):
    def test_correct_data(self):
        result = integrated_cipher_processor("hello", 3, "key")
        self.assertEqual(result, "ulmyv")

    def test_empty_data(self):
        with self.assertRaises(ValueError):
            integrated_cipher_processor("", 3, "key")

    def test_zero_key(self):
        result = integrated_cipher_processor("hello", 0, "key")
        self.assertEqual(result, "rijvs")

    @patch("vigenere.vigenere_encrypt")
    def test_vigenere_called(self, mock_vigenere):
        mock_vigenere.return_value = "test"
        integrated_cipher_processor("test", 1, "key")
        self.assertTrue(mock_vigenere.called)

    def test_error_logging(self):
        with self.assertRaises(TypeError):
            integrated_cipher_processor(123, 1, "key")

        logging.shutdown()

        with open("error.log", "r") as f:
            log_content = f.read()
            self.assertIn("Текст должен быть строкой", log_content)
            self.assertIn("Ошибка в integrated_cipher_processor", log_content)


if __name__ == "__main__":
    unittest.main()
