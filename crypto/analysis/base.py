"""
Base interface for all analysis tools
"""
from abc import abstractmethod
from typing import Any, NamedTuple, Iterable, Sized, Union


class AnalyzerResult(NamedTuple):
    best_keys: Union[Iterable[Any], Sized]
    """
    Best keys produced by the analyzer that have the best loss.
    A dictionary of cipher algorithms and a list of all matched keys for that algo
    """
    best_score: float
    """
    Best loss after fitting
    """
    score_is_loss: bool = True


class BaseAnalyzer:

    @abstractmethod
    def decrypt(self, crypttext: Any, key: Any, **kwargs) -> str:
        raise NotImplementedError()

    @abstractmethod
    def fit(self, crypttext: Any, **kwargs) -> AnalyzerResult:
        raise NotImplementedError()


class BaseKeyGenerator:
    """
    Key generator "slot machine" which produces new keys
    based on some initial information.
    """

    @property
    def initial_key(self) -> Any:
        """
        Initial key to use in hill climbing
        """
        raise NotImplementedError()

    def hill_climbing(self, key: Any) -> Iterable[Any]:
        raise NotImplementedError()

    def __iter__(self) -> 'BaseKeyGenerator':
        return self

    def __next__(self) -> Any:
        """
        Return next key to use
        """
        raise NotImplementedError()
