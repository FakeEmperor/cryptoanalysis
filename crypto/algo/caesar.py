"""
Caesar cipher implementation:

"""
from typing import Any, Union, Sequence

from crypto.algo.base import Cipher
from crypto.algo.utils import from_alphabet


class CaesarCipher(Cipher):

    def to_text(self, data: str) -> str:
        return data

    def __init__(self, alphabet: Union[str, Sequence[str]]):
        self.alphabet = from_alphabet(alphabet, lower=True)

    def encrypt(self, data: str, key: Union[str, int], **kwargs) -> Any:
        if isinstance(key, str):
            key = self._alpha_to_shift(key)
        return self._encrypt_int(data, key)

    def decrypt(self, data: str, key: Union[str, int], **kwargs) -> Any:
        if isinstance(key, str):
            key = self._alpha_to_shift(key)
        return self._encrypt_int(data, -key)

    def _encrypt_int(self, data: str, key: int):
        key = key % len(self.alphabet)

        ctext = []

        for c in data:
            pos = self.alphabet.find(c)
            if pos == -1:
                raise RuntimeError(f"Character '{c}' is not in the alphabet")
            ctext.append(self.alphabet[(pos + key) % len(self.alphabet)])
        return "".join(ctext)

    def _alpha_to_shift(self, key: str):
        if len(key) != 1:
            raise ValueError(f"Key {key} is not a single character required by {self.__class__.__name__}")
        shift = self.alphabet.find(key.upper())
        if shift == -1:
            raise ValueError(f"Key {key} is not in the alphabet")
        return shift
