import sys
import pathlib
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

# provide a minimal stub so that abstracts.preprocess can be imported without
# the heavy spaCy dependency present
dummy_mod = type("_Dummy", (), {"load": lambda *a, **kw: None, "tqdm": lambda x: x})
sys.modules.setdefault("spacy", dummy_mod)
sys.modules.setdefault("tqdm", dummy_mod)
sys.modules.setdefault("pandas", dummy_mod)

from abstracts.preprocess import clean_text


class TestPreprocess(unittest.TestCase):
    def test_clean_text_basic(self):
        raw = "Visit https://example.com! NLP?"
        cleaned = clean_text(raw)
        self.assertEqual(cleaned, "visit nlp")


if __name__ == "__main__":
    unittest.main()
