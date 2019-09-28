import unittest

from crypto.algo.caesar import CaesarCipher


class TestCaesarCipher(unittest.TestCase):
    def setUp(self) -> None:
        self.cipher = CaesarCipher("1234")

    def test_encrypt_decrypt_smoke(self):
        plaintext = "321"
        self.assertEqual(plaintext, self.cipher.to_text(self.cipher.decrypt(self.cipher.encrypt(plaintext, 1), 1)))

    def test_to_text_is_noop(self):
        self.assertEqual("1234", self.cipher.to_text("1234"))

    def test_encrypt_zero_key(self):
        plaintext = "112233"
        self.assertEqual(plaintext, self.cipher.to_text(self.cipher.encrypt(plaintext, 0)))

    def test_encrypt_int(self):
        plaintext = "321"
        self.assertEqual("432", self.cipher.encrypt(plaintext, 1))

    def test_encrypt_character(self):
        # test invalid length
        plaintext = "321"
        with self.assertRaises(ValueError):
            self.cipher.encrypt(plaintext, "11")
        # test invalid char
        with self.assertRaises(ValueError):
            self.cipher.encrypt(plaintext, "a")
        # test valid char "3" that shifts to two ["1" -> 0 (its index), "2" -> 1 and so on]
        self.assertEqual("143", self.cipher.encrypt(plaintext, "3"))
