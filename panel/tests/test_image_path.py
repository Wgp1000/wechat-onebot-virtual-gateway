import unittest

from panel.web import qr_image_path


class PanelImagePathTests(unittest.TestCase):
    def test_qr_path_is_relative_to_keep_the_tunnel_subpath(self):
        self.assertEqual(qr_image_path(), "qr.png")


if __name__ == "__main__":
    unittest.main()
