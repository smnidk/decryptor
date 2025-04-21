import pytest
from unittest.mock import patch
from decryptor.aes_modified import generate_random_key, encrypt, decrypt


def test_generate_random_key_with_mock():
    with patch("secrets.token_hex") as mock_token:
        mock_token.return_value = "a1b2c3d4e5f6g7h8"
        key = generate_random_key()
        assert key == "a1b2c3d4e5f6g7h8"
        mock_token.assert_called_once_with(16)


def test_encrypt_with_mocked_keys():
    mock_keys = [b"1234567890abcdef", b"fedcba0987654321"]  
    with patch("decryptor.aes_modified.encrypt_block") as mock_encrypt:
        mock_encrypt.return_value = b"encrypted_data"
        data = b"secret_data"
        encrypted = encrypt(data, mock_keys, depth=2)
        expected_padded_data = data + b"\x05" * 5
        mock_encrypt.assert_called_with(expected_padded_data, mock_keys)
        assert encrypted == b"encrypted_data"
