import unittest
from game_controller import GameController

class TestGameController(unittest.TestCase):
    
    def setUp(self):
        # Initialize with a test user and test configuration
        self.user = "test_user"
        self.db_config = {
            'host': 'localhost',
            'database': 'iq_test',
            'user': 'flaskuser',
            'password': 'pi64'
        }
        self.controller = GameController(self.user, self.db_config)

    def test_initial_round_count(self):
        # Test that the round count is initialized correctly
        self.assertEqual(self.controller.round_count, 0)

    def test_start_round(self):
        # Test that starting a round increases round count
        self.controller.start_round()
        self.assertEqual(self.controller.round_count, 1)

    def test_calculate_score(self):
        # Mock patterns and user input
        correct_pattern = [[True, False, False, True], [False, True, True, False]]
        user_pattern = [[True, False, False, True], [False, False, True, True]]
        score = self.controller.calculate_score(user_pattern, correct_pattern)
        self.assertEqual(score, 2)  # Assuming it scores based on number of correct cells

    def test_save_score(self):
        # Test saving score (this may need database mocking)
        score = 10
        self.controller.save_score(score)
        # Here you would check the database, but a mock would be more appropriate
        # Check that no exceptions occur

if __name__ == '__main__':
    unittest.main()
