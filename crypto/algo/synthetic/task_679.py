"""
Task 679
"""
import base64
from dataclasses import dataclass
from typing import Dict, Any, Union, Tuple

from crypto.algo.base import Cipher


@dataclass
class Differential:
    input_difference: Tuple[bytes, bytes]
    output_difference: Tuple[bytes, bytes]
    seen: int = 0

    def __post_init__(self):
        if len(self.input_difference[0]) != 1 or len(self.input_difference[1]) != 1:
            raise ValueError("Input values should be of length 1!")
        if len(self.output_difference[0]) != 1 or len(self.output_difference[1]) != 1:
            raise ValueError("Input values should be of length 1!")

    @property
    def input_delta(self) -> int:
        return self.input_difference[0][0] ^ self.input_difference[1][0]

    @property
    def output_delta(self) -> int:
        return self.output_difference[0][0] ^ self.output_difference[1][0]


class ExampleSPNCipher(Cipher):

    def __init__(self, sbox_upper: Dict[bytes, bytes], sbox_lower: Dict[bytes, bytes]):
        """
        Example cipher from: https://ioactive.com/differential-cryptanalysis-for-dummies/
        :param sbox_upper:
        :param sbox_lower:
        """
        self.sbox_upper = sbox_upper
        self.sbox_lower = sbox_lower

    @classmethod
    def key_from(cls, s: str) -> Tuple[bytes, bytes]:
        if len(s) % 2 != 0:
            raise ValueError("String length should be ")
        key = s.encode()
        return key[:len(s) // 2], key[len(s) // 2:]

    def encrypt(self, data: bytes, k0: bytes = None, k1: bytes = None, **kwargs) -> bytes:
        """

        :param data:
        :param k0:
        :param k1:
        :param kwargs:
        :return:
        """
        if len(k0) != len(k1):
            raise ValueError("Keys length is not equal.")
        if len(data) % len(k0) != 0:
            raise ValueError("Data length should be a multiplicative of key length")
        data = self.apply_key(data, k0)
        data = self.apply_sbox(data, self.sbox_upper)
        data = self.apply_key(data, k1)
        # BUG: this adds no security at all
        data = self.apply_sbox(data, self.sbox_lower)
        return data

    @classmethod
    def apply_key(cls, data: bytes, key: bytes):
        return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

    @classmethod
    def apply_sbox(cls, data: bytes, sbox: Dict[bytes, bytes]):
        for fr, to in sbox.items():
            data = data.replace(fr, to)
        return data

    def decrypt(self, data: bytes, **kwargs) -> str:
        pass

    def to_text(self, data: Union[bytes, str]) -> str:
        if isinstance(data, bytes):
            return base64.b64encode(data)
        return data


class Task679Cipher(Cipher):
    pass
