import unittest
from caesar import caesar_encrypt, caesar_decrypt

class TestCaesarCipher(unittest.TestCase):
    def test_encrypt(self):
        self.assertEqual(caesar_encrypt("hello", 3), "khoor")
        self.assertEqual(caesar_encrypt("WORLD", 5), "BTWQI")
        self.assertEqual(caesar_encrypt("Hello, World!", 7), "Olssv, Dvysk!")

    def test_decrypt(self):
        self.assertEqual(caesar_decrypt("khoor", 3), "hello")
        self.assertEqual(caesar_decrypt("BTWQI", 5), "WORLD")
        self.assertEqual(caesar_decrypt("Olssv, Dvysk!", 7), "Hello, World!")

if __name__ == "__main__":
    unittest.main()