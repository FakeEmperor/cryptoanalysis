"""
Base interface
"""
from abc import ABC, abstractmethod
from typing import Any, Sequence, Union, Set


class Cipher(ABC):

    @abstractmethod
    def encrypt(self, data: Any, **kwargs) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def decrypt(self, data: Any, **kwargs) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def to_text(self, data: Any) -> str:
        raise NotImplementedError()
