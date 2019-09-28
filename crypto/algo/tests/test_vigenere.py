import unittest

from crypto.algo.vigenere import VigenereCipher


class TestVigenereCipher(unittest.TestCase):
    def setUp(self) -> None:
        self.cipher = VigenereCipher("1234")

    def test_encrypt_decrypt_smoke(self):
        plaintext = "321"
        self.assertEqual(plaintext, self.cipher.to_text(self.cipher.decrypt(self.cipher.encrypt(plaintext, "23"), "23")))

    def test_to_text_is_noop(self):
        self.assertEqual("1234", self.cipher.to_text("1234"))

    def test_encrypt_zero_key(self):
        plaintext = "112233"
        self.assertEqual(plaintext, self.cipher.to_text(self.cipher.encrypt(plaintext, "11")))

    def test_encrypt_int(self):
        plaintext = "321"
        self.assertEqual("442", self.cipher.encrypt(plaintext, [1, 2]))

    def test_encrypt_character(self):
        plaintext = "321123"
        # test invalid length
        with self.assertRaises(ValueError):
            self.cipher.encrypt(plaintext, [])
        # test invalid char
        with self.assertRaises(ValueError):
            self.cipher.encrypt(plaintext, "aa")
        # test valid char "3" that shifts to two ["1" -> 0 (its index), "2" -> 1 and so on]
        self.assertEqual("244311", self.cipher.encrypt(plaintext, "43"))
