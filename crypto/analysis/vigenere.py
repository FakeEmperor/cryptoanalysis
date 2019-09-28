"""
Vigenere cipher analyzer
"""
import logging
from collections import OrderedDict
from typing import Union, Sequence, Dict

from crypto.algo.vigenere import VigenereCipher
from crypto.analysis.base import BaseAnalyzer, AnalyzerResult
from crypto.analysis.caesar import CaesarAnalyzer
from crypto.analysis.language.frequency import Language, coincidence_index


logger = logging.getLogger(__name__)


class VigenereAnalyzer(BaseAnalyzer):

    def __init__(self, language: Language, default_max_key_length: int = 10):
        self.caesar_analyzer = CaesarAnalyzer(language)
        self.vigenere_cipher = VigenereCipher(language.alphabet)
        self.default_max_key_length = default_max_key_length

    @property
    def language(self) -> Language:
        return self.caesar_analyzer.language

    def decrypt(self, crypttext: str, key: Union[str, Sequence[int]], **kwargs) -> str:
        return self.vigenere_cipher.decrypt(crypttext, key)

    def fit(self, crypttext: str, min_key_length: int = 1, max_key_length: int = None, **kwargs) -> AnalyzerResult:
        if max_key_length is None:
            max_key_length = min(self.default_max_key_length, len(crypttext))
        if min_key_length < 1:
            raise ValueError("Min key length could not be less than one")
        possible_lengths = self.fit_lengths(crypttext, min_key_length=min_key_length, max_key_length=max_key_length)

        best_keys = set()
        best_loss: float = None
        for length, index in possible_lengths.items():
            logger.info(f"Trying out length {length} with index {index}...")
            scores_sum = 0
            keys = []
            for cut_index in range(length):
                result = self.caesar_analyzer.fit(crypttext[cut_index::length])
                logger.info(f"Best keys for #{cut_index} so far: {result.best_keys}")
                if len(result.best_keys) > 1 and keys:
                    logger.warning(f"Caesar analyzer for cut index {cut_index} @ length {length} "
                                   f"returned {len(result.best_keys)} keys ({result.best_keys}). "
                                   f"We'll use all, which will produce key explosion to ({len(keys) * len(result.best_keys)})")
                if not keys:
                    keys = list(result.best_keys)
                else:
                    for i, key in enumerate(keys):
                        for key_char in result.best_keys:
                            keys[i] = key + key_char

                scores_sum += result.best_score
            coincidence_score = scores_sum / length
            loss = abs(self.language.coincidence.natural - coincidence_score)
            logger.debug(f"Found {len(keys)} with median coincidence loss of {loss:.3f} (score: {coincidence_score})")
            if best_loss is None or best_loss > loss:
                logger.info(f"Keys {keys} is the best key so far (loss = {loss:.3f} vs. best_loss = {best_loss})")
                best_loss = loss
                best_keys = set(keys)
            elif abs(best_loss - loss) <= 0.001:
                logger.info(f"Adding {keys} to the best keys")
                best_keys.union(keys)
        logger.info(f"Best keys after fitting: {best_keys} ({best_loss:.3f})")
        return AnalyzerResult(best_keys, best_loss, score_is_loss=True)

    def fit_lengths(self, crypttext: str, min_key_length: int, max_key_length: int) -> Dict[int, float]:
        key_lengths: Dict[int, float] = dict()
        for key_length in range(min_key_length, max_key_length + 1):
            indices = [
                coincidence_index(crypttext[text_cut_index::key_length], language=None)
                for text_cut_index in range(key_length)
            ]
            key_lengths[key_length] = sum(indices) / len(indices)

        return OrderedDict(sorted(key_lengths.items(), key=lambda x: x[1], reverse=True))
