import unittest

from ui_worker.inbox_scan import parse_list_tsv


class InboxScanTests(unittest.TestCase):
    def test_groups_words_by_row_and_extracts_title_preview_time(self):
        tsv = """level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext
5\t1\t1\t1\t1\t1\t10\t10\t60\t12\t92\tAlice
5\t1\t1\t1\t2\t1\t10\t30\t90\t10\t92\tHello
5\t1\t1\t1\t3\t1\t160\t10\t30\t12\t92\t12:30
5\t1\t2\t1\t1\t1\t10\t90\t60\t12\t92\tBob
5\t1\t2\t1\t2\t1\t10\t110\t90\t10\t92\tPreview
5\t1\t2\t1\t3\t1\t160\t90\t30\t12\t92\t12:31
"""
        rows = parse_list_tsv(tsv, row_height=80)
        self.assertEqual([(row.title, row.preview, row.timestamp, row.row) for row in rows], [("Alice", "Hello", "12:30", 0), ("Bob", "Preview", "12:31", 1)])

    def test_ignores_low_confidence_noise(self):
        tsv = """level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext
5\t1\t1\t1\t1\t1\t10\t10\t20\t10\t20\tNoise
"""
        self.assertEqual(parse_list_tsv(tsv, row_height=80), [])

    def test_uses_actual_scaled_row_coordinates(self):
        tsv = """level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext
5\t1\t1\t1\t1\t1\t20\t30\t60\t20\t90\tAlice
5\t1\t1\t1\t2\t1\t20\t70\t60\t20\t90\tHi
5\t1\t2\t1\t1\t1\t20\t270\t60\t20\t90\tBob
5\t1\t2\t1\t2\t1\t20\t310\t60\t20\t90\tYo
"""
        rows = parse_list_tsv(tsv, row_height=240)
        self.assertEqual([(row.title, row.preview) for row in rows], [("Alice", "Hi"), ("Bob", "Yo")])


if __name__ == "__main__":
    unittest.main()
