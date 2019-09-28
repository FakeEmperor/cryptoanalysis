"""

"""
from logging import getLogger
from typing import Sequence, Union, Any, List, Callable

from crypto.algo.base import Cipher
from crypto.algo.caesar import CaesarCipher
from crypto.algo.utils import from_alphabet

logger = getLogger(__name__)


class VigenereCipher(Cipher):

    def __init__(self, alphabet: Union[str, Sequence[str]]):
        self.caesar = CaesarCipher(alphabet)

    def to_text(self, data: str) -> str:
        return data

    @property
    def alphabet(self) -> str:
        return self.caesar.alphabet

    @staticmethod
    def _verify_key(key: Union[str, List[int]]):
        if not isinstance(key, (str, list)):
            raise ValueError(f"Key {key} should be a string or a list of integers")
        if not len(key):
            raise ValueError("Zero-length key")

    def _crypt(self, data: str, key: Union[str, List[int]], callback: Callable[[str, Union[str, int]], str]) -> str:
        self._verify_key(key)
        subtexts = []

        for i, subkey in enumerate(key):
            subtexts.append(callback(data[i::len(key)], subkey))

        ptext = []
        for i in range(len(subtexts[0])):
            for st in subtexts:
                if i < len(st):
                    ptext.append(st[i])
        return "".join(ptext)

    def encrypt(self, data: str, key: Union[str, List[int]]) -> str:
        return self._crypt(data, key, self.caesar.encrypt)

    def decrypt(self, data: str, key: Union[str, List[int]]):
        self._verify_key(key)
        subtexts = []

        for i, subkey in enumerate(key):
            subtexts.append(self.caesar.decrypt(data[i::len(key)], subkey))

        ptext = []
        for i in range(len(subtexts[0])):
            for st in subtexts:
                if i < len(st):
                    ptext.append(st[i])
        return "".join(ptext)
