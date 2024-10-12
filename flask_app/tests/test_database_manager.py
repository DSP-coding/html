import unittest
from database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        # Initialize with test configuration
        self.db_config = {
            'host': 'localhost',
            'database': 'iq_test',
            'user': 'flaskuser',
            'password': 'pi64'
        }
        self.db_manager = DatabaseManager(self.db_config)

    def test_database_connection(self):
        # Test that the connection to the database is successful
        conn = self.db_manager.connect()
        self.assertIsNotNone(conn)

    def test_fetch_high_scores(self):
        # Test that high scores are fetched correctly (assuming database has data)
        high_scores = self.db_manager.fetch_high_scores()
        self.assertIsInstance(high_scores, list)

    def test_insert_score(self):
        # Test inserting a score into the database
        username = "test_user"
        score = 50
        result = self.db_manager.insert_score(username, score)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
