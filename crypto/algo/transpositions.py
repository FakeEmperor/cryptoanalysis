from logging import getLogger
from typing import List, Any

import pandas as pd

from crypto.algo.base import Cipher
from crypto.utils import from_df

logger = getLogger(__name__)


class DoubleTranspositionCipher(Cipher):

    @classmethod
    def to_text(cls, data: pd.DataFrame) -> str:
        return "".join(from_df(data))

    @classmethod
    def decrypt(cls, data: pd.DataFrame, k1: List[int]=None, k2: List[int]=None):
        if not k1 and not k2:
            logger.warning("No key was passed to decode, leaving as is")
            return data
        data = data.reindex(index=k1, columns=k2)
        return data

    @classmethod
    def encrypt(cls, data: pd.DataFrame, k1: List[int]=None, k2: List[int]=None):
        return cls.decrypt(data, k1, k2)
