from typing import Union, Sequence


def from_alphabet(alphabet: Union[str, Sequence[str]], lower: bool = True) -> str:
    alphabet = "".join(alphabet) if not isinstance(alphabet, str) else alphabet
    if len(alphabet) != len(set(alphabet)):
        raise ValueError("Passed alphabet must not contain duplicate characters!")
    if lower:
        alphabet = alphabet.upper()
    return alphabet
