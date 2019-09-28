import copy
import itertools
import random
from typing import Iterator, List, Iterable, Set, Tuple, Any

import pandas as pd


def to_df(text: str, size: Tuple[int, int]) -> pd.DataFrame:
    """
    Convert a line of text into a two dimensional array

    :param text:
    :param size:
    :return:
    """
    data = []
    for i in range(size[0]):
        row = []
        for j in range(size[1]):
            row.append(text[i*size[1]+j])
        data.append(row)
    return pd.DataFrame(data)


def from_df(matrix: pd.DataFrame) -> List[str]:
    """
    Convert matrix to a text lines array

    :param matrix:
    :return:
    """
    texts = []
    for i in matrix.index:
        texts.append("".join([s for s in matrix.loc[i]]))
    return texts


def swap_elements(a: List[int], swap: Tuple[int, int]):
    a = copy.copy(a)
    tmp = a[swap[0]]
    a[swap[0]] = a[swap[1]]
    a[swap[1]] = tmp
    return a
