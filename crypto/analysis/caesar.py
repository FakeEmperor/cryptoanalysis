"""
Caesar encrypted text analysis
"""
import logging
from typing import Union, Set

from crypto.algo.caesar import CaesarCipher
from crypto.analysis.base import BaseAnalyzer, AnalyzerResult
from crypto.analysis.language.frequency import Language, coincidence_index


logger = logging.getLogger(__name__)


class CaesarAnalyzer(BaseAnalyzer):

    def __init__(self, language: Language):
        self.language = language
        self.caesar_cipher = CaesarCipher(language.alphabet)

    def decrypt(self, crypttext: str, key: Union[int, str], algorithm: str = None, **kwargs) -> str:
        return self.caesar_cipher.decrypt(crypttext, key=key)

    def fit(self, crypttext: str, **kwargs) -> AnalyzerResult:
        crypttext = crypttext.upper()
        best_keys: Set[str] = set()
        best_score = None

        for char in self.language[1]:
            score = coincidence_index(self.caesar_cipher.decrypt(crypttext, char), language=self.language)
            logger.debug(f"Key {char} has coincidence score {score:.3f}")

            if best_score is None or score > best_score:
                logger.info(f"Key {char} is the best key so far (score = {score:.3f} vs. best_score = {best_score})")
                best_score = score
                best_keys = {char}
            elif abs(score - best_score) < 0.001:
                best_keys.add(char)
        return AnalyzerResult(best_keys, best_score=best_score, score_is_loss=False)
