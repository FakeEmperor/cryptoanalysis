"""
Language processing utilities:
- ENGLISH_FREQUENCY_TABLE

"""
import math
import numpy as np
from collections import Counter, OrderedDict, defaultdict
from logging import getLogger
from typing import NamedTuple, Dict, List

logger = getLogger(__name__)
ENGLISH_FREQUENCY_TABLE = {
    'A': 8.12 * 10**-2,
    'B': 1.49 * 10**-2,
    'C': 2.71 * 10**-2,
    'D': 4.32 * 10**-2,
    'E': 12.02 * 10**-2,
    'F': 2.30 * 10**-2,
    'G': 2.03 * 10**-2,
    'H': 5.92 * 10**-2,
    'I': 7.31 * 10**-2,
    'J': 0.10 * 10**-2,
    'K': 0.69 * 10**-2,
    'L': 3.98 * 10**-2,
    'M': 2.61 * 10**-2,
    'N': 6.95 * 10**-2,
    'O': 7.68 * 10**-2,
    'P': 1.82 * 10**-2,
    'Q': 0.11 * 10**-2,
    'R': 6.02 * 10**-2,
    'S': 6.28 * 10**-2,
    'T': 9.10 * 10**-2,
    'U': 2.88 * 10**-2,
    'V': 1.11 * 10**-2,
    'W': 2.09 * 10**-2,
    'X': 0.17 * 10**-2,
    'Y': 2.11 * 10**-2,
    'Z': 0.07 * 10**-2,
}


class TextDescriptor(NamedTuple):
    entropy: float
    frequencies: Dict[str, float]
    length: int

    @classmethod
    def describe(cls, text: str) -> 'TextDescriptor':
        counts = Counter(text)
        length = len(text)
        freqs = {}
        entropy = 0.0
        for letter, count in counts.items():
            p = float(count) / length
            freqs[letter] = p
            entropy -= p*math.log2(p)
        return TextDescriptor(length=length, entropy=entropy, frequencies=freqs)


def match_table(a: Dict[str, float], b: Dict[str, float],
                rtol: float=0.05, atol: float=0.01) -> Dict[str, List[str]]:
    """
    Tries to match one frequency table to another

    :return: a dictionary of matches letters from a -> b
    """
    a = OrderedDict(sorted(a.items(), key=lambda t: t[1]))
    b = OrderedDict(sorted(b.items(), key=lambda t: t[1]))
    mapping = defaultdict(list)
    for a_key, a_freq in a.items():
        for b_key, b_freq in b.items():
            #logger.debug(f"Comparing {a_key}-{b_key} ({a_freq} vs. {b_freq})")
            if np.allclose(a_freq, b_freq, rtol=rtol, atol=atol):
                logger.debug(f"Mapping {a_key}->{b_key} ({a_freq} -> {b_freq})")
                mapping[a_key].append(b_key)
        if len(mapping[a_key]) == 0:
            logger.warning(f"Not found any letters for letter {a_key} ({a_freq})")
    return mapping


# ASSERTIONS on the static data defined above
assert abs(sum(ENGLISH_FREQUENCY_TABLE.values())-1) < 0.0001, \
    f"Frequencies in ENGLISH_FREQUENCY_TABLE should sum up to 1 (sum is {sum(ENGLISH_FREQUENCY_TABLE.values())})"
