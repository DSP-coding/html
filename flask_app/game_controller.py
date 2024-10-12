import random
import time
import threading
from sensehat_manager import SenseHatManager
from database_manager import DatabaseManager

class GameController:
    def __init__(self, username, db_config):
        self.username = username
        self.patterns = []
        self.round_count = 0
        self.max_rounds = 5
        self.correct_answers = 0
        self.total_time_taken = 0  # Total time taken for all rounds
        self.sense_hat_manager = SenseHatManager()
        self.db_manager = DatabaseManager(db_config)
        self.start_time = None  # Timer start time
        self.display_thread = None  # Thread for displaying patterns

    def start_round(self):
        self.sense_hat_manager.show_orientation()
        pattern = self.generate_pattern()
        self.patterns.append(pattern)
        self.round_count += 1
        self.start_time = time.time()  # Start the timer
        self.display_thread = threading.Thread(target=self.display_pattern_thread, args=(pattern, 8))
        self.display_thread.start()  # Start the thread to display pattern

    def display_pattern_thread(self, pattern, duration):
        self.sense_hat_manager.display_pattern(pattern, duration)

    def generate_pattern(self):
        return [[random.choice([True, False]) for _ in range(4)] for _ in range(4)]

    def calculate_efficiency(self):
        if self.round_count > 0:
            average_time = self.total_time_taken / self.round_count
            efficiency = (self.correct_answers / self.max_rounds) * 100
            adjusted_efficiency = efficiency - average_time  # Adjust if needed
            print(f"Calculated efficiency for {self.username}: {adjusted_efficiency}")  # Debug line
            return max(adjusted_efficiency, 0)  # Ensure efficiency is not negative
        return 0

    def save_score(self):
        score = self.calculate_efficiency()  # Calculate efficiency as score
        print(f"Calculated efficiency score for {self.username}: {score}")  # Debug line
        self.db_manager.save_score(self.username, score)  # Save efficiency as score

    def calculate_score(self, user_pattern, correct_pattern):
        score = 0
        for i in range(4):
            for j in range(4):
                if user_pattern[i][j] == correct_pattern[i][j]:
                    score += 1
        return score

    def reset_game(self):
        self.patterns = []
        self.round_count = 0
        self.correct_answers = 0  # Reset correct answers
        self.total_time_taken = 0  # Reset total time
        self.start_time = None  # Reset timer
