import unittest
from sensehat_manager import SenseHatManager

class TestSenseHatManager(unittest.TestCase):

    def setUp(self):
        # Initialize the SenseHatManager
        self.sense_manager = SenseHatManager()

    def test_generate_pattern(self):
        # Test that a pattern is generated correctly
        pattern = self.sense_manager.generate_pattern()
        self.assertEqual(len(pattern), 4)  # Assuming 4x4 pattern
        self.assertTrue(all(len(row) == 4 for row in pattern))

    def test_display_pattern(self):
        # Mock Sense HAT display (this may require mocking the actual hardware)
        pattern = [[True, False, True, False], [False, True, False, True]]
        try:
            self.sense_manager.display_pattern(pattern)
        except Exception as e:
            self.fail(f"Display pattern raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
