import unittest

from ui_worker.x11_driver import ChatGeometry, current_chat_send_script


class X11DriverTests(unittest.TestCase):
    def test_send_script_pastes_then_clicks_send_button(self):
        script = current_chat_send_script(ChatGeometry())
        self.assertIn("xclip -selection clipboard", script)
        self.assertIn("xdotool mousemove 1080 736 click 1", script)
        self.assertNotIn("tesseract", script)

    def test_send_geometry_is_scoped_to_main_wechat_window(self):
        geometry = ChatGeometry(main_x=129, main_y=30, main_width=1021, main_height=740)
        self.assertEqual(geometry.input_point, (430, 675))
        self.assertEqual(geometry.send_point, (1080, 736))


if __name__ == "__main__":
    unittest.main()
