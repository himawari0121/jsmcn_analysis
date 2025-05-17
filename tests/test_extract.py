import pathlib
import tempfile
import unittest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from abstracts.extract import parse_directory


SAMPLE_TEXT = """\
【演題番号】1
【演題名】テストタイトル
【著者】太郎
【所属】テスト大学
【セッション】AI
本文1
------
【演題番号】2
【演題名】別のタイトル
【著者】次郎
【所属】別大学
【セッション】ML
本文2
"""


class TestParseDirectory(unittest.TestCase):
    def test_parse_directory(self):
        with tempfile.TemporaryDirectory() as d:
            tmp_dir = pathlib.Path(d)
            (tmp_dir / "sample.txt").write_text(SAMPLE_TEXT, encoding="utf-8")
            rule = pathlib.Path(__file__).resolve().parents[1] / "conf" / "extract" / "jscn.yml"
            df = parse_directory(tmp_dir, rule)
            self.assertEqual(len(df), 2)
            self.assertIn("title", df.columns)
            self.assertEqual(df.iloc[0]["id"], "1")


if __name__ == "__main__":
    unittest.main()

