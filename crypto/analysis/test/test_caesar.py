import unittest
from pathlib import Path

from crypto.analysis.caesar import CaesarAnalyzer
from crypto.analysis.language.frequency import Language


class TestCaesarAnalyzer(unittest.TestCase):

    def test_fit_correct_key(self):
        language = Language("english", Path(__file__).parent / "files" / "english")
        analyzer = CaesarAnalyzer(language)
        result = analyzer.fit("efgfoeuiffbtuxbmmpguifdbtumf")
        self.assertIn("B", result.best_keys)
