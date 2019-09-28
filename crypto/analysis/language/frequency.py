# Loads in the following format from here:
# http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/
import json
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path
from typing import Dict, Tuple, Union, Callable, Iterable, Any, Sequence, Optional

logger = getLogger(__name__)


@dataclass
class GramStat:
    ngrams: Dict[str, float]
    min_frequency: Tuple[str, float] = field(init=False, default=None)
    max_frequency: Tuple[str, float] = field(init=False, default=None)

    def __post_init__(self):
        self.min_frequency = min(self.items(), key=lambda x: x[1])
        self.max_frequency = max(self.items(), key=lambda x: x[1])

    def __getitem__(self, item: str) -> float:
        return self.ngrams[item]

    def __iter__(self):
        return iter(self.ngrams)

    def keys(self) -> Iterable[str]:
        return self.ngrams.keys()

    def values(self) -> Iterable[float]:
        return self.ngrams.values()

    def items(self) -> Iterable[Tuple[str, float]]:
        return self.ngrams.items()

    def get(self, item: str, default: Any = None):
        return self.ngrams.get(item, default)

    @property
    def n(self):
        return len(next(self.ngrams))

    @classmethod
    def process(cls, ngrams: Dict[str, int], total_count: int = None,
                percentage: bool = True, sort: bool = False) -> 'GramStat':
        coef = 100.0 if percentage else 1.0
        if total_count is None:
            total_count = sum(ngrams.values())
        data = [(ngram, coef * count / total_count) for ngram, count in ngrams.items()]
        if sort:
            return cls(OrderedDict(sorted(data, key=lambda x: x[1], reverse=True)))
        return cls(dict(data))

    @classmethod
    def from_file(cls, path: Path, encoding: str = None, mapping: Dict[str, str] = None,
                  percentage: bool = True, sort: bool = False) -> 'GramStat':
        ngrams = defaultdict(int)
        total_count = 0
        with path.open(encoding=encoding) as f:
            for line in f:
                ngram, count = line.strip().split()
                if mapping:
                    for from_char, to_char in mapping.items():
                        ngram = ngram.replace(from_char, to_char)
                count = int(count)
                ngrams[ngram] += count
                total_count += count
        return cls.process(ngrams, total_count=total_count, percentage=percentage, sort=sort)

    @classmethod
    def frequencies(cls, text: str, n: int, mapping: Dict[str, str] = None) -> Tuple[Dict[str, int], int, str]:
        if n <= 0:
            raise ValueError("N should be a positive number!")
        if mapping:
            for from_char, to_char in mapping.items():
                text = text.replace(from_char, to_char)
        ngrams = zip(*[text[i:] for i in range(n)])
        ngrams = ["".join(ngram) for ngram in ngrams]
        counts = defaultdict(int)
        for ngram in ngrams:
            counts[ngram] += 1
        total_count = len(ngrams)
        return counts, total_count, text

    @classmethod
    def from_text(cls, text: str, n: int, mapping: Dict[str, str] = None,
                  percentage: bool = True, sort: bool = False) -> 'GramStat':
        if n <= 0:
            raise ValueError("N should be a positive number!")
        counts, total_count, _ = cls.frequencies(text, n=n, mapping=mapping)
        return cls.process(counts, total_count=total_count, percentage=percentage, sort=sort)


@dataclass
class IndicesOfCoincidence:
    natural: float


@dataclass
class Language:
    GRAMS = {
        "monograms": 1,
        "bigrams": 2,
        "trigrams": 3,
        "quadgrams": 4,
    }

    name: str
    root: Path
    mapping: Dict[str, str] = None
    encoding: str = None
    percentage: bool = True
    sort: bool = True
    language_data: Dict[str, Any] = field(init=False)
    grams: Dict[str, GramStat] = field(init=False)
    coincidence: IndicesOfCoincidence = field(init=False)

    def __post_init__(self):
        """
        Loads all language statistics
        """
        self.grams = {}
        logger.debug(f"Loading language data from json file")
        self.language_data = json.loads((self.root / f"{self.name}.json").read_text())
        self.coincidence = IndicesOfCoincidence(**self.language_data["coincidence"])
        for gram in self.GRAMS:
            path = self.root / f"{self.name}_{gram}.txt"
            logger.debug(f"Trying to load gram {gram} @ {str(path)}")
            self.grams[gram] = GramStat.from_file(path, encoding=self.encoding, mapping=self.mapping,
                                                  percentage=self.percentage, sort=self.sort)

    def __getitem__(self, ngram: Union[str, int]) -> GramStat:
        if isinstance(ngram, int):
            for gram, n in self.GRAMS.items():
                if n == ngram:
                    ngram = gram
                    break
            else:
                raise KeyError(f"Cannot find ngram '{ngram}' (int value)")
        return self.grams[ngram]

    @property
    def alphabet(self) -> Sequence[str]:
        """
        Lower-cased alphabet sequence.
        """
        return sorted(map(lambda x: x.upper(), self["monograms"].keys()))


def ngram_fitness(data: str, n: Union[str, int], language: Language,
                  loss: Callable[[GramStat, GramStat], float]) -> Tuple[GramStat, float]:
    actual_grams = language[n]
    predicted_grams = GramStat.from_text(data, n=n, mapping=language.mapping, percentage=language.percentage)
    return predicted_grams, loss(predicted_grams, actual_grams)


def coincidence_index(text: str, *, language: Optional[Language]) -> float:
    """
    Calculates coincidence index:
    https://en.wikipedia.org/wiki/Index_of_coincidence

    :param text:      Data to calculate for
    :param language:  Optional. Language with probabilities required.
                      If not specified
    :return:          I(data) if language is not specified: I(data) = sum(p^2), else I(data, language) = sum(p * p_language)
    """
    freqs, _, text = GramStat.frequencies(text, n=1, mapping=language.mapping if language else None)
    coef = 0.01 if language is not None and language.percentage else 1
    coincidence = sum((
        freq / len(text) * (language[1][ngram] if language is not None else freq / len(text)) * coef
        for ngram, freq in freqs.items()
    ))
    return coincidence
