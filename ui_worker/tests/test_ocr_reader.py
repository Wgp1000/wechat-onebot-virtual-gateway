import unittest

from ui_worker.ocr_reader import extract_left_aligned_lines


class OcrReaderTests(unittest.TestCase):
    def test_filters_known_outbound_and_empty_lines(self):
        from ui_worker.ocr_reader import extract_new_lines
        text = "\n[Adapter Test] inbound\n[WeChat Adapter Test] outbound ok\n"
        self.assertEqual(extract_new_lines(text, outgoing_marker="[WeChat Adapter Test]"), ["[Adapter Test] inbound"])

    def test_only_keeps_left_aligned_ocr_line_groups(self):
        tsv = """level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext
5\t1\t1\t1\t1\t1\t35\t80\t60\t20\t95\tHello
5\t1\t1\t1\t1\t2\t100\t80\t60\t20\t95\tinbound
5\t1\t2\t1\t1\t1\t470\t180\t60\t20\t95\tOld
5\t1\t2\t1\t1\t2\t540\t180\t80\t20\t95\toutbound
"""
        self.assertEqual(extract_left_aligned_lines(tsv, split_x=350), ["Hello inbound"])


if __name__ == "__main__":
    unittest.main()
