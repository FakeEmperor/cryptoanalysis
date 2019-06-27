import logging
import math
from collections import Counter
from crypto.language import ENGLISH_FREQUENCY_TABLE, TextDescriptor, match_table

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DATA = "KQEREJEBCPPCJCRKIEACUZBKRVPKRBCIBQCARBJCVFCUP\
KRIOFKPACUZQEPBKRXPEIIEABDKPBCPFCDCCAFIEABDKP\
BCPFEQPKAZBKRHAIBKAPCCIBURCCDKDCCJCIDFUIXPAFF\
ERBICZDFKABICBBENEFCUPJCVKABPCYDCCDPKBCOCPERK\
IVKSCPICBRKIJPKABI\
"

if __name__ == "__main__":
    description = TextDescriptor.describe(DATA)
    crypt_text_mapping = match_table(description.frequencies, ENGLISH_FREQUENCY_TABLE,
                                     rtol=0.1, atol=0.02)
    input()
