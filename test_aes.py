import unittest
from unittest.mock import patch
from aes import main

class TestAES(unittest.TestCase):
    @patch('builtins.input', side_effect=['thisisasecretkey', 'Hello, World!'])
    def test_encryption_decryption(self, mock_input):
        with patch('builtins.print') as mock_print:
            main()
            # Debug output to see what is printed
            for call in mock_print.call_args_list:
                print(call)
            # Check if the encrypted text and decrypted text are printed
            self.assertTrue(any("Encrypted text:" in call[0][0] for call in mock_print.call_args_list))
            self.assertTrue(any("Decrypted text: Hello, World!" in call[0][0] for call in mock_print.call_args_list))

if __name__ == '__main__':
    unittest.main()