import math
from collections import Counter


data = "KCCPKBGUFDPHQTYAVINRRTMVGRKDNBVFDETDGILTXRGUD\
DKOTFMBPVGEGLTGCKQRACQCWDNAWCRXIZAKFTLEWRPTYC\
QKYVXCHKFTPONCQQRHJVAJUWETMCMSPKQDYHJVDAHCTRL\
SVSKCGCZQQDZXGSFRLSWCWSJTBHAFSIASPRJAHKJRJUMV\
GKMITZHFPDISPZLVLGWTFPLKKEBDPGCEBSHCTJRWXBAFS\
PEZQNRWXCVYCGAONWDDKACKAWBBIKFTIOVKCGGHJVLNHI\
FFSQESVYCLACNVRWBBIREPBBVFEXOSCDYGZWPFDTKFQIY\
CWHJVLNHIQIBTKHJVNPIST"


def entropy(text, keylen: int=1):
    text = text[::keylen]
    print(f"Text to be considered: {text}")
    counts = Counter(text)
    freqs = {}
    entropy_result = 0.0
    for word, count in counts.items():
        p = (count / len(text))
        freqs[word] = p
        entropy_result -= p*math.log2(p)
    print(f"ENTROPY FOR keylen={keylen}")
    print(entropy_result)
    return entropy_result, freqs


if __name__ == "__main__":
    min_i, min_entropy = None, None
    for i in range(1, 20):
        entropy_result, freqs = entropy(data, i)
        print("==========================")
        print(f"I(text)={freqs['I']}")
        if min_entropy is None or min_entropy >= entropy_result:
            min_i = i
            min_entropy = entropy_result

    print(f"Minimal entropy: {min_i}, {min_entropy}")
    input()
