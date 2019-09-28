import unittest
from pathlib import Path

from crypto.analysis.language.frequency import Language
from crypto.analysis.vigenere import VigenereAnalyzer


class TestCaesarAnalyzer(unittest.TestCase):

    def test_fit_correct_key_wiki(self):
        language = Language("english", Path(__file__).parent / "files" / "english")
        analyzer = VigenereAnalyzer(language)
        result = analyzer.fit("QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEA"
                              "IZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSP"
                              "MYKVQXJTDCIOMEEXDQVSRXLRLKZHOV")
        self.assertIn("EVERY", result.best_keys)

    def test_fit_correct_key_task(self):
        language = Language("english", Path(__file__).parent / "files" / "english")
        analyzer = VigenereAnalyzer(language)
        result = analyzer.fit("CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBW"
                              "RVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAK"
                              "LXFPSKAUTEMNDCMGTSXMXBTUIADNGMGPSRELXNJELX"
                              "VRVPRTULHDNQWTWDTYGBPHXTFALJHASVBFXNGLLCHR"
                              "ZBWELEKMSJIKNBHWRJGNMGJSGLXFEYPHAGNRBIEQJT"
                              "AMRVLCRREMNDGLXRRIMGNSNRWCHRQHAEYEVTAQEBBI"
                              "PEEWEVKAKOEWADREMXMTBHHCHRTKDNVRZCHRCLQOHP"
                              "WQAIIWXNRMGWOIIFKEE")
        self.assertIn("JANET", result.best_keys)
