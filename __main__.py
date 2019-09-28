import logging
from pathlib import Path

import numpy as np

from crypto.algo.transpositions import DoubleTranspositionCipher
from crypto.analysis.hill import HillClimbingAnalyzer
from crypto.analysis.language.frequency import Language
from crypto.analysis.language.utils import abs_loss
from crypto.utils import KeyGenerator, to_df
np.set_printoptions(precision=3)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%I:%M:%S')

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    crypto_zachet = "ЯНЛВКРАДОЕТЕРГОМИЗЯЕ\
    ЙЛТАЛФЫИПЕУИООГЕДБОР\
    ЧРДЧИЕСМОНДКХИНТИКЕО\
    НУЛАЕРЕБЫЫЕЕЗИОННЫЧД\
    ЫТДОЕМППТЩВАНИПТЯЗСЛ\
    ИКСИ-ТЧНО--Е-ЛУЛ-Т-Ж\
    "
    crypto_zachet_size = (6, 20)
    crypttext = to_df(crypto_zachet, crypto_zachet_size)
    russian = Language(name="russian", root=Path(r"E:\Source\Personal\University\2019\Crypto\data"),
                       mapping={"Ё": "Е"}, encoding="utf-8")
    keygen = KeyGenerator([8, 2, 5, 6, 15, 3, 1, 11, 7, 0, 17, 19, 13, 14, 18, 10, 16, 9, 4, 12],
                          permutation_indices=range(0, 14), linked_groups=[[-1, -2, -3, -4, -5, -6]])
    next_key = next(keygen)
    analyzer = HillClimbingAnalyzer(cipher=DoubleTranspositionCipher(), key_generator=keygen,
                                    loss_fn=abs_loss, key_argname="k2", language=russian)
    analyzer.fit(crypttext, ngrams=4)
    print("Done")
