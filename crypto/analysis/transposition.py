import itertools
import random
from typing import Tuple, List, Iterator, Iterable, Set, Any

from crypto.analysis.base import BaseKeyGenerator
from crypto.utils import swap_elements


class TranspositionKeyGenerator(BaseKeyGenerator):
    """
    Key generator "slot machine" which produces new keys
    based on some initial information.

    This particular generator produces random keys, honoring some restrictions
    put on the structure of a new key.

    :param linked_groups: a list of groups of indices in an initial
    key which should be considered as a single group.
    Imagine the following:
    initial key [a, b, c, d, e, f]
    linked groups: [{0, 1}, {-2, -1}]
    this means that key generation will consider first two and last two
    indices of an initial key as two elements, respecting their relative positions.

    Note: restrictions on those groups apply:
    - they must be continous ((0,1,2,3) not (0,2,3))
    - they must be disjoint: all indices must be present only in one linked group

    :param permutation_indices: a set of all indices which are allowed to be permuted
    independently.

    Note: restrictions on those indices apply:
    - should not intersect with linked groups
    - linked groups and permutation indices should produce a list of all indices
    """

    @classmethod
    def _verify_linked_groups(cls, key: List[int], linked_groups: List[Iterable[int]]) -> List[Set[int]]:
        if not linked_groups:
            return []
        linked_groups = [set([(idx if idx >= 0 else len(key) + idx) for idx in group]) for group in linked_groups]
        union = set()
        for group in linked_groups:
            # verify disjoint
            union_size = len(union)
            intersection = union.intersection(group)
            union = union.union(group)
            if len(union) != (union_size + len(group)):
                raise ValueError(f"Linked group {group} has a repeated elements {intersection} present "
                                 f"somewhere in other groups")
            # verify continuity
            group = sorted(group)
            for idx in range(1, len(group)):
                if group[idx] - group[idx - 1] > 1:
                    raise ValueError(f"Group {group} in linked groups has non-continous elements: "
                                     f"{group[idx]} and {group[idx - 1]}")
        return linked_groups

    @classmethod
    def _verify_permutation_indices(cls, key: List[int],
                                    permutation_indices: Iterable[int],
                                    linked_groups: List[Set[int]]) -> List[int]:
        total_linked_groups = set().union(*linked_groups)
        if permutation_indices is None:
            return [s for s in range(len(key)) if s not in total_linked_groups]
        permutation_indices = list(permutation_indices)
        for idx in permutation_indices:
            if idx in total_linked_groups:
                raise ValueError(f"Value {idx} of permutation indices is present in one of the linked groups!")
        all_indices = sorted(list(total_linked_groups) + permutation_indices)
        if all_indices != list(range(len(key))):
            raise ValueError(f"Union of permutation indices and linked groups does "
                             f"not sum up to a range over length of key: {all_indices}")
        return permutation_indices

    def __init__(self, initial_key: List[int], linked_groups: List[Iterable[int]] = None,
                 permutation_indices: Iterable[int] = None,
                 shuffle_linked_groups_outer: bool = False):
        self._initial_key = initial_key
        self.linked_groups = linked_groups
        self.permutation_indices = permutation_indices
        self.shuffle_linked_groups_outer = shuffle_linked_groups_outer
        self.linked_groups = self._verify_linked_groups(self.initial_key, self.linked_groups)
        self.permutation_indices = self._verify_permutation_indices(self.initial_key,
                                                                    self.permutation_indices,
                                                                    self.linked_groups)

    @property
    def initial_key(self) -> Any:
        return self._initial_key

    def __iter__(self) -> Iterator[List[int]]:
        return self

    def __next__(self) -> List[int]:
        shuffling_elements = [*self.permutation_indices,
                              *(self.linked_groups if self.shuffle_linked_groups_outer else [])]
        random.shuffle(shuffling_elements)
        return [
            self.initial_key[idx]
            for sublist in shuffling_elements
            for idx in (sublist if not isinstance(sublist, int) else [sublist])
        ] + (
            [self.initial_key[idx] for group in self.linked_groups for idx in group]
            if not self.shuffle_linked_groups_outer else []
        )

    def hill_climbing(self, key: List[int]) -> Iterator[List[int]]:
        permutations = itertools.permutations(self.permutation_indices, 2)
        swap: Tuple[int, int]
        for swap in permutations:
            yield swap_elements(key, swap=swap)
