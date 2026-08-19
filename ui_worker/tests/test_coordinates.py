import unittest

from ui_worker.coordinates import crop_point_to_root


class CoordinatesTests(unittest.TestCase):
    def test_translates_root_crop_point_to_root_coordinates(self):
        # Screenshots are root captures cropped at root coordinate (430,100).
        self.assertEqual(crop_point_to_root((175, 359), main_origin=(129, 30), crop_origin=(430, 100)), (605, 459))


if __name__ == "__main__":
    unittest.main()
