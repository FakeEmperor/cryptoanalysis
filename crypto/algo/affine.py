"""

"""
from typing import Union, Sequence

from math import gcd


class AffineEncryptor:
    def __init__(self, alphabet: Union[str, Sequence[str]]):
        alphabet = "".join(alphabet) if not isinstance(alphabet, str) else alphabet
        if len(alphabet) != len(set(alphabet)):
            raise ValueError("Passed alphabet must not contain duplicate characters!")
        self.alphabet = alphabet

    def encrypt(self, data: str, factor, shift, **kwargs) -> str:
        return self.__encrypt(data, factor, shift)

    def decrypt(self, data: str, factor, shift, **kwargs) -> str:
        g = gcd(factor, len(self.alphabet))
        x = factor // g
        return self.__encrypt(ctext, x, -shift)

    def __encrypt(self, ptext, factor, shift):
        while shift < 0:
            shift += len(self.alphabet)
        ctext = []
        for c in ptext:
            pos = self.alphabet.find(c)
            if pos == -1:
                raise Exception("Text not in alphabet")
            ctext.append(self.alphabet[(pos * factor + shift) % len(self.alphabet)])
        return "".join(ctext)
