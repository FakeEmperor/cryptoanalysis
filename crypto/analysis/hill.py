from logging import getLogger
from typing import Callable, Any, Dict

from crypto.algo.base import Cipher
from crypto.analysis.base import AnalyzerResult, BaseAnalyzer, BaseKeyGenerator
from crypto.analysis.language.frequency import GramStat, Language, ngram_fitness
from crypto.analysis.language.utils import log_loss

import numpy as np

logger = getLogger(__name__)


class HillClimbingAnalyzer(BaseAnalyzer):

    def __init__(self, cipher: Cipher, key_generator: BaseKeyGenerator, key_argname: str,
                 language: Language, loss_fn: Callable[[GramStat, GramStat], float] = log_loss,
                 decrypt_kwargs: Dict[str, Any] = None):
        self.cipher = cipher
        self.key_generator = key_generator
        self.loss_fn = loss_fn
        self.language = language
        self.decrypt_kwargs = decrypt_kwargs or {}
        self.key_argname = key_argname

    def hill_climbing_round(self, crypttext: Any, current_key: Any, current_loss: float, n: int):
        best_loss = current_loss
        max_iters = len(current_key) * (len(current_key) - 1)
        for idx, key in enumerate(self.key_generator.hill_climbing(current_key)):
            logger.debug(f"[{idx + 1}/{max_iters}] Trying swapped key {key}...")
            data = self.decrypt(crypttext, key=key)
            _, loss = ngram_fitness(data, n=n, language=self.language, loss=self.loss_fn)
            logger.debug(f"Loss: {loss:.3f}, best: {best_loss:.3f}")
            if loss < best_loss:
                logger.debug(f"Found better key: {key} with loss {loss:.3f}!")
                return key, loss
        logger.debug(f"Did not found any better key for {current_key}!")
        return None, None

    def decrypt(self, crypttext: Any, key: Any, algorithm: str = None, **kwargs) -> str:
        data = self.cipher.decrypt(crypttext, **{self.key_argname: key}, **(self.decrypt_kwargs or {}))
        return self.cipher.to_text(data)

    def hill_climbing_phase(self, crypttext: Any, starting_key: Any, n: int, starting_loss: float = None):
        if starting_loss is None:
            _, starting_loss = ngram_fitness(self.decrypt(crypttext, starting_key), n=n,
                                             language=self.language, loss=self.loss_fn)
        improved_key = current_key = starting_key
        current_loss = starting_loss
        while improved_key is not None:
            logger.debug(f"Starting Hill Climbing round with {current_key}...")
            improved_key, improved_loss = self.hill_climbing_round(crypttext, current_key,
                                                                   current_loss=current_loss, n=n)
            logger.debug(f"Improved key: {improved_key} ({improved_loss})")
            if improved_key is not None:
                current_key, current_loss = improved_key, improved_loss
        logger.debug(f"[STOP] best key: {current_key}, best loss {current_loss:.3f} "
                     f"(improved? {current_key != starting_key})")
        return current_key, current_loss

    def fit(self, crypttext: Any, ngrams: int = 3, phases: int = 100, **kwargs) -> AnalyzerResult:
        starting_key = self.key_generator.initial_key
        _, starting_loss = ngram_fitness(self.decrypt(crypttext, starting_key), n=ngrams,
                                         language=self.language, loss=self.loss_fn)
        best_keys, best_loss = [starting_key], starting_loss
        current_key, current_loss = starting_key, starting_loss
        # needed to produce new key
        for phase in range(phases):
            if (phase + 1) % int(0.05 * phases) == 0:
                logger.info(f"Phase [{phase + 1}/{phases} {100 * (phase + 1) / phases:.2f}%]...")
                logger.info(f"Decoded so far: '{self.decrypt(crypttext, best_keys[-1])}' ({best_loss:.3f})")
            # logger.debug(f"Trying key {current_key}...")
            new_key, new_loss = self.hill_climbing_phase(crypttext, current_key, starting_loss=current_loss, n=ngrams)
            if new_loss < best_loss:
                logger.info(f"[GREAT SUCCESS] Best key is updated: {new_key} ({new_loss:.3f})")
                best_keys, best_loss = [new_key], new_loss
            elif np.equal(new_loss, best_loss):
                logger.info(f"[SUCCESS] Best key is added: {new_key} ({new_loss:.3f})")
                best_keys.append(new_key)

            # produce new key
            current_key = next(self.key_generator)
            _, current_loss = ngram_fitness(self.decrypt(crypttext, current_key), n=ngrams,
                                            language=self.language, loss=self.loss_fn)
            logger.debug(f"Generated new key: {current_key} ({current_loss:.3f})")
        logger.info(f"[END] Keys: {best_keys} Best loss: {best_loss}")
        return AnalyzerResult(best_keys, best_score=best_loss, score_is_loss=True)
